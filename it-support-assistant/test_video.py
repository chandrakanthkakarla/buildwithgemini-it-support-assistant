import asyncio
from google.adk.tools import ToolContext
from google.adk.artifacts import InMemoryArtifactService
from app.agent import generate_it_support_video

async def main():
    ctx = ToolContext()
    ctx._artifact_service = InMemoryArtifactService()
    ctx.session_id = "test_session"
    result = await generate_it_support_video("A short cinematic drone shot of a data center server rack", ctx)
    print("Result:", result)
    
    # Check artifacts
    artifacts = await ctx.list_artifacts()
    print("Saved artifacts:", artifacts)

if __name__ == "__main__":
    asyncio.run(main())
