<div align="center">

<img src="assets/build-with-gemini-banner.png" alt="Build with Gemini" width="100%" />

# 🚀 Build with Gemini · Track 3

### The starter kit for Track 3 of the Build with Gemini World Tour, and a showcase of participant projects.

Clone this repo, open [Antigravity](https://antigravity.google), and build your agent-first app on Google Cloud. Every featured project was prototyped with Antigravity and `agents-cli`, equipped with Memory, tools, and storage, deployed to Agent Platform, and hosted on Cloud Run.

<sub>📖 <a href="https://cszhu.github.io/build-with-gemini/">Lab Guide</a> · 🛠️ <a href="https://google.github.io/agents-cli/guide/getting-started/">agents-cli</a> · 🤖 <a href="https://google.github.io/adk-docs/">ADK</a></sub>

</div>

---

## 📚 Table of Contents

- [🧩 Anatomy of a Track 3 Project](#-anatomy-of-a-track-3-project)
- [📂 Featured Projects](#-featured-projects)
- [🧠 What's in this Repo](#-whats-in-this-repo)
- [🧰 Build Your Own](#-build-your-own)
- [📚 Resources](#-resources)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🧩 Anatomy of a Track 3 Project

Every app in this collection uses standard Google Cloud building blocks:

| Layer | What it does | Powered by |
|---|---|---|
| 🤖 **The Agent** | Core reasoning loop | [ADK](https://google.github.io/adk-docs/) + [`agents-cli`](https://google.github.io/agents-cli/guide/getting-started/), scaffolded with [Antigravity](https://antigravity.google) |
| 🧠 **Memory** | Remembers facts across sessions | [Agent Platform Memory Bank](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/memory-bank) |
| 🗄️ **Structured Data** | Inventory, records, lists | [Firestore](https://console.cloud.google.com/firestore) |
| 🖼️ **Files & Blobs** | Images, media, assets | [Cloud Storage](https://console.cloud.google.com/storage) |
| 🔧 **Tools** | Takes real actions and fetches data | ADK function tools |
| 🎨 **Media Generation** | Generates images and video | `gemini-3.1-flash-lite-image` · Omni |
| 🧪 **Code Sandbox** | Safely runs generated code | Agent Platform code execution |
| 🪟 **Agent-first UI** | Cards and tables UI | [A2UI](https://adk.dev/integrations/a2ui/) |
| 🌐 **Frontend** | Shareable web UI | FastAPI proxy on [Cloud Run](https://cloud.google.com/run) |

---

## 📂 Featured Projects

### 🍳 Food & Recipe Agents

- 🥫 **[Smart Pantry Recipe Concierge](https://github.com/matthewrose/buildwithgemini-smart-pantry-recipe-concierge)**: Tracks your pantry and recommends recipes grounded in a real recipe corpus. <br/> <sub>by [@matthewrose](https://github.com/matthewrose)</sub>

### ✈️ Travel & Local Agents

- ⛈️ **[SafeStageWX](https://github.com/felix1028/buildwithgemini-safestagewx)**: An agentic mobile app that helps event planners identify weather threats and climate risks for an event given its date and location. <br/> <sub>by [@felix1028](https://github.com/felix1028)</sub>
- 🌇 **[Sidewalk & Sun](https://github.com/OlafHaalstra/buildwithgemini-sidewalk-and-sun)**: Recommends sunny or shaded NYC spots from a curated 500-venue corpus, plotted on an interactive map. <br/> <sub>by [@OlafHaalstra](https://github.com/OlafHaalstra)</sub>

### 💪 Health, Fitness & Wellness Agents

- 🏊 **[TriCoach AI](https://github.com/common-aman/buildwithgemini-tricoach-ai)**: A triathlon coach that logs workouts, computes training zones, and generates motivational visuals. <br/> <sub>by [@common-aman](https://github.com/common-aman)</sub>

### 📚 Learning & Knowledge Agents

- 🎤 **[Interview Coach (PrepPal)](https://github.com/VineethBaradi/buildwithgemini-interview-coach)**: A mock-interview coach that runs LLM-driven practice sessions from a Firestore question bank. <br/> <sub>by [@VineethBaradi](https://github.com/VineethBaradi)</sub>

### 🏢 Productivity & Enterprise Agents

- 🔧 **[GitCraft](https://github.com/fpobletemu/buildwithgemini-gitcraft)**: A developer git assistant that inspects your repo and drafts Conventional-Commits-style messages. <br/> <sub>by [@fpobletemu](https://github.com/fpobletemu)</sub>
- 🖥️ **[IT Helpdesk Agent](https://github.com/NaweedAhmadi/buildwithgemini-it-helpdesk-agent)**: An IT support assistant that answers from a knowledge base and retains context across sessions. <br/> <sub>by [@NaweedAhmadi](https://github.com/NaweedAhmadi)</sub>

### 🧪 Experimental & Other

- 🃏 **[Poker Agent](https://github.com/jakecho1108/buildwithgemini-poker-agent)**: A poker trainer with a real 800-iteration Monte Carlo equity engine and strategy tips. <br/> <sub>by [@jakecho1108](https://github.com/jakecho1108)</sub>

---

## 🧠 What's in this Repo

The `.agents/` folder configures Antigravity to build agents on Google Cloud.

### Skills

| Skill | What it does |
| --- | --- |
| [`pick-your-agent-project`](.agents/skills/pick-your-agent-project/SKILL.md) | Brainstorm your app idea and write a project brief |
| [`troubleshoot-lab-setup`](.agents/skills/troubleshoot-lab-setup/SKILL.md) | Verify environment and fix common setup errors |
| [`memory-bank-setup`](.agents/skills/setup-memory-bank/SKILL.md) | Add cross-session memory with Vertex AI Memory Bank |
| [`enable-a2ui`](.agents/skills/enable-a2ui/SKILL.md) | Enable rich UI cards (A2UI) in the ADK dev UI |
| [`build-agent-frontend`](.agents/skills/build-agent-frontend/SKILL.md) | Generate a FastAPI chat frontend and deploy to Cloud Run |
| [`record-demo`](.agents/skills/record-demo/SKILL.md) | Record a branded demo video of your agent |
| [`publish-to-github`](.agents/skills/publish-to-github/SKILL.md) | Publish finished project to GitHub and submit for swag |

### MCP Tools Config

[`.agents/mcp_config.json`](.agents/mcp_config.json) integrates Model Context Protocol (MCP) servers:

- **Firebase**: Work directly with Firestore and Firebase services.
- **Google Developer Knowledge**: Grounded access to official documentation.

---

## 🧰 Build Your Own

**Prerequisites:**

- Google Cloud project with billing enabled
- [Antigravity](https://antigravity.google) (`agy`)
- [agents-cli](https://google.github.io/agents-cli/guide/getting-started/) (built on ADK)
- Authenticated `gcloud` CLI

**Quickstart:**

```bash
git clone [https://github.com/cszhu/build-with-gemini](https://github.com/cszhu/build-with-gemini)
cd build-with-gemini
agy
