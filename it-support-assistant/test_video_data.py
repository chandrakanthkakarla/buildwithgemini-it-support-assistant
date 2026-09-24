import asyncio
from google.genai import Client
from app.agent import PROJECT_ID
import base64

async def main():
    client = Client(vertexai=True, project=PROJECT_ID, location="global")
    try:
        interaction = client.interactions.create(
            model="gemini-omni-flash-preview",
            input="A short test video",
            response_format={"type": "video"}
        )
        data = interaction.output_video.data
        print("Data type:", type(data))
        if isinstance(data, bytes):
            print("Data (first 20 bytes):", data[:20])
        elif isinstance(data, str):
            print("Data (first 20 chars):", data[:20])
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
