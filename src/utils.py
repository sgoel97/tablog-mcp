from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel
from typing import Optional

BASE_URL = "https://tabelog.com/en/tokyo/"
MAX_PAGES = 60
NUM_PAGES_TO_SCRAPE = 5
MAX_RESTAURANTS_TO_SCRAPE = 50

class Restaurant(BaseModel):
    name: str
    tagline: str
    rating: str
    cost: str
    text: str
    url: str

    def __hash__(self):
        return hash((self.name, self.tagline, self.rating, self.cost, self.text, self.url))

    def to_string(self) -> str:
        return f"""
Name: {self.name}
URL: {self.url}
{'Tagline: ' + self.tagline if self.tagline else ''}
{'Rating: ' + self.rating if self.rating else ''}
{'Cost: ' + self.cost if self.cost else ''}
Text: {self.text}
""".strip()

def fetch_restaurant_links_from_page(page_link: str) -> list[str]:
    out = requests.get(page_link)
    soup = BeautifulSoup(out.content, "html.parser")

    all_page_links = []
    for link in soup.find_all("a"):
        all_page_links.append(link.get("href"))

    links = []
    for link in all_page_links:
        if link is not None and link.startswith(BASE_URL) and 'rstLst' not in link:
            cleaned_link = link.replace(BASE_URL, "").rstrip("/")
            if len(cleaned_link.split("/")) == 3:
                links.append(link)
    return list(set(links))

def fetch_restaurant_details(restaurant_link: str) -> Optional[Restaurant]:
    try:
        out = requests.get(restaurant_link)
        soup = BeautifulSoup(out.content, "html.parser")

        name = soup.find('h2', class_='display-name').text.strip()
        tagline = soup.find('span', class_='pillow-word')
        if tagline:
            tagline = tagline.text.strip()
        else:
            tagline = ""

        rating = soup.find('b', class_='c-rating__val')
        if rating:
            rating = rating.text.strip()
        else:
            rating = ""

        cost = soup.find('a', class_='rdheader-budget__price-target')
        if cost:
            cost = cost.text.strip()
        else:
            cost = ""

        text = soup.find('div', id='container').get_text().strip()
        text = ' '.join(text.split())
        
        return Restaurant(name=name, tagline=tagline, rating=rating, cost=cost, text=text, url=restaurant_link)
    except Exception as e:
        print(f"Error fetching restaurant details for {restaurant_link}: {e}")
        return None

def fetch_restaurants(area_code: str, cuisine_code: str, max_price: Optional[int] = None) -> list[Restaurant]:
    # Get `NUM_PAGES_TO_SCRAPE` links to scrape based on the area and cuisine
    page_links = []
    for page in range(1, NUM_PAGES_TO_SCRAPE + 1):
        url = f"{BASE_URL}{area_code}rstLst/{cuisine_code}/{page}/?SrtT=rt" # sort by highest rating
        if max_price:
            max_price = int(max_price / 1000) # tablog uses thousands of yen
            url += f"&LstCosT={max_price}"
        page_links.append(url)
        
    restaurant_links = set()
    with ThreadPoolExecutor(max_workers=NUM_PAGES_TO_SCRAPE) as executor:
        results = executor.map(fetch_restaurant_links_from_page, page_links, timeout=5)
        for result in results:
            restaurant_links.update(result)

    # Limit the number of restaurants to scrape
    restaurant_links = list(restaurant_links)[:MAX_RESTAURANTS_TO_SCRAPE]

    restaurants = []
    with ThreadPoolExecutor(max_workers=len(restaurant_links)) as executor:
        results = executor.map(fetch_restaurant_details, restaurant_links, timeout=5)
        for result in results:
            if result:
                restaurants.append(result)
    return restaurants
