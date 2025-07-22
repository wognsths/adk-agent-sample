# Financial Research Agent

A **multi‑agent investment‑research system** powered by **Google ADK**, **Gemini 2.5** models, and external data services (Smithery EXA, Financial Modeling Prep, Fed).

---

## Features

* **Parallel Company, Macro, and Financial Search** – three specialised agents run in sequence and then hand results to a synthesis agent.
* **Pluggable Tooling** – drop‑in MCP toolsets for Smithery and FMP; easy to add more.

---

## Directory Structure

```text
financial-research-agent/
├── assets/                 # Sample results
├── agents/                 # Company, FMP, and FOMC agents
├── src/                    # Entry point for `adk web` demo
├── .env.example            # Copy → .env and update keys
└── pyproject.toml          # uv installs from here
```

---

## 1 · Prerequisites

| Requirement | Version |
| ----------- | ------- |
| **Python**  | ≥ 3.12  |
| **uv**      | ≥ 0.1   |

Install **uv** once (if you haven’t yet):

```bash
pipx install uv   # or: pip install uv
```

---

## 2 · Environment Variables

Create a file named **`.env`** in the project root and paste:

```dotenv
# <Smithery>
SMITHERY_API_KEY=YOUR_SMITHERY_API_KEY
SMITHERY_PROFILE=YOUR_SMITHERY_PROFILE

# <Google API key>
GOOGLE_API_KEY1=Your_GOOGLE_API_KEY1
GOOGLE_API_KEY2=Your_GOOGLE_API_KEY2
GOOGLE_API_KEY3=Your_GOOGLE_API_KEY3
GOOGLE_API_KEY4=Your_GOOGLE_API_KEY4

# <FMP>  Visit: https://site.financialmodelingprep.com/
FMP_ACCESS_TOKEN=YOUR_FMP_ACCESS_TOKEN

# Choose Model Backend: 0 → ML Dev, 1 → Vertex
GOOGLE_GENAI_USE_VERTEXAI=0
```

> **Tip →** You can also export the same keys from your shell instead of using a `.env` file.

---

## 3 · Installation (with **uv**)

```bash
# 1) Clone and enter the project
$ git clone https://github.com/<your_org>/financial-research-agent.git
$ cd financial-research-agent

# 2) Create an isolated environment
$ uv venv                 # generates .venv/ under the repo
$ source .venv/bin/activate  # Windows → .venv\Scripts\activate

# 3) Install project dependencies from pyproject.toml
$ uv pip install -e .
```

---

## 4 · Run the Demo Web UI

```bash
# activate env if not already
$ source .venv/bin/activate

# step into source directory and launch
$ cd src
$ adk web
```

`adk web` spins up a local browser UI where you can:

1. Provide a company ticker or name.
2. Watch the **Company Search Agent**, **Financial Research Agent**, and **FOMC Research Agent** run in parallel.
3. Review the synthesised investment recommendation.

---

## 5· Reference – Core Agents

| Agent                                 | Purpose                               | Tools              |
| ------------------------------------- | ------------------------------------- | ------------------ |
| **company\_search\_agent**            | Gathers company & competitor info     | Smithery EXA MCP   |
| **financial\_research\_agent**        | Fetches financial metrics, peer comps | FMP MCP            |
| **fomc\_research\_agent**             | Always pulls latest FOMC meeting data | Custom Fed scraper |
| **investment\_research\_synthesizer** | Merges all findings → final call      | Gemini‑2.5‑pro     |

---

## License

Apache 2.0 © 2025 Jaehun Shon
