import requests
from bs4 import BeautifulSoup
from pprint import pprint

def get_info(page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.0.1996 Yowser/2.5 Safari/537.36'}
    url = 'https://roscontrol.com'
    response = requests.get(url + '/category/produkti/molochnie_produkti/moloko'+f'?page={page}', headers=headers)
    dom = BeautifulSoup(response.text, 'html.parser')
    products = dom.find_all('div', {'class':'wrap-product-catalog__item grid-padding grid-column-4 grid-column-large-6 grid-column-middle-12 grid-column-small-12 grid-left js-product__item' })
    product_list = []
    for product in products:
        product_data = {}
        name = product.find('div', {'class': 'product__item-link'}).getText()
        rating_block_values = product.find_all('div', {'class': 'right'})
        try:
            safety = int(rating_block_values[0].getText())
        except:
            safety = None
        try:
            naturality = int(rating_block_values[1].getText())
        except:
            naturality = None
        try:
            nutritional_value = int(rating_block_values[2].getText())
        except:
            nutritional_value = None
        try:
            quality = int(rating_block_values[3].getText())
        except:
            quality = None
        try:
            general_assessment = int(product.find('div', {'class': 'rate rating-value'}).getText())
        except:
            general_assessment = None
        link = product.find('a')['href']
        link = url + link
        product_data['name'] = name
        product_data['safety'] = safety
        product_data['naturality'] = naturality
        product_data['nutritional_value'] = nutritional_value
        product_data['quality'] = quality
        product_data['general_assessment'] = general_assessment
        product_data['link'] = link
        product_list.append(product_data)
    return(product_list)
product_list = []
for i in range(1, 6):
    a = get_info(i)
    product_list.append(a)
pprint(product_list)
