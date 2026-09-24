import asyncio
import os
import uuid
from google.cloud import storage
from google.genai import types, Client as GenaiClient
from app.agent import generate_it_support_video, PROJECT_ID

class DummyContext:
    async def save_artifact(self, name, part, **kwargs):
        print(f"Artifact {name} saved.")
        return 1

async def main():
    ctx = DummyContext()
    print("Testing generate_it_support_video...")
    res = await generate_it_support_video("A short cinematic drone shot of a data center server rack", ctx)
    print("Result:", res)

if __name__ == "__main__":
    asyncio.run(main())
