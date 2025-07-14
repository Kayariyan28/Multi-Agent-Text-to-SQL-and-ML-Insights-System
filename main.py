import os
import argparse
from src.graph import build_graph
from src.utils import get_table_schema, bq_client
from src.agents import AgentState

def run_analysis(question: str, graph):
    table_schema = get_table_schema(bq_client, os.environ['BQ_DATASET'], os.environ['BQ_TABLE'])
    if "Error" in table_schema:
        print(table_schema)
        return

    initial_state = {"question": question, "schema": table_schema}
    final_state = graph.invoke(initial_state)

    print("\n" + "="*60)
    print("          FINAL BUSINESS INSIGHT & RECOMMENDATIONS")
    print("="*60 + "\n")
    print(final_state.get('insight', 'No insight generated.'))
    print("\n" + "="*60)

    if final_state.get('error'):
        print(f"\nError: {final_state['error']}")

    return final_state

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run business analysis.")
    parser.add_argument("--question", type=str, required=True, help="Business question to analyze.")
    args = parser.parse_args()

    graph = build_graph()
    run_analysis(args.question, graph)
