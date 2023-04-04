import os

from django.core.exceptions import ObjectDoesNotExist

os.environ["DJANGO_SETTINGS_MODULE"] = "onlineStore.settings"

import django

django.setup()

from bs4 import BeautifulSoup
import pandas as pd
import requests
import xml.etree.ElementTree as ET
import gzip
import urllib.request
from onlineStoreApp.models import Product, Retailer, Price, Manufacturer
from django.db import IntegrityError
from django.utils import timezone
import time


# http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=0&storeId=413



if __name__ == '__main__':
    start = time.time()

    num = 0

    def units_converter(unit):
        conversions = {
            'יחידה': ['units', 1],
            'גרמים': ['g', 100],
            'מיליליטרים': ['ml', 100],
            'קילוגרמים': ['kg', 1],
            'ליטרים': ['l', 1],
            'מטרים': ['m', 1],
        }
        return conversions.get(unit, [None, None])


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
    response = urllib.request.urlopen(price_url)

    with gzip.open(response, 'rb') as f:
        xml_data = f.read()

    root = ET.fromstring(xml_data)

    items_list = []

    # Loop through all Item elements
    for item in root.iter('Item'):
        # Create a dictionary for the current item
        item_dict = {}
        # Loop through all sub-elements of the current item
        for child in item:
            item_dict[child.tag] = child.text
        # Append the dictionary to the list of items
        items_list.append(item_dict)

    df = pd.DataFrame(items_list)

    # Convert data types
    df['Quantity'] = pd.to_numeric(df['Quantity'])
    df['QtyInPackage'] = pd.to_numeric(df['QtyInPackage'])
    df['ItemPrice'] = pd.to_numeric(df['ItemPrice'])
    df['UnitOfMeasurePrice'] = pd.to_numeric(df['UnitOfMeasurePrice'])

    # current_timestamp = int(timezone.now().timestamp())
    # retailer, created = Retailer.objects.get_or_create(name='Shufersal', defaults={'last_scan': current_timestamp})
    # retailer.last_scan = current_timestamp
    # retailer.save()
    #
    # for index, row in df.iterrows():
    #     num += 1
    #     if row['ManufacturerName'] is None or row['ManufacturerName'] == 'None':
    #         manufacturer_name = 'כללי'
    #     else:
    #         manufacturer_name = row['ManufacturerName']
    #     manufacturer = Manufacturer.objects.get_or_create(name=manufacturer_name)
    #     # print(manufacturer[0], type(manufacturer[0]))
    #
    #     unit_detail = units_converter(row['UnitQty'])
    #
    #     defaults = {
    #         'name': row['ItemName'],
    #         'quantity': row['Quantity'],
    #         'product_status': row['ItemStatus'],
    #         'discount_status': row['AllowDiscount'],
    #         'unit_of_measure_price': row['UnitOfMeasurePrice'],
    #         'units': unit_detail[0],
    #         'unit_of_measure': unit_detail[1],
    #         'manufacturer_id': manufacturer[0],
    #     }
    #     try:
    #         product, created = Product.objects.update_or_create(catalog_number=row['ItemCode'], defaults=defaults)
    #
    #     except IntegrityError:
    #         product = Product.objects.get(catalog_number=row['ItemCode'])
    #         product.name = row['ItemName']
    #         product.quantity = row['Quantity']
    #         product.product_status = True if row['ItemStatus'] == 1 else False
    #         product.discount_status = True if row['AllowDiscount'] == 1 else False
    #         product.unit_of_measure_price = row['UnitOfMeasurePrice']
    #         product.units = unit_detail[0]
    #         product.unit_of_measure = unit_detail[1]
    #         product.manufacturer_id = manufacturer[0]
    #         product.save()
    #
    #
    #     try:
    #         price, created = Price.objects.update_or_create(product_id=product, retailer_id=retailer, defaults={'price': row['ItemPrice']})
    #
    #     except IntegrityError:
    #         pass
    #
    # print(num)
    # end = time.time()
    # print(end - start)









    current_timestamp = int(timezone.now().timestamp())
    retailer, created = Retailer.objects.get_or_create(name='Shufersal', defaults={'last_scan': current_timestamp})
    retailer.last_scan = current_timestamp
    retailer.save()

    manufacturer_create_list = []
    manufacturer_update_list = []

    product_create_list = []
    product_update_list = []

    price_create_list = []
    price_update_list = []

    for index, row in df.iterrows():
        num += 1
        if row['ManufacturerName'] is None or row['ManufacturerName'] == 'None':
            manufacturer_name = 'כללי'
        else:
            manufacturer_name = row['ManufacturerName']

        try:
            manufacturer = Manufacturer.objects.get(name=manufacturer_name)

            if manufacturer.country != row['ManufactureCountry']:
                manufacturer.country = row['ManufactureCountry']

                manufacturer_update_list.append(manufacturer)

        except ObjectDoesNotExist:
            manufacturer = Manufacturer(
                name = manufacturer_name,
                country = row['ManufactureCountry'],
            )
            manufacturer_create_list.append(manufacturer)


        unit_detail = units_converter(row['UnitQty'])

        try:
            product= Product.objects.get(catalog_number=row['ItemCode'])

            product.name = row['ItemName']
            product.quantity = row['Quantity']
            product.product_status = True if row['ItemStatus'] == 1 else False
            product.discount_status = True if row['AllowDiscount'] == 1 else False
            product.unit_of_measure_price = row['UnitOfMeasurePrice']
            product.units = unit_detail[0]
            product.unit_of_measure = unit_detail[1]
            product.manufacturer_id = manufacturer

            product_update_list.append(product)

        except ObjectDoesNotExist:
            product = Product(
                name = row['ItemName'],
                quantity = row['Quantity'],
                product_status = row['ItemStatus'],
                discount_status = row['AllowDiscount'],
                unit_of_measure_price = row['UnitOfMeasurePrice'],
                units = unit_detail[0],
                unit_of_measure = unit_detail[1],
                manufacturer_id = manufacturer,
            )
            product_create_list.append(product)

        try:
            price = Price.objects.get(product_id=product, retailer_id=retailer)

            if price.price != row['ItemPrice']:
                price.price = row['ItemPrice']

                price_update_list.append(price)

        except ObjectDoesNotExist:
            price = Price(
                product_id = product,
                retailer_id = retailer,
                price = row['ItemPrice'],
            )

    if manufacturer_create_list:
        Manufacturer.objects.bulk_create(manufacturer_create_list)
    if manufacturer_update_list:
        Manufacturer.objects.bulk_update(manufacturer_update_list, ['country'])

    if product_create_list:
        Product.objects.bulk_create(product_create_list)
    if product_update_list:
        Product.objects.bulk_update(product_update_list, ['name', 'manufacturer_id', 'quantity', 'product_status', 'unit_of_measure_price', 'units', 'unit_of_measure', 'discount_status',])

    if price_create_list:
        Price.objects.bulk_create(price_create_list)
    if price_update_list:
        Price.objects.bulk_update(price_update_list, ['price'])

    print(num)
    end = time.time()
    print(end - start)