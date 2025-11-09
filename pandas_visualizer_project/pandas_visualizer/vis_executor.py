
import os
import time
import matplotlib.pyplot as plt

class PandasVisExecutor:
    """Executes generated visualization code and saves the result."""

    @staticmethod
    def execute(code: str, global_vars: dict, save_dir: str = "plots"):
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, f"visualization_{int(time.time())}.png")

        try:
            print("✅ Executing visualization code...")
            exec(code, global_vars)
            plt.savefig(save_path, bbox_inches="tight")
            plt.show()
            print(f"💾 Saved plot to {save_path}")
            return save_path
        except Exception as e:
            print(f"❌ Error executing visualization code: {e}")
            return None
