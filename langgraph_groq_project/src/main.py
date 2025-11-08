from research.state import GraphState
from research.tools.pandasql_tool import pandasql_tool

if __name__ == "__main__":
    state = GraphState(
        messages=[],
        inputs="List total revenue per region",
        choice="sql_analysis",
        answer="",
        tool_choice="pandasql_tool",
    )

    updated_state = pandasql_tool(state, execute=False)
    print("\n✅ Final State:\n", updated_state)
