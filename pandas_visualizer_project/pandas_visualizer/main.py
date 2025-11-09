
import os
import time
from pandas_visualizer.data_loader import DataLoader
from pandas_visualizer.vis_generator import PandasVisGenerator
from pandas_visualizer.vis_executor import PandasVisExecutor
from research.state import GraphState

def ensure_folders():
    for folder in ["data", "plots", "logs"]:
        os.makedirs(folder, exist_ok=True)

def pandas_vis_tool(state: GraphState, execute: bool = True):
    base_dir = "pandas_visualizer_project"
    data_dir = os.path.join(base_dir, "data")
    plots_dir = os.path.join(base_dir, "plots")
    logs_dir = os.path.join(base_dir, "logs")

    ensure_folders()
    paths, df_infos, global_vars = DataLoader.load_dataframes(data_dir)

    if not df_infos:
        print("⚠️ No data found.")
        return state

    purpose = state.get("inputs", "").strip()
    if not purpose:
        print("⚠️ No analysis purpose provided.")
        return state

    print("🎨 Generating visualization code...")
    generator = PandasVisGenerator()
    vis_code = generator.generate(df_infos, purpose)

    print("\n===== Generated Visualization Code =====\n")
    print(vis_code)

    save_path = None
    if execute:
        print("\n🚀 Executing visualization...")
        save_path = PandasVisExecutor.execute(vis_code, global_vars, plots_dir)

    log_path = os.path.join(logs_dir, f"log_{int(time.time())}.txt")
    with open(log_path, "w") as f:
        f.write(purpose + "\n\n" + vis_code + "\n")
        if save_path:
            f.write(f"Saved Plot: {save_path}\n")

    state["vis_code"] = vis_code
    state["plot_path"] = save_path
    state["log_path"] = log_path
    state["messages"].append("✅ Visualization completed.")

    return state
