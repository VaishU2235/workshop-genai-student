# workshop-genai-student
Student's version of project

Student's version of the GenAI Workshop Competition project. This repository contains the tools and infrastructure needed to participate in the competition using CrewAI and Claude.

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Anthropic API key for Claude

### Setup

1. Clone this repository
2. Create a `.env` file with your credentials:
    ```
    ANTHROPIC_API_KEY=<your_anthropic_api_key>
    ```
3. Run the Docker Compose setup:
    ```
    docker-compose up -d
    ```
4. Access the JupyterLab environment at `http://localhost:8888`.

### Using JupyterLab

Access JupyterLab at http://localhost:8888. The notebook environment is pre-configured with all required dependencies.

## Creating Submissions

### Example Notebook (Agent.ipynb)

Create a new notebook in the `notebooks` directory. Here's a basic template:

Create your agent
agent = Agent(
role="Expert Analyst",
goal="Provide insightful analysis",
backstory="Experienced data analyst with expertise in market research",
llm=claude
)
Define your task
task = Task(
description="Analyze the given market data and provide recommendations",
agent=agent
)
Create the crew
crew = Crew(
agents=[agent],
tasks=[task],
verbose=True
)
Submit your response
result = submit_crew_response(
crew=crew,
team_name="your_team_name",
password="your_password"
)
print(result)




### Submission Process

The submission system includes:
1. Rate limiting (5 minutes between submissions)
2. Authentication with team credentials
3. Automatic formatting of prompts and responses

### Key Components

#### SubmissionClient
- Handles authentication
- Manages rate limiting
- Executes CrewAI workflows
- Submits results to the competition backend

#### Rate Limiting
- One submission every 5 minutes
- System tracks your last submission time
- Provides feedback on waiting time if needed

### Best Practices

1. **Development**:
   - Use separate notebooks for experimentation
   - Test your agents and tasks before submission
   - Keep track of successful prompts

2. **Submission**:
   - Verify your team credentials
   - Check the rate limit before submitting
   - Monitor the response status

3. **Error Handling**:
   - Check submission status in the result
   - Look for error messages if submission fails
   - Verify your API key is set correctly




## Troubleshooting

1. **Authentication Issues**:
   - Verify team credentials
   - Check if backend service is running

2. **Rate Limiting**:
   - Wait 5 minutes between submissions
   - Check your last submission time

3. **API Key Issues**:
   - Verify ANTHROPIC_API_KEY in .env
   - Restart services after updating .env

## Support

For issues or questions:
1. Check the error message in the response
2. Verify your setup matches the documentation
3. Contact the workshop organizers for assistance

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.

