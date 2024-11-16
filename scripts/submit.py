import requests
import pandas as pd
import json

def get_positions(pos_dict):
    """
    Validates and normalizes positions to ensure they meet portfolio constraints.

    Args:
        pos_dict (dict): Portfolio allocations.

    Returns:
        pd.Series: Normalized and validated portfolio allocations.
    """
    pos = pd.Series(pos_dict)
    pos = pos.replace([float('inf'), -float('inf')], pd.NA)
    pos = pos.dropna()
    pos = pos / pos.abs().sum()
    pos = pos.clip(-0.1, 0.1)
    if pos.abs().max() / pos.abs().sum() > 0.1:
        raise ValueError(f"Portfolio too concentrated {pos.abs().max()=} / {pos.abs().sum()=}")
    return pos

def get_submission_dict(pos_dict, your_team_name: str, your_team_passcode: str):
    """
    Prepares the submission dictionary with portfolio allocations, team name, and passcode.

    Args:
        pos_dict (dict): Portfolio allocations.
        your_team_name (str): Your team name.
        your_team_passcode (str): Submission passcode.

    Returns:
        dict: Submission dictionary.
    """
    return {
        **get_positions(pos_dict).to_dict(),
        **{
            "team_name": your_team_name,
            "passcode": your_team_passcode,
        },
    }

def submit_to_google_form(submission, form_url):
    """
    Submits the portfolio allocations to a Google Form.

    Args:
        submission (dict): Submission dictionary.
        form_url (str): Google Form submission URL.
    """
    # Convert the submission to a JSON string
    json_submission = json.dumps(submission)

    # Map the JSON submission to the form field
    form_data = {
        "entry.1234567890": "true",  # Replace with the email toggle field ID
        "entry.0987654321": json_submission,  # Replace with the allocations field ID
    }

    # Submit the form
    response = requests.post(form_url, data=form_data)

    if response.status_code == 200:
        print("Form submitted successfully!")
    else:
        print(f"Failed to submit form. Status code: {response.status_code}")
        print(response.text)




