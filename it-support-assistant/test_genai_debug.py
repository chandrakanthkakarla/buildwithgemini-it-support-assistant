import asyncio
from google.genai import Client
from app.agent import PROJECT_ID

async def main():
    client = Client(vertexai=True, project=PROJECT_ID, location="global")
    try:
        interaction = client.interactions.create(
            model="gemini-omni-flash-preview",
            input="A short test video",
            response_format={"type": "video"}
        )
        print("Output Video object type:", type(interaction.output_video))
        print("Attributes:", dir(interaction.output_video))
        if hasattr(interaction.output_video, 'video_bytes'):
            print("Has video_bytes")
        if hasattr(interaction.output_video, 'video'):
            print("Has video")
        if hasattr(interaction.output_video, 'bytes'):
            print("Has bytes")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
