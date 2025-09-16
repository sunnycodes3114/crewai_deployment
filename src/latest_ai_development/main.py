#!/usr/bin/env python
import sys
import warnings

from latest_ai_development.crew import LatestAiDevelopment

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'AI LLMs',
        'chat_id': "59611922-0a6e-438e-bf30-2eba03a0efd5",
        'bot_user_id': "7109d6a8-1799-4c45-b22e-45e1baba3e26"
    }
    visible_dict = {k: v for k, v in inputs.items() if k == 'topic'}
    hidden_dict = {k: v for k, v in inputs.items() if k != 'topic'}
    crew = LatestAiDevelopment(hidden_dict).crew()
    result = crew.kickoff(inputs=visible_dict)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        LatestAiDevelopment().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        LatestAiDevelopment().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        LatestAiDevelopment().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
