import asyncio
import logging
import pytest  # Make sure pytest is imported

from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use.agent.service import Agent
from openai import max_retries

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Define multiple test tasks as strings
tasks = [
    (
        '1. Open the URL "https://app.testsigma.com/ui/" in browser'
        '2. Enter the username "sigma@qateam.com" in the username field'
        '3. Enter the password "Testsigma@1222" in the password field'
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
        '15. Close browser instance'
    ),
    (
        '1. Open the URL "https://app.testsigma.com/ui/" in browser'
        '2. Enter the username "sigma@qateam.com" in the username field'
        '3. Enter the password "Testsigma@1222" in the password field'
        '4. Click on the "Sign In" or "Login" button to log into the Testsigma application'
        '5. Wait for 5 seconds for the page to load'
        '6. Go to url https://app.testsigma.com/ui/td/184/cases/filters/881'
        '7. Click on record button'
        '8. Wait for 4 seconds'
        '9. Click on version dropdown and select Android 13 value in it'
        '10. Click on device dropdown and select samsung s23 ultra in it'
        '11. Click on record button again'
        '12. Wait for 20 seconds'


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

    attempt = 0
    while attempt <= max_retries:  # We limit retries to 2
        try:
            history = await agent.run()
            # Get the final result and success status of the task
            test_result = history.final_result()
            test_result1 = history.is_successful()
            return test_result, test_result1
        except Exception as e:
            logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
            attempt += 1
            if attempt > max_retries:
                raise  # If we exceed max retries, raise the error
            else:
                logger.info(f"Retrying task {attempt + 1}...")  # Log the retry attempt

# Test case 1
@pytest.mark.asyncio
async def test_case_1(request):  # request fixture is passed here
    task = tasks[0]  # Use the first task in the list
    test_result, test_result1 = await run_task(task)
    print('Final Result ------>' + test_result)
    print('Actual Value ------> ' + str(test_result1))

    # Store test result in the request.node object
    request.node.test_result = test_result  # This stores test_result in node

    assert str(test_result1) == "True"


# Test case 2
@pytest.mark.asyncio
async def test_case_2(request):  # request fixture is passed here
    task = tasks[1]  # Use the second task in the list
    test_result, test_result1 = await run_task(task)
    print('Final Result ------>' + test_result)
    print('Actual Value ------> ' + str(test_result1))

    # Store test result in the request.node object
    request.node.test_result = test_result  # This stores test_result in node

    assert str(test_result1) == "True"
