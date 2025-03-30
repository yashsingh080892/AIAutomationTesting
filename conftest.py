import requests
import pytest

# Google Chat Webhook URL (replace with your actual webhook URL)
WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/AAAAznSM5qI/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=1JwGPUhtm-r_8bdpveyrjrcQkiDylhlOL3655L61khs"

# List to store the test case summaries
test_summary = []

# Capture detailed test results
def pytest_runtest_makereport(item, call):
    """Hook to capture individual test case results."""
    if call.when == "call":  # Only capture the results after the test is run
        test_name = item.nodeid
        test_status = "PASSED" if call.excinfo is None else "FAILED"
        duration = call.stop - call.start
        test_summary.append({
            "name": test_name,
            "status": test_status,
            "duration": round(duration, 2)  # Round the duration for easier reading
        })

# Capture the overall test summary and send it to Google Chat after the test session finishes
def pytest_sessionfinish(session, exitstatus):
    total_tests = len(test_summary)
    passed_tests = sum(1 for test in test_summary if test["status"] == "PASSED")
    failed_tests = total_tests - passed_tests
    total_duration = sum(test["duration"] for test in test_summary)

    # Prepare a detailed summary message
    message = f"Test Summary Report:\n"
    message += f"Total Tests: {total_tests}\n"
    message += f"Passed Tests: {passed_tests}\n"
    message += f"Failed Tests: {failed_tests}\n"
    message += f"Total Duration: {total_duration:.2f} seconds\n\n"

    # Add individual test case details
    message += "Individual Test Results:\n"
    for test in test_summary:
        message += f"Test Name: {test['name']}, Status: {test['status']}, Duration: {test['duration']} seconds\n"

    # Send the summary message to Google Chat
    send_to_google_chat(message)

# Function to send message to Google Chat
def send_to_google_chat(message):
    headers = {
        'Content-Type': 'application/json'
    }

    # Create the message payload
    payload = {
        "text": message
    }

    # Send the request to Google Chat webhook
    response = requests.post(WEBHOOK_URL, json=payload, headers=headers)

    # Log the result of the request
    if response.status_code == 200:
        print("Successfully sent message to Google Chat.")
    else:
        print(f"Failed to send message to Google Chat. Status code: {response.status_code}")