
import io
import os
import pandas as pd

class DataLoader:
    """Handles CSV loading and schema extraction."""

    @staticmethod
    def capture_df_info(df: pd.DataFrame) -> str:
        buffer = io.StringIO()
        df.info(buf=buffer)
        return buffer.getvalue()

    @staticmethod
    def load_dataframes(csv_dir: str):
        """Load CSVs from the data directory."""
        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)
            print(f"📁 Created data directory: {csv_dir}")
            print("⚠️ Please add CSV files.")
            return {}, {}, {}

        paths, df_infos, globals_dict = {}, {}, {}
        csv_files = [f for f in os.listdir(csv_dir) if f.lower().endswith(".csv")]

        if not csv_files:
            print(f"⚠️ No CSV files found in {csv_dir}. Please add CSV files.")
            return {}, {}, {}

        for fname in csv_files:
            name = os.path.splitext(fname)[0]
            path = os.path.join(csv_dir, fname)
            df = pd.read_csv(path)
            paths[name] = path
            df_infos[name] = DataLoader.capture_df_info(df)
            globals_dict[name] = df.copy()

        print(f"✅ Loaded {len(paths)} dataframes from {csv_dir}.")
        return paths, df_infos, globals_dict
