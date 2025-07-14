from typing import TypedDict, Optional
import pandas as pd
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
import os

# Initialize LLMs (load from env)
llm_planner = ChatOpenAI(model="o1-preview", temperature=0.0)
llm_coder = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.0, convert_system_message_to_human=True)
llm_reviewer = ChatOpenAI(
    model="grok-beta",
    api_key=os.environ["XAI_API_KEY"],
    base_url="https://api.x.ai/v1",
    temperature=0.0
)
llm_analyst = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0.1)

class AgentState(TypedDict):
    question: str
    schema: str
    task_type: str
    plan: str
    initial_code: str
    refined_code: str
    result_df: pd.DataFrame
    insight: str
    error: Optional[str]

def planning_agent(state: AgentState) -> AgentState:
    print("---AGENT 2: Planner (OpenAI o1-preview)---")
    prompt_template = """
    You are a master strategist and business analyst at McKinsey level. First, analyze the user's question to determine if it can be answered with a standard SQL query or if it requires advanced ML for deeper insights (e.g., prediction, clustering, classification, anomaly detection).

    - Use SQL for data retrieval, aggregation, filtering, joins, etc.
    - Use ML for predictive modeling, pattern discovery, recommendations, etc. You can use SparkML for ML tasks.

    Output format:
    Type: SQL or ML

    Step-by-Step Plan:
    [Detailed steps to answer the question, including required data, calculations, or ML algorithms]

    **Schema:**
    {schema}

    **User Question:**
    {question}
    """
    prompt = PromptTemplate.from_template(prompt_template)
    chain = prompt | llm_planner | StrOutputParser()
    response = chain.invoke({"schema": state['schema'], "question": state['question']})
    
    lines = response.split('\n')
    task_type = lines[0].split(': ')[1].strip().lower()
    plan = '\n'.join(lines[1:]).strip()
    
    print(f"Determined Task Type: {task_type.upper()}")
    print(f"Generated Plan:\n{plan}")
    return {"task_type": task_type, "plan": plan}

def sql_generation_agent(state: AgentState) -> AgentState:
    print("---AGENT 1: SQL Coder (Gemini 1.5 Pro)---")
    prompt_template = """
    You are a Google BigQuery expert. Write a single, advanced BigQuery SQL query to execute the plan. Use CTEs, window functions, etc., for deep analysis.
    **DO NOT** wrap in markdown. Output only the raw SQL query.

    **Schema:** {schema}
    **Plan:** {plan}
    """
    prompt = PromptTemplate.from_template(prompt_template)
    chain = prompt | llm_coder | StrOutputParser()
    code = chain.invoke({"schema": state['schema'], "plan": state['plan']})
    print(f"Generated SQL:\n{code}")
    return {"initial_code": code}

def ml_generation_agent(state: AgentState) -> AgentState:
    print("---AGENT 1: ML Coder (Gemini 1.5 Pro)---")
    prompt_template = """
    You are a SparkML expert. Write PySpark code to execute the ML plan. Read data from BigQuery using spark.read.format("bigquery").options(table=f"{os.environ['GOOGLE_CLOUD_PROJECT']}.{os.environ['BQ_DATASET']}.{os.environ['BQ_TABLE']}").load().
    Use SparkML libraries for modeling. End with: result_df = [final DataFrame with insights]
    Import necessary modules. Assume spark is available.

    **Schema:** {schema}
    **Plan:** {plan}
    """
    prompt = PromptTemplate.from_template(prompt_template)
    chain = prompt | llm_coder | StrOutputParser()
    code = chain.invoke({"schema": state['schema'], "plan": state['plan']})
    print(f"Generated PySpark Code:\n{code}")
    return {"initial_code": code}

def code_reviewing_agent(state: AgentState) -> AgentState:
    print("---AGENT 3: Code Reviewer (xAI Grok)---")
    prompt_template = """
    You are a senior code reviewer. Review the {task_type} code for syntax, logic, and efficiency.
    Verify it implements the question correctly.
    If perfect, output the original code.
    If improvements needed, output the refined code only. No explanations.

    **Question:** {question}
    **Code to Review:** {code}
    """
    prompt = PromptTemplate.from_template(prompt_template)
    chain = prompt | llm_reviewer | StrOutputParser()
    refined_code = chain.invoke({"task_type": state['task_type'].upper(), "question": state['question'], "code": state['initial_code']})
    print(f"Refined Code:\n{refined_code}")
    return {"refined_code": refined_code}

def insight_analyst_agent(state: AgentState) -> AgentState:
    print("---AGENT 4: Insight Analyst (Claude 3.5 Sonnet)---")
    if state['result_df'].empty:
        return {"insight": "No data returned. Cannot generate insights.", "error": "Empty result."}

    result_str = state['result_df'].to_string()
    prompt_template = """
    You are a McKinsey-level business consultant. Synthesize the data into actionable insights for C-suite.
    Focus on implications, "so what?", and recommendations. Use headings and bullets.

    **Question:** {question}
    **Data:** {result}
    """
    prompt = PromptTemplate.from_template(prompt_template)
    chain = prompt | llm_analyst | StrOutputParser()
    insight = chain.invoke({"question": state['question'], "result": result_str})
    print(f"Generated Insight:\n{insight}")
    return {"insight": insight}
