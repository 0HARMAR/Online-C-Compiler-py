import requests
from bs4 import BeautifulSoup

url = "https://en.cppreference.com/w/c/header/stdio.html"

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
try:
    response = requests.get(url,headers=headers)
    response.raise_for_status()

    html_content = response.text
    print("HTML content fetched successfully.")
    print(html_content)

    # 查找所有的h3标签，并打印它们的文本内容
    soup = BeautifulSoup(html_content, 'html.parser')
    h3_tags = soup.find_all('h3')
    print("Found h3 tags:")
    for tag in h3_tags:
        print(tag.text)

except requests.exceptions.RequestException as e:
    print(f"An error occurred while fetching the URL: {e}")