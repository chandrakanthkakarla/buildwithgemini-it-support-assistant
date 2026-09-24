# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import re
import shutil
import socket
import subprocess
import time
from zoneinfo import ZoneInfo

from a2ui.basic_catalog.provider import BasicCatalog
from a2ui.schema.manager import A2uiSchemaManager
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.cloud import firestore, storage
from google.genai import types, Client as GenaiClient
from google.adk.tools import ToolContext
import uuid

from .a2ui_utils import a2ui_callback

PROJECT_ID = "qwiklabs-gcp-01-3c21c96f2321"

schema_manager = A2uiSchemaManager(
    version="0.8",
    catalogs=[BasicCatalog.get_config("0.8")],
)

instruction = schema_manager.generate_system_prompt(
    role_description="You are an IT Support Assistant specializing in networking, Linux, AWS, and cybersecurity issues.",
    workflow_description=(
        "Analyze the user request. Use ping_host to test server reachability, and use search_troubleshooting_guides and get_troubleshooting_guide to search and retrieve solutions stored in Firestore. "
        "When rendering a single troubleshooting guide, return a clean A2UI Card. "
        "When displaying multiple troubleshooting guides, render them as a simple table using Column and Row components of Text. "
        "For general questions or simple conversational answers where a card or table is not useful, reply in plain text without A2UI JSON.\n\n"
        "VIDEO REQUESTS:\n"
        "When the user explicitly asks to generate, create, make, or show a video about an IT-support topic, ALWAYS call `generate_it_support_video` instead of answering with a text-only guide or searching Firestore first.\n\n"
        "Examples that MUST call the video tool:\n"
        "- \"Generate a video showing how to plug in an Ethernet cable.\"\n"
        "- \"Create a video explaining DNS troubleshooting.\"\n"
        "- \"Make a short video showing how to troubleshoot Wi-Fi.\"\n"
        "- \"Show me a video about fixing network connectivity.\"\n\n"
        "The tool must be called even if there is no matching troubleshooting guide in Firestore.\n\n"
        "Only use Firestore troubleshooting tools when the user is asking for a textual troubleshooting solution and is NOT explicitly requesting a video."
    ),
    ui_description=(
        "Keep every surface tiny and flat: ONE Card > ONE Column > a few Text rows. "
        "Never nest a Card inside a Card. "
        "Use ONLY these components: Card, Column, Row, Text. Do not use Table or Heading components (unsupported; use Rows/Columns of Text instead). "
        "No markdown in text; use the usageHint property ('h1', 'h2', 'body') for headings and emphasis. "
        "Output ONLY the raw A2UI JSON array when rendering UI — no prose, and never wrap it in <a2a_datapart_json> tags."
    ),
    include_schema=True,
    include_examples=True,
)


def ping_host(host: str) -> dict:
    """Run a simple ICMP or socket ping test to check if a remote host or IP address is reachable.

    Args:
        host: Target hostname or IP address (e.g. "8.8.8.8" or "google.com").

    Returns:
        A dictionary containing reachability status, average latency in ms, and packet loss percentage.
    """
    clean_host = host.strip()
    if not clean_host or re.search(r"[^\w\.-]", clean_host):
        return {
            "host": host,
            "status": "unreachable",
            "error": "Invalid hostname or IP address format.",
        }

    # If system 'ping' command is available, use CLI ping
    if shutil.which("ping"):
        try:
            res = subprocess.run(
                ["ping", "-c", "2", "-W", "2", clean_host],
                capture_output=True,
                text=True,
                timeout=5,
            )

            output = res.stdout + res.stderr
            packet_loss = 100.0
            loss_match = re.search(r"(\d+)% packet loss", output)
            if loss_match:
                packet_loss = float(loss_match.group(1))

            latency_ms = None
            rtt_match = re.search(r"rtt min/avg/max/mdev = [\d\.]+/([\d\.]+)/", output)
            if rtt_match:
                latency_ms = float(rtt_match.group(1))

            is_reachable = res.returncode == 0 and packet_loss < 100.0
            return {
                "host": clean_host,
                "status": "reachable" if is_reachable else "unreachable",
                "avg_latency_ms": latency_ms,
                "packet_loss_percent": packet_loss,
            }
        except Exception:
            pass

    # Socket connection fallback when system 'ping' binary is absent
    try:
        ip = socket.gethostbyname(clean_host)
        start_time = time.time()
        connected = False
        for port in (443, 80, 53):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2.0)
            try:
                s.connect((ip, port))
                connected = True
                s.close()
                break
            except Exception:
                s.close()

        latency_ms = round((time.time() - start_time) * 1000, 2)

        if connected:
            return {
                "host": clean_host,
                "status": "reachable",
                "avg_latency_ms": latency_ms,
                "packet_loss_percent": 0.0,
            }
        else:
            return {
                "host": clean_host,
                "status": "unreachable",
                "avg_latency_ms": None,
                "packet_loss_percent": 100.0,
            }
    except Exception as e:
        return {
            "host": clean_host,
            "status": "unreachable",
            "avg_latency_ms": None,
            "packet_loss_percent": 100.0,
            "error": f"Resolution or connection failed: {str(e)}",
        }


