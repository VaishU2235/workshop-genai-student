import os
import requests
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
import logging
from crewai import Crew
from langchain_anthropic import ChatAnthropic

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Claude model
claude = ChatAnthropic(
    anthropic_api_key=os.getenv('ANTHROPIC_API_KEY'),
    model="claude-3-sonnet-20240229",
    temperature=0.7
)

class SubmissionClient:
    def __init__(self, base_url: str = "http://backend:8000"):
        self.base_url = base_url
        self.token = None
        self.headers = {"Content-Type": "application/json"}

    def login(self, team_name: str, password: str) -> bool:
        """Login and get access token"""
        try:
            response = requests.post(
                f"{self.base_url}/api/teams/login",
                json={"team_name": team_name, "password": password},
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()
            self.token = data["access_token"]
            self.headers["Authorization"] = f"Bearer {self.token}"
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Login failed: {str(e)}")
            return False

    def get_latest_submission_time(self) -> Optional[datetime]:
        """Get the datetime of the latest submission"""
        try:
            response = requests.get(
                f"{self.base_url}/api/submissions/mine",
                headers=self.headers
            )
            response.raise_for_status()
            submissions = response.json()
            
            if not submissions:
                return None
                
            # Submissions are ordered by submitted_at desc
            latest = submissions[0]
            return datetime.fromisoformat(latest["submitted_at"])
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get submissions: {str(e)}")
            return None

    def execute_crew(self, crew: Crew) -> Dict[str, Any]:
        """Execute CrewAI workflow and return results"""
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
            return {
                "status": "error",
                "error": str(e),
                "error_type": type(e).__name__
            }

    def submit(self, crew: Crew) -> Dict:
        """Execute crew and submit results with rate limiting"""
        try:
            # Step 1: Check rate limit
            latest_time = self.get_latest_submission_time()
            
            if latest_time:
                time_since_last = datetime.utcnow() - latest_time.replace(tzinfo=None)
                if time_since_last < timedelta(minutes=5):
                    return {
                        "status": "failure",
                        "reason": f"Rate limit: Must wait {5 - time_since_last.seconds // 60} minutes before next submission"
                    }

            # Step 2: Execute crew
            crew_result = self.execute_crew(crew)
            if crew_result["status"] != "success":
                return crew_result

            # Step 3: Submit results
            submission_data = {
                "prompt": crew_result["prompt"],
                "response": crew_result["response"],
                "table_metadata": {
                    "timestamp": datetime.utcnow().isoformat(),
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/submissions",
                json=submission_data,
                headers=self.headers
            )
            response.raise_for_status()
            
            return {
                "status": "success",
                "data": response.json()
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "status": "failure",
                "reason": f"Submission failed: {str(e)}"
            }

def submit_crew_response(crew: Crew, team_name: str, password: str) -> Dict:
    """Main function to handle the complete submission process"""
    client = SubmissionClient()
    
    # Step 1: Login
    if not client.login(team_name, password):
        return {
            "status": "failure",
            "reason": "Login failed"
        }
    
    # Step 2: Submit crew results with rate limiting
    return client.submit(crew)

# Example usage
if __name__ == "__main__":
    from crewai import Agent, Task
    
    # Example agent and task
    agent = Agent(
        role="Writer",
        goal="Write a story",
        backstory="Expert storyteller",
        llm=claude
    )
    
    task = Task(
        description="Write a short story about AI",
        agent=agent
    )
    
    # Create crew
    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True
    )
    
    # Submit crew response
    result = submit_crew_response(
        crew=crew,
        team_name="team_alpha",
        password="password123!"
    )
    
    print(result) 