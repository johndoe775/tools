
from langchain_core.prompts import PromptTemplate
from research.helpers import LLM

class PandasVisGenerator:
    """Generates Seaborn/Matplotlib visualization code using LLM."""

    def __init__(self):
        self.llm = LLM().llm
        self.prompt = PromptTemplate(
            input_variables=["df_infos", "purpose"],
            template=(
                'You are a data analysis expert. The user has these dataframes (with info shown) '
                'and wants to achieve a given analysis purpose.\n\n'
                '### Instructions:\n'
                '*** use name from df_info dictionary to create a dataframe using paths["name"] to access the path\n'
                '1) Do NOT tamper with original dataframes; use df.copy() if needed.\n'
                '2) Always reference df.info() to confirm column names and dtypes.\n'
                '3) Do NOT hallucinate column names: only use those present.\n'
                '4) Recommend the single best chart or minimal set of charts.\n'
                '5) If merging is needed, do it within the sns call.\n'
                '6) Do all data calculations on separate lines before plotting.\n'
                '7) Output ONLY the Python code lines (no comments, no narrative, no preamble, and do not mention the language).\n\n'
                '### DataFrames Info:\n{df_infos}\n\n'
                '### Purpose of Analysis:\n{purpose}\n\n'
                '### Example output code:\n\n'
                'import pandas\nimport numpy\n\ndf.info()'
            ),
        )
        self.chain = self.prompt | self.llm

    def generate(self, df_infos: dict, purpose: str) -> str:
        response = self.chain.invoke({"df_infos": df_infos, "purpose": purpose})
        return response.content.strip()
