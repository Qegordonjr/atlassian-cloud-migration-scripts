import requests
import csv

# Configuration
site1 = {
    'url': 'https://site1.atlassian.net/wiki/rest/api',
    'username': 'username1',
    'api_token': 'api_token1'
}

site2 = {
    'url': 'https://site2.atlassian.net/wiki/rest/api',
    'username': 'username2',
    'api_token': 'api_token2'
}

# Function to get spaces from a Confluence site
def get_spaces(site):
    auth = (site['username'], site['api_token'])
    url = f"{site['url']}/space?type=global&limit=1000"
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    spaces = response.json().get('results', [])
    return {space['key']: space['name'] for space in spaces}

# Function to write spaces to a CSV file
def write_spaces_to_csv(spaces, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Space Key', 'Space Name'])
        for key, name in spaces.items():
            writer.writerow([key, name])

# Function to compare spaces and write matches to a CSV file
def compare_spaces_and_write_matches(spaces1, spaces2, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Space Key', 'Space Name Site 1', 'Space Name Site 2'])
        for key in spaces1.keys() & spaces2.keys():
            writer.writerow([key, spaces1[key], spaces2[key]])

# Main script
spaces1 = get_spaces(site1)
spaces2 = get_spaces(site2)

write_spaces_to_csv(spaces1, 'site1_spaces.csv')
write_spaces_to_csv(spaces2, 'site2_spaces.csv')
compare_spaces_and_write_matches(spaces1, spaces2, 'matching_spaces.csv')

print("CSVs generated successfully.")
