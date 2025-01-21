import os
from typing import Dict, Any
from crewai import Crew

def execute_crew(crew: Crew) -> Dict[str, Any]:
    """
    Execute a CrewAI workflow and return the results in a structured format.
    
    Args:
        crew (Crew): An initialized CrewAI Crew instance with agents and tasks
    
    Returns:
        Dict[str, Any]: {
            "status": "success" or "error",
            "response": raw result string,
            "prompt": formatted string of all task outputs
        }
    """
    try:
        # Execute the crew's tasks
        result = crew.kickoff()
        
        # Format task outputs into a single string
        task_outputs = []
        for task_output in crew.tasks:
            task_str = (
                f"Description: {task_output.description}\n"
                f"Expected_output: {task_output.expected_output}\n"
                "---"
            )
            task_outputs.append(task_str)
        
        formatted_prompt = "\n\n".join(task_outputs)
        
        return {
            "status": "success",
            "response": result,
            "prompt": formatted_prompt
        }
        
    except Exception as e:
        # Handle any errors during execution
        return {
            "status": "error",
            "error": str(e),
            "error_type": type(e).__name__
        }