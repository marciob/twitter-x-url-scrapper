import requests
from bs4 import BeautifulSoup
import json

def extract_twitter_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        # Update this line to check for both 'twitter.com' and 'x.com'
        twitter_links = set(link['href'] for link in links if 'twitter.com' in link['href'] or 'x.com' in link['href'])
        return list(twitter_links)  # Convert the set back to a list
    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return None

def read_websites_from_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data.get('websites', [])

def save_to_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# File paths
input_file = 'websites_list.json'  # JSON file containing the list of websites
output_file_with_twitter = 'twitter_links.json'
output_file_without_twitter = 'no_twitter_links.json'

# Process websites
websites = read_websites_from_file(input_file)
twitter_links = {}
no_twitter_links = []

for url in websites:
    links = extract_twitter_links(url)
    if links:
        twitter_links[url] = links
    else:
        no_twitter_links.append(url)

# Save results to JSON files
save_to_json(output_file_with_twitter, twitter_links)
save_to_json(output_file_without_twitter, no_twitter_links)
