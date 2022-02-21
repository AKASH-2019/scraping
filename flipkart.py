import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl

def tshirtsUrl(page):
    url = f'https://www.flipkart.com/mens-tshirts/pr?sid=clo%2Cash%2Cank%2Cedy&otracker[]=categorytree&otracker[]=nmenu_sub_Men_0_T-Shirts&page={page}'

    r = requests.get(url)
    # soup = BeautifulSoup(r.content,'html.parser')

    return r

def extract(soup):
    divs = soup.find_all('div', class_='_1xHGtK _373qXS')

    for items in divs:
        try:
            company = items.find('div', class_='_2WkVRV').text
        except:
            company = 'Company name not available'
        
        title = items.find('a', class_='IRpwTa').text

        try:
            pack_of = items.find('div',class_='_3eWWd-').text
        except:
            pack_of = 'pack_of not available'
        
        try:
            originalPrice = items.find('div',class_='_30jeq3').text.replace('₹','')
        except:
            originalPrice = 'price not available'
        
        try:
            discountedPrice = items.find('div',class_='_3I9_wc').text.replace('₹','')
        except:
            discountedPrice = 'no discount'
        
        try:
            discount = items.find('div',class_='_3Ay6Sb').text.replace('off','')
        except:
            discount = 'no discount'

        # print(company,title,pack_of) 
        tshirt = {
            'Product Name':title,
            'Company Name':company,
            'Price':originalPrice,
            'Discounted Price':discountedPrice,
            'Pack of':pack_of,
            'Discount':discount

        }
        tshirt_list.append(tshirt)

    return len(divs)


tshirt_list = []
for i in range(1,51):
    print(f"scraping page {i}")
    Urlcontent = tshirtsUrl(i)

    soup = BeautifulSoup(Urlcontent.content,'html.parser')
    chaeckdivs = soup.find_all('div', class_='_1xHGtK _373qXS')

    if Urlcontent.status_code == 200 and len(chaeckdivs)>0:
        extract(soup)
    else:
        print('url not valid')
        break

# print(tshirt_list)
df = pd.DataFrame(tshirt_list)
# df.to_csv("Tshirts.csv")
df.to_excel("Tshirts.xlsx")
