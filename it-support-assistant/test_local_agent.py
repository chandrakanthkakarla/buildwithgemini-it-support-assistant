import asyncio
from google.adk.runners import InMemoryRunner
from app.agent import root_agent

async def main():
    runner = InMemoryRunner(agent=root_agent, app_name="app")
    
    print("Sending prompt to local agent...")
    async for event in runner.run_async(user_id="tester", prompt="Generate a short video showing how to plug in an ethernet cable to fix network connectivity."):
        if event.content:
            print("Response:", event.content)
            
if __name__ == "__main__":
    asyncio.run(main())
