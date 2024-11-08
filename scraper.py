import requests
from bs4 import BeautifulSoup
import json

# URL сайта
BASE_URL = "https://quotes.toscrape.com/page/{}/"

# Функция для получения данных с одной страницы
def get_quotes_from_page(page_num):
    url = BASE_URL.format(page_num)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    quotes = []
    for quote_div in soup.find_all('div', class_='quote'):
        text = quote_div.find('span', class_='text').text
        author = quote_div.find('small', class_='author').text
        tags = [tag.text for tag in quote_div.find_all('a', class_='tag')]

        quotes.append({
            "text": text,
            "author": author,
            "tags": tags
        })

    return quotes

# Сбор всех цитат со всех страниц
def scrape_quotes():
    all_quotes = []
    page_num = 1
    while True:
        quotes = get_quotes_from_page(page_num)
        if not quotes:
            break
        all_quotes.extend(quotes)
        page_num += 1

    return all_quotes

# Сохранение данных в JSON файл
def save_to_json(data, filename="quotes.json"):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Основной процесс
if __name__ == "__main__":
    quotes = scrape_quotes()
    save_to_json(quotes)
    print(f"Data successfully saved to quotes.json")