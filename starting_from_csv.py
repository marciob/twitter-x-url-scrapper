import requests
from bs4 import BeautifulSoup
import csv
import time
import os

# Create 'data' directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Function to ensure URLs are well-formed
def format_url(url):
    if not url.startswith('http://') and not url.startswith('https://'):
        return 'https://' + url
    return url

def extract_twitter_links(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(format_url(url), headers=headers, verify=False, timeout=10)  # 10 seconds timeout
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        twitter_links = set(link['href'] for link in links if 'twitter.com' in link['href'] or 'x.com' in link['href'])
        return list(twitter_links)
    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return None

def read_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

def write_csv(file_path, data, fieldnames):
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

input_file = 'data/crypto_vcs.csv'
output_file = 'data/crypto_vcs_updated.csv'

data = read_csv(input_file)

# Process only the first 10 rows for testing
data = data[:10]

for row in data:
    twitter_links = extract_twitter_links(row['Website'])
    row['twitter'] = ', '.join(twitter_links) if twitter_links else ''
    time.sleep(1)  # Sleep for 1 second between requests

fieldnames = data[0].keys()
write_csv(output_file, data, fieldnames)

print(f"Updated CSV file saved as {output_file}")
