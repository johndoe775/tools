
from research.state import GraphState
from pandas_visualizer.main import pandas_vis_tool

if __name__ == "__main__":
    example_state = GraphState(inputs="Show average sales by category as a bar chart.", messages=[])
    pandas_vis_tool(example_state, execute=False)
