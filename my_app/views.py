import requests
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup

BASE_CRAIGSLIST_URL = 'https://bangalore.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


# Create your views here.
def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    # print(final_url)
    response = requests.get(final_url)
    data = response.text
    # print(data)
    soup = BeautifulSoup(data, features='html.parser')
    post_listing = soup.find_all('li', {'class':'result-row'})

    final_postlisting =[]
    for post in post_listing:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            image = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image = BASE_IMAGE_URL.format(image)
        else:
            post_image = 'https://www.essence-gas.com/wp-content/uploads/2017/08/no_image.jpg'
        final_postlisting.append((post_title, post_url, post_price, post_image))

    stuff_for_frondend = {
        'search': search,
        'final_postlisting': final_postlisting,
    }

    for post in final_postlisting:
        print(post[0])
        print(post[1])
        print(post[2])
        print(post[3])
    return render(request, 'my_app/new_search.html', stuff_for_frondend)
