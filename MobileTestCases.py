import asyncio
import logging
import pytest
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use.agent.service import Agent

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Define multiple test tasks as strings
tasks = [
    (
        '1. Open the URL "https://app.testsigma.com/ui/" in browser'
        '2. Enter the username "sigma@qateam.com" in the username field'
        '3. Enter the password "Testsigma@123" in the password field'
        '4. Click on the "Sign In" or "Login" button to log into the Testsigma application'
        '5. Wait for 5 seconds for the page to load'
        '6. Go to url https://app.testsigma.com/ui/td/184/cases/filters/881'
        '7. Click on record button'
        '8. Wait for 4 seconds'
        '9. Click on version dropdown and select Android 13 value in it'
        '10. Click on device dropdown and select samsung s23 ultra in it'
        '11. Click on record button again'
        '12. Wait for 20 seconds'
        '13. Click on add new step'
        '14. Verify STOP button should be present in the mobile editor in right side panel'
    ),
    (
        '1. Open the URL "https://google.com" in browser'
        '2. Enter the Automation in search field'
        '3. hit enter button'
    ),
]

# Function to run a task
async def run_task(task):
    llm = ChatGoogleGenerativeAI(
        model='gemini-2.0-flash',
        api_key='AIzaSyAhm6Gl0foNqps1PLo9WdC8WIQdhbjUb84'
    )
    logger.info("Running the automation task...")

    # Create the agent and run the task
    agent = Agent(task, llm, use_vision=True)
    history = await agent.run()

    # Get the final result and success status of the task
    test_result = history.final_result()
    test_result1 = history.is_successful()

    return test_result1

# Test case 1
@pytest.mark.asyncio
async def test_case_1():
    task = tasks[0]  # Use the first task in the list
    test_result1 = await run_task(task)
    print('Actual Value ------> '+str(test_result1))
    assert str(test_result1) == "True"


# Test case 2
@pytest.mark.asyncio
async def test_case_2():
    task = tasks[1]  # Use the second task in the list
    test_result1 = await run_task(task)
    assert str(test_result1) == "True"
