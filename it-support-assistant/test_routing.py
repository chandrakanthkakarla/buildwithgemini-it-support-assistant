import asyncio
from google.adk.runners import InMemoryRunner
from app.agent import root_agent

# Patch the tool so it doesn't actually call the Vertex AI API and take 60s
original_func = None
for i, t in enumerate(root_agent.tools):
    if t.name == "generate_it_support_video":
        original_func = t
        
        async def fake_video_tool(prompt: str, tool_context) -> dict:
            print(f"*** TOOL CALLED! Prompt: {prompt} ***")
            return {"status": "success", "message": "Fake video generated", "public_url": "http://fake.com/vid.mp4"}
            
        from google.adk.tools import FunctionTool
        root_agent.tools[i] = FunctionTool(fake_video_tool, name="generate_it_support_video")
        break

async def main():
    runner = InMemoryRunner(agent=root_agent, app_name="app")
    
    print("\n--- Test 1: Video Request ---")
    prompt1 = "Generate a short video showing how to plug in an ethernet cable to fix network connectivity."
    async for event in runner.run_async(user_id="test1", prompt=prompt1):
        if event.content:
            print("Response:", event.content.text)
            
    print("\n--- Test 2: Normal Troubleshooting ---")
    prompt2 = "How do I troubleshoot a DNS problem?"
    async for event in runner.run_async(user_id="test1", prompt=prompt2):
        if event.content:
            print("Response:", event.content.text)

if __name__ == "__main__":
    asyncio.run(main())
