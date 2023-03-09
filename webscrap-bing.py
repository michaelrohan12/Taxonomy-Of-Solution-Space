import requests
from bs4 import BeautifulSoup

# Set the search query
query = "python programming"

# Send a request to Bing and get the HTML response
url = f"https://www.bing.com/search?q={query}"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
response = requests.get(url, headers=headers)

# Parse the HTML response using Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')

# Get the top three links from the search results
search_results = soup.find_all('li', {'class': 'b_algo'})[:3]

# Scrape the text from the top three links and write it to a file
for i, link in enumerate(search_results):
    # Get the link URL
    url = link.find('a')['href']
    # Send a request to the link URL and get the HTML response
    response = requests.get(url, headers=headers)
    # Parse the HTML response using Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')
    # Get the text from the HTML response, replace consecutive whitespace characters with a single space, and strip leading/trailing whitespace
    text = ' '.join(soup.get_text().split())
    # Format the text into paragraphs
    paragraphs = []
    curr_paragraph = ''
    for sentence in text.split('.'):
        if len(curr_paragraph + sentence) > 80:
            paragraphs.append(curr_paragraph.strip())
            curr_paragraph = ''
        curr_paragraph += sentence + '.'
    if curr_paragraph:
        paragraphs.append(curr_paragraph.strip())
    # Write the paragraphs to a file
    with open(f"bing-results/result{i+1}.txt", "w", encoding='utf-8') as f:
        for p in paragraphs:
            f.write(p + '\n\n')
