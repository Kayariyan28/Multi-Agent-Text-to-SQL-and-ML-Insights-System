# Multi-Agent-Text-to-SQL-and-ML-Insights-System
This GitHub repository organizes the multi-agent system built with LangGraph for advanced text-to-SQL.
multi-agent-insights/
├── README.md               # Project overview, setup, and usage instructions
├── LICENSE                 # MIT License
├── requirements.txt        # Python dependencies
├── .gitignore              # Standard Python ignores (e.g., __pycache__, .env)
├── .env.example            # Template for environment variables (API keys, GCP project)
├── src/                    # Core Python modules
│   ├── __init__.py
│   ├── agents.py           # Agent definitions (planning, generation, reviewing, analysis)
│   ├── utils.py            # Helper functions (schema retrieval, query/code execution)
│   └── graph.py            # Graph building, routers, and execution nodes
├── main.py                 # Entry point for running analysis
└── notebooks/              # Jupyter notebooks for demos
    └── demo.ipynb          # Example usage with business questions
