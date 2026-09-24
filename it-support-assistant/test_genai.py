import asyncio
from google.genai import Client
from app.agent import PROJECT_ID

async def main():
    print("Testing genai client directly...")
    client = Client(vertexai=True, project=PROJECT_ID, location="global")
    try:
        interaction = client.interactions.create(
            model="gemini-omni-flash-preview",
            input="A very short 1 second video of a red bouncing ball",
            response_format={"type": "video"}
        )
        if hasattr(interaction, "output_video") and interaction.output_video:
            print(f"Success! Received {len(interaction.output_video.video_bytes)} bytes of video data.")
        else:
            print("Failed: No video output in response.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
