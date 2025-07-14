# Multi-Agent-Text-to-SQL-and-ML-Insights-System
This GitHub repository organizes the multi-agent system built with LangGraph for advanced text-to-SQL.
# Multi-Agent Text-to-SQL and ML Insights System

## Overview
This repository implements a multi-agent system using LangGraph for converting natural language business questions into advanced SQL queries or ML tasks on BigQuery datasets. It supports RAG for schema awareness and executes via BigQuery or SparkML for insights. Agents are specialized:
- Planner (OpenAI o1-preview): Determines task type (SQL/ML) and creates plans.
- Coder (Gemini 1.5 Pro): Generates SQL or PySpark code.
- Reviewer (xAI Grok): Validates and refines code.
- Analyst (Claude 3.5 Sonnet): Generates McKinsey-level insights.

Built for detailed analysis, e.g., sales trends or predictive modeling.

## Setup
1. Clone the repo: `git clone https://github.com/your-username/multi-agent-insights.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up Spark (for ML tasks):
   - Download Spark 3.5.1: https://spark.apache.org/downloads.html
   - Set environment variables: `export SPARK_HOME=/path/to/spark` and `export JAVA_HOME=/path/to/java`
   - Install BigQuery connector JAR if needed.
4. Copy `.env.example` to `.env` and fill in:
   - GOOGLE_API_KEY=your-key
   - OPENAI_API_KEY=your-key
   - ANTHROPIC_API_KEY=your-key
   - XAI_API_KEY=your-key
   - GOOGLE_CLOUD_PROJECT=your-project-id
   - BQ_DATASET=your-dataset
   - BQ_TABLE=your-table
   - LOCATION=US
5. Authenticate with GCP: `gcloud auth application-default login`

## Usage
Run from CLI: `python main.py --question "Your business question here"`
Or use notebooks/demo.ipynb for interactive examples.

## Contributing
Fork and PR. Issues welcome.

## License
MIT
