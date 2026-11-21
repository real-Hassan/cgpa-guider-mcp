# agent/main.py
import asyncio
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from agent import build_agent, MCP_URL

DB_PATH = "chat_memory.sqlite"


async def list_threads(memory) -> list[str]:
    """Return all distinct thread_ids saved in the SQLite checkpointer."""
    async with memory.conn.execute(
        "SELECT DISTINCT thread_id FROM checkpoints"
    ) as cursor:
        rows = await cursor.fetchall()
    return [row[0] for row in rows]

async def show_history(app, config) -> None:
    """Fetch and pretty-print the saved message history for the current thread."""
    state = await app.aget_state(config)
    messages = state.values.get("messages", [])
    if not messages:
        print("(no history yet)")
        return

    print("\n--- Chat History ---")
    for msg in messages:
        role = msg.type.upper()
        content = getattr(msg, "text", None) or msg.content
        if content:
            print(f"[{role}]: {content}")
    print("--------------------\n")

async def repair_orphaned_tool_calls(app, config) -> bool:
    """If the last saved message is an AIMessage with unanswered tool_calls,
    inject synthetic ToolMessages so Groq won't reject the thread."""
    state = await app.aget_state(config)
    messages = state.values.get("messages", [])
    if not messages:
        return False

    last_msg = messages[-1]
    if isinstance(last_msg, AIMessage) and last_msg.tool_calls:
        patch = [
            ToolMessage(
                tool_call_id=tc["id"],
                name=tc["name"],
                content="Error: The MCP tool server is currently down or unreachable. Tell the user you cannot run calculations right now.",
            )
            for tc in last_msg.tool_calls
        ]
        # as_node="tools" tells LangGraph the tools node finished, so the model runs next
        await app.aupdate_state(config, {"messages": patch}, as_node="tools")
        return True
    return False

async def main():
    async with AsyncSqliteSaver.from_conn_string(DB_PATH) as memory:
        await memory.setup()
        app = await build_agent(checkpointer=memory)

        existing = await list_threads(memory)
        print("Saved chats:", existing or "(none yet)")
        name = input("Who's chatting? ").strip()
        config = {"configurable": {"thread_id": name}}
        await repair_orphaned_tool_calls(app, config)

        while True:
            user_input = input(f"[{name}] > ").strip()
            if not user_input: 
                continue
            if user_input == "/switch":
                name = input("Who's chatting? ").strip()
                config = {"configurable": {"thread_id": name}}
                await repair_orphaned_tool_calls(app, config)
                continue
            if user_input == "/history":
                await show_history(app, config)
                continue
            if user_input == "/forget":
                await memory.adelete_thread(name)
                print(f"Forgot {name}'s history.")
                continue
            if user_input in ("/exit", "/quit"):
                break

            # result = await app.ainvoke(
            #     {"messages": [HumanMessage(user_input)]}, config
            # )
            # print(result["messages"][-1].text)

            try:
                async for chunk in app.astream(
                    {"messages": [HumanMessage(user_input)]},
                    config,
                    stream_mode=["updates", "messages"],
                ):
                    kind, data = chunk
                    if kind == "messages":
                        token, metadata = data
                        if metadata.get("langgraph_node") == "model" and token.text:
                            print(token.text, end="", flush=True)
                    else:  # "updates"
                        for node, update in data.items():
                            pass  # optional: show "[calling tool: X]" here while waiting
                print()
            except Exception as e:
                print(f"\n[Server error: {e}]")
                if await repair_orphaned_tool_calls(app, config):
                    async for chunk in app.astream(
                        None,
                        config,
                        stream_mode=["updates", "messages"],
                    ):
                        kind, data = chunk
                        if kind == "messages":
                            token, metadata = data
                            if metadata.get("langgraph_node") == "model" and token.text:
                                print(token.text, end="", flush=True)
                    print()

if __name__ == "__main__":
    asyncio.run(main())
