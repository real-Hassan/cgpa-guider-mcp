```markdown
# CGPA Guider — MCP Server & Academic Advising Agent

**Student:** Muhammad Hassan Farooq (`BCSF24A025`)  
**Course:** Artificial Intelligence — Assignment 3  
**GitHub Repository:** [https://github.com/real-Hassan/cgpa-guider-mcp](https://github.com/real-Hassan/cgpa-guider-mcp)

An AI-powered academic advising assistant for PUCIT (BSCS) students, built with **FastMCP**, **LangChain**, **Groq**, and **SQLite** persistent memory. The tool server is hosted on **Prefect Horizon**, and the local CLI agent connects to it over Streamable HTTP with token-by-token streaming, multi-thread memory, and graceful error recovery.

---

## Live Deployment Details

* **MCP Server URL:** `https://cgpa-guider-mcp.fastmcp.app/mcp`
* **Hosting Platform:** Prefect Horizon (Private Endpoint)
* **FastMCP API Key:** `fmcp_q2RWBhrWHa2_oy5WpkMPqk4E5bGTbhVz7l46LTSZfdc`

Verify the live server and list all 7 tools from your terminal:

```bash
fastmcp list [https://cgpa-guider-mcp.fastmcp.app/mcp](https://cgpa-guider-mcp.fastmcp.app/mcp) --auth fmcp_q2RWBhrWHa2_oy5WpkMPqk4E5bGTbhVz7l46LTSZfdc

```

---

## Project Structure

```text
BCSF24A025_Assignment3/
├── agent/
│   ├── agent.py          # MCPAdapter client & LangChain agent builder
│   ├── llm.py            # Groq LLM configuration
│   ├── main.py           # CLI loop, streaming, memory commands & error recovery
│   └── .env.example      # Environment variable template
├── server/
│   ├── server.py         # FastMCP HTTP server entrypoint (server/server.py:mcp)
│   ├── tools.py          # 7 PUCIT GPA/CGPA & course lookup tools
│   └── requirements.txt  # Server-only dependencies for Prefect Horizon
├── requirements.txt      # Full project dependencies
├── .gitignore
└── README.md

```

---

## Available MCP Tools (7)

1. `marks_to_grade_points(marks)` — Converts raw course marks into GPA grade points.
2. `calculate_semester_gpa(grade_points, credit_hours)` — Computes a single semester's GPA.
3. `calculate_new_cgpa(current_cgpa, completed_credit_hours, semester_gpa, semester_credit_hours)` — Computes updated cumulative GPA.
4. `required_gpa_for_target(target_cgpa, current_cgpa, completed_credit_hours, remaining_credit_hours)` — Calculates the average GPA required over remaining credits to hit a target CGPA.
5. `get_semester_courses(semester)` — Returns PUCIT BSCS courses, codes, and credit hours for semesters 1–8.
6. `get_remaining_credit_hours(start_semester, end_semester)` — Calculates total credit hours across a semester range.
7. `save_report(filename, content)` — Saves a formatted advising report to disk.

---

## Setup & Running Locally

### 1. Create a virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

```

### 2. Configure environment variables

Copy `agent/.env.example` to `agent/.env` and fill in your keys:

```env
GROQ_API_KEY=your_groq_api_key_here
MCP_URL=[https://cgpa-guider-mcp.fastmcp.app/mcp](https://cgpa-guider-mcp.fastmcp.app/mcp)
FASTMCP_KEY=fmcp_q2RWBhrWHa2_oy5WpkMPqk4E5bGTbhVz7l46LTSZfdc

```

### 3. Run the Agent

```bash
python agent/main.py

```

*(No local server is needed—the agent connects directly to the hosted Prefect Horizon endpoint.)*

---

## CLI Features & Commands

* **Token Streaming:** Responses stream live to the terminal as they are generated.
* **Persistent Memory:** Conversations are stored per user/thread in `chat_memory.sqlite`.
* **Graceful Error Recovery:** If the MCP server is unreachable mid-conversation, the agent catches the failure, patches orphaned tool calls, and keeps the session usable.

| Command | Action |
| --- | --- |
| `/history` | Display the current thread's conversation history |
| `/switch` | Switch to another saved or new chat thread |
| `/forget` | Delete the current thread's saved memory |
| `/exit` | Quit the application |

