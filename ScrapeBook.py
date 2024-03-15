# importing dependencies
import requests
from bs4 import BeautifulSoup
import pymongo

# function to fetch the data and scrape the data from website
def fetchBooks(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    books  = []
    for book in soup.find_all('article', class_= 'product_pod'):
        name = book.find('h3').a['title']
        price = book.find('p', class_= 'price_color').text
        availability = book.find('p', class_='instock availability').text.strip()
        rating = book.find('p', class_='star-rating')['class'][1]
        books.append({'name': name, 'price': price, 'availability': availability, 'rating': rating})
    return books

# Create mongoDB instance
mongoClient = pymongo.MongoClient("mongodb://localhost:27017")
db = mongoClient["TailNode2"]

# API endpoint
baseUrl = 'http://books.toscrape.com/catalogue/page-{}.html'
booksData = []
# Get data from page
for pageNum in range(1, 51):
    url = baseUrl.format(pageNum)
    booksData += fetchBooks(url)

# Save data to mongoDB
books_collection = db["books"]
books_collection.insert_many(booksData)
