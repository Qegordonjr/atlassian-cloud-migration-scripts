import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

# Replace these variables with your Confluence Cloud information
username = 'your-email@example.com'
api_token = 'your-api-token'
base_url = 'https://your-domain.atlassian.net/wiki'

# API endpoint to retrieve spaces
spaces_endpoint = f'{base_url}/rest/api/space'

# Function to get all spaces of a specific type
def get_spaces(username, api_token, space_type):
    spaces = []
    start = 0
    limit = 50
    while True:
        response = requests.get(
            spaces_endpoint,
            auth=HTTPBasicAuth(username, api_token),
            params={'start': start, 'limit': limit, 'type': space_type}
        )
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        spaces.extend(data['results'])
        if 'next' not in data['_links']:
            break
        start += limit
    return spaces

# Retrieve global spaces
global_spaces = get_spaces(username, api_token, 'global')
global_space_data = [{'key': space['key'], 'name': space['name'], 'type': space['type']} for space in global_spaces]

# Retrieve personal spaces
personal_spaces = get_spaces(username, api_token, 'personal')
personal_space_data = [{'key': space['key'], 'name': space['name'], 'type': space['type']} for space in personal_spaces]

# Create DataFrames and save to CSV
df_global = pd.DataFrame(global_space_data)
df_global.to_csv('confluence_global_spaces.csv', index=False)

df_personal = pd.DataFrame(personal_space_data)
df_personal.to_csv('confluence_personal_spaces.csv', index=False)

print('CSV files "confluence_global_spaces.csv" and "confluence_personal_spaces.csv" have been created successfully.')
