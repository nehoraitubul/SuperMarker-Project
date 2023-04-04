from bs4 import BeautifulSoup
import pandas as pd
import requests
import xml.etree.ElementTree as ET
import gzip
import urllib.request
# from onlineStoreApp.models import Product, Retailer, Price


# http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=0&storeId=413



if __name__ == '__main__':

    def units(unit):
        if unit == 'יחידה':
            return 'units'
        if unit == 'גרמים':
            return 'g'
        if unit == 'מיליליטרים':
            return 'ml'
        if unit == 'קילוגרמים':
            return 'kg'
        if unit == 'ליטרים':
            return 'l'


    response = requests.get('http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=0&storeId=413')

    soup = BeautifulSoup(response.text, 'html.parser')

    price_full_url = soup.find("td", string='pricefull')
    a = price_full_url.parent
    print('price full data link:')
    price_url = a.find('a')['href']
    print(price_url)

    promo_full_url = soup.find("td", string='promofull')
    b = promo_full_url.parent
    print('promos full data link:')
    promo_url = b.find('a')['href']
    print(promo_url)



    # request to DataFrame
    # response = urllib.request.urlopen(price_url)
    #
    # with gzip.open(response, 'rb') as f:
    #     xml_data = f.read()
    #
    # root = ET.fromstring(xml_data)
    #
    # items_list = []
    #
    # # Loop through all Item elements
    # for item in root.iter('Item'):
    #     # Create a dictionary for the current item
    #     item_dict = {}
    #     # Loop through all sub-elements of the current item
    #     for child in item:
    #         item_dict[child.tag] = child.text
    #     # Append the dictionary to the list of items
    #     items_list.append(item_dict)
    #
    # df = pd.DataFrame(items_list)
    #
    # # Convert data types
    # df['Quantity'] = pd.to_numeric(df['Quantity'])
    # df['QtyInPackage'] = pd.to_numeric(df['QtyInPackage'])
    # df['ItemPrice'] = pd.to_numeric(df['ItemPrice'])
    # df['UnitOfMeasurePrice'] = pd.to_numeric(df['UnitOfMeasurePrice'])
    #
    # retailer = Retailer.objects.get(name='Shufersal')
    #
    # for index, row in df.iterrows():
    #     product = Product.objects.get(catalog_number = row['ItemCode'])
    #     product.name = row['ItemName']
    #     product.quantity = row['Quantity']
    #     product.product_status = True if row['ItemStatus'] == 1 else False
    #     product.discount_status = True if row['AllowDiscount'] == 1 else False
    #     product.unit_of_measure_price = row['UnitOfMeasurePrice']
