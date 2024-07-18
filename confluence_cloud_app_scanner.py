import requests
from requests.auth import HTTPBasicAuth
import csv

# Replace these variables with your Confluence Cloud details
CONFLUENCE_URL = 'https://your-confluence-site.atlassian.net/wiki'
USERNAME = 'your-email@example.com'
API_TOKEN = 'your-api-token'

# Define the endpoint for getting the list of installed apps
endpoint = f'{CONFLUENCE_URL}/rest/plugins/1.0/'

# Make the request to the Confluence Cloud API
response = requests.get(endpoint, auth=HTTPBasicAuth(USERNAME, API_TOKEN))

# Check if the request was successful
if response.status_code == 200:
    installed_apps = response.json().get('plugins', [])
    
    # Define the CSV file name
    csv_file = 'user_installed_apps.csv'
    
    # Write the list of user-installed apps to a CSV file
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['App Name', 'Version'])  # Write the header row
        
        for app in installed_apps:
            if app.get('userInstalled'):
                writer.writerow([app.get('name'), app.get('version')])
    
    print(f"List of user-installed apps has been saved to {csv_file}")
else:
    print(f"Failed to retrieve apps. Status code: {response.status_code}, Response: {response.text}")