def search_troubleshooting_guides(query: str = "") -> list[dict]:
    """Search for IT troubleshooting guides in Firestore by query string or list all guides if query is empty.

    Args:
        query: Search term to filter troubleshooting guides by title, category, symptoms, solution, or commands.

    Returns:
        A list of matching troubleshooting guide dictionaries from Firestore.
    """
    db = firestore.Client(project=PROJECT_ID)
    docs = db.collection("troubleshooting_guides").stream()

    results = []
    query_lower = query.lower().strip()

    for doc in docs:
        guide = doc.to_dict()
        guide["id"] = doc.id
        if not query_lower:
            results.append(guide)
        else:
            searchable_text = f"{guide.get('title', '')} {guide.get('category', '')} {guide.get('symptoms', '')} {guide.get('solution', '')} {guide.get('commands', '')}".lower()
            if query_lower in searchable_text:
                results.append(guide)

    return results


def get_troubleshooting_guide(guide_id: str) -> dict:
    """Retrieve a specific troubleshooting guide from Firestore by its document ID.

    Args:
        guide_id: The document ID of the troubleshooting guide in Firestore.

    Returns:
        A dictionary containing the troubleshooting guide details or an error message.
    """
    db = firestore.Client(project=PROJECT_ID)
    doc = db.collection("troubleshooting_guides").document(guide_id).get()

    if doc.exists:
        data = doc.to_dict()
        data["id"] = doc.id
        return data
    return {"error": f"Guide with ID '{guide_id}' not found."}


def get_weather(query: str) -> str:
    """Simulates a web search. Use it get information on weather.

    Args:
        query: A string containing the location to get weather information for.

    Returns:
        A string with the simulated weather information for the queried location.
    """
    if "sf" in query.lower() or "san francisco" in query.lower():
        return "It's 60 degrees and foggy."
    return "It's 90 degrees and sunny."


def get_current_time(query: str) -> str:
    """Simulates getting the current time for a city.

    Args:
        query: The name of the city to get the current time for.

    Returns:
        A string with the current time information.
    """
    if "sf" in query.lower() or "san francisco" in query.lower():
        tz_identifier = "America/Los_Angeles"
    else:
        return f"Sorry, I don't have timezone information for query: {query}."

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    return f"The current time for query {query} is {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"


async def generate_it_support_video(prompt: str, tool_context: ToolContext) -> dict:
    """Generates a short instructional IT support video based on the prompt.

    Call this tool immediately when the user explicitly asks to generate, create, make, or show a video about an IT support topic. Do not search Firestore first for video requests. Only use this tool to generate videos related to IT support, networking, or troubleshooting.

    Args:
        prompt: A descriptive prompt of what the video should show (e.g. "A person plugging in an ethernet cable into a router").
        tool_context: Context for saving artifacts.

    Returns:
        A dictionary containing the status, a public Cloud Storage URL, or an error message.
    """
    # 1. Generate video bytes using Omni model
    client = GenaiClient(vertexai=True, project=PROJECT_ID, location="global")
    try:
        interaction = client.interactions.create(
            model="gemini-omni-flash-preview",
            input=prompt,
            response_format={"type": "video"}
        )
        import base64
        if not hasattr(interaction, "output_video") or not interaction.output_video:
            return {"status": "error", "message": "Failed to generate video: No video output received."}
            
        raw_data = interaction.output_video.data
        if isinstance(raw_data, str):
            video_bytes = base64.b64decode(raw_data)
        elif isinstance(raw_data, bytes) and raw_data.startswith(b"AAAAGGZ0"):
            video_bytes = base64.b64decode(raw_data)
        else:
            video_bytes = raw_data
    except Exception as e:
         return {"status": "error", "message": f"Video generation failed: {str(e)}"}

    filename = f"instructional_video_{uuid.uuid4().hex[:8]}.mp4"
    
    # 2. Save video as a Playground artifact
    try:
        part = types.Part(inline_data=types.Blob(mime_type="video/mp4", data=video_bytes))
        await tool_context.save_artifact(filename, part)
    except Exception as e:
        print(f"Failed to save artifact: {e}")

    # 3. Upload to Cloud Storage
    bucket_name = "qwiklabs-gcp-01-3c21c96f2321-static-assets-bucket"
    try:
        storage_client = storage.Client(project=PROJECT_ID)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(filename)
        blob.upload_from_string(video_bytes, content_type="video/mp4")
        
        public_url = f"https://storage.googleapis.com/{bucket_name}/{filename}"
        return {
            "status": "success",
            "message": "Video generated and uploaded successfully.",
            "public_url": public_url
        }
    except Exception as e:
         return {"status": "error", "message": f"Cloud Storage upload failed: {str(e)}"}


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=instruction,
    tools=[
        ping_host,
        search_troubleshooting_guides,
        get_troubleshooting_guide,
        get_weather,
        get_current_time,
        generate_it_support_video,
    ],
    after_model_callback=a2ui_callback,
)

app = App(
    root_agent=root_agent,
    name="app",
)


