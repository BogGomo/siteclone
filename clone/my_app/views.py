import requests
from requests.compat import quote_plus
from django.shortcuts import render
from . import models
from bs4 import BeautifulSoup
BASE_EMAG_URL = 'https://www.emag.ro/search/{}'
# Create your views here.

def home(request):
    return render(request, 'base.html')
def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_EMAG_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    post_listings = soup.find_all('div', {'class': 'card-item js-product-data'})
    final_postings = []


    for post in post_listings:
        post_title = post.find(class_="product-title").text
        reverse_price = post.find(class_="product-new-price").text[::-1]
        lenght = len(reverse_price)
        price_end =  reverse_price[3:6]
        price_start = reverse_price[6:lenght]
        price_start = price_start.replace('.','')
        post_new_price = price_start[::-1] + '.' + price_end[::-1]
        #post_new_price = float(post_new_price)
        for image in post.find_all('img', class_='lozad', src=True):
            post_image = image.get('data-src')
            print(post_image)
        for link in post.find_all('a', class_= 'product-title js-product-url', href=True):
            post_url = link.get('href')

        final_postings.append((post_title, post_new_price,post_url, post_image))

    stuf_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, 'my_app/new_search.html', stuf_for_frontend)

