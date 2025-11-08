import io
import os
import pandas as pd
from pandasql import sqldf
from langchain_core.prompts import PromptTemplate
from research.helpers import LLM
from research.state import GraphState

# ======================================================
#  DataLoader
# ======================================================
class DataLoader:
    @staticmethod
    def capture_df_info(df: pd.DataFrame) -> str:
        buffer = io.StringIO()
        df.info(buf=buffer)
        return buffer.getvalue()

    @staticmethod
    def load_dataframes(csv_dir: str):
        paths, df_infos, globals_dict = {}, {}, {}
        for fname in os.listdir(csv_dir):
            if fname.lower().endswith(".csv"):
                name = os.path.splitext(fname)[0]
                path = os.path.join(csv_dir, fname)
                df = pd.read_csv(path)
                paths[name] = path
                df_infos[name] = DataLoader.capture_df_info(df)
                globals_dict[name] = df.copy()
        return paths, df_infos, globals_dict


# ======================================================
#  SQLGenerator (using | instead of LLMChain)
# ======================================================
class SQLGenerator:
    def __init__(self):
        self.llm = LLM().llm

        # Prompt template describing the task
        self.prompt = PromptTemplate(
            input_variables=["df_infos", "question"],
            template=(
                "You are an expert in SQL-based data analysis. "
                "The user has these tables (with schema info shown) and wants to answer a question using SQL (SQLite syntax).\n\n"
                "### Rules:\n"
                "1) Use only provided table names and columns.\n"
                "2) JOIN explicitly if needed.\n"
                "3) Output ONLY the SQL query (no backticks or comments).\n\n"
                "### Tables Info:\n{df_infos}\n\n"
                "### Question:\n{question}\n\n"
                "### SQL Query:\n"
            ),
        )

        # Build the LCEL chain (Prompt → LLM → output parser)
        self.chain = self.prompt | self.llm

    def generate(self, df_infos: dict, question: str) -> str:
        """Generate SQL query using LCEL pipeline."""
        response = self.chain.invoke({"df_infos": df_infos, "question": question})
        return response.content.strip()


# ======================================================
#  SQLExecutor
# ======================================================
class SQLExecutor:
    @staticmethod
    def execute(sql_query: str, global_vars: dict) -> pd.DataFrame:
        try:
            pysqldf = lambda q: sqldf(q, global_vars)
            result_df = pysqldf(sql_query)
            print("✅ Query executed successfully.\n")
            print(result_df)
            return result_df
        except Exception as e:
            print(f"❌ Error executing query: {e}")
            return pd.DataFrame()


# ======================================================
#  Main Tool Function
# ======================================================
def pandasql_tool(state: GraphState, execute: bool = True):
    csv_dir = "content"
    print("📂 Loading CSV files...")
    paths, df_infos, global_vars = DataLoader.load_dataframes(csv_dir)

    for name, info in df_infos.items():
        print(f"\n--- Schema for {name} ---")
        print(info)

    question = state.get("inputs", "").strip()
    if not question:
        print("⚠️ No question provided. Exiting.")
        return state

    print("\n🧠 Generating SQL query using LCEL...")
    sql_generator = SQLGenerator()
    sql_query = sql_generator.generate(df_infos, question)

    print("\n===== 📝 Generated SQL Query =====\n")
    print(sql_query)

    result_df = None
    if execute:
        print("\n🚀 Executing SQL query...")
        result_df = SQLExecutor.execute(sql_query, global_vars)
    else:
        print("\n⚙️ Execution skipped — returning only SQL query.")

    state["messages"].append("✅ Completed pandasql analysis")
    state["sql_query"] = sql_query
    state["outputs"] = result_df if execute else None

    return state
