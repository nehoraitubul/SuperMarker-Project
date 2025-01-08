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
from onlineStoreApp.models import Product, Retailer, Price, Manufacturer, Promo, PromoProduct
from django.db import IntegrityError, transaction
from django.utils import timezone
import time
from datetime import datetime



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

    end = time.time()
    print('enf of scraping', end - start)



    # request to DataFrame
    response = urllib.request.urlopen(promo_url)

    with gzip.open(response, 'rb') as f:
        xml_data = f.read()

    root = ET.fromstring(xml_data)

    # PRICE #

    # end = time.time()
    # print('xml to memory', end - start)
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
    # # result = df[df['ItemCode'] == '10900145015']
    # # pd.set_option('display.max_rows', None)  # to display all rows
    # # pd.set_option('display.max_columns', None)  # to display all columns
    # # print(result['ItemPrice'])
    #
    # end = time.time()
    # print('pandas dataFrame', end - start)
    #
    # # Convert data types
    # df['Quantity'] = pd.to_numeric(df['Quantity'])
    # df['QtyInPackage'] = pd.to_numeric(df['QtyInPackage'])
    # df['ItemPrice'] = pd.to_numeric(df['ItemPrice'])
    # df['UnitOfMeasurePrice'] = pd.to_numeric(df['UnitOfMeasurePrice'])
    #
    # processed_catalog_numbers = []
    #
    # current_timestamp = int(timezone.now().timestamp())
    # retailer, created = Retailer.objects.get_or_create(name='Shufersal', defaults={'last_scan': current_timestamp})
    # retailer.last_scan = current_timestamp
    # retailer.save()
    #
    # created_itemcodes = []
    #
    # try:
    #     with transaction.atomic():
    #         for index, row in df.iterrows():
    #             processed_catalog_numbers.append(row['ItemCode'])
    #             num += 1
    #             # if row['ManufacturerName'] is None or row['ManufacturerName'] == 'None':
    #             #     manufacturer_name = 'כללי'
    #             # else:
    #             #     manufacturer_name = row['ManufacturerName']
    #             # manufacturer = Manufacturer.objects.get_or_create(name=manufacturer_name)
    #             # # print(manufacturer[0], type(manufacturer[0]))
    #
    #             unit_detail = units_converter(row['UnitQty'])
    #
    #             defaults = {
    #                 # 'name': row['ItemName'],
    #                 'quantity': row['Quantity'],
    #                 'product_status': row['ItemStatus'],
    #                 'discount_status': row['AllowDiscount'],
    #                 'unit_of_measure_price': row['UnitOfMeasurePrice'],
    #                 'units': unit_detail[0],
    #                 'unit_of_measure': unit_detail[1],
    #                 # 'manufacturer_id': manufacturer[0],
    #             }
    #             try:
    #                 product, created = Product.objects.update_or_create(catalog_number=row['ItemCode'], defaults=defaults)
    #
    #                 if created:
    #                     created_itemcodes.append(row['ItemCode'])
    #
    #             except IntegrityError:
    #                 product = Product.objects.get(catalog_number=row['ItemCode'])
    #                 # product.name = row['ItemName']
    #                 product.quantity = row['Quantity']
    #                 product.product_status = True if row['ItemStatus'] == 1 else False
    #                 product.discount_status = True if row['AllowDiscount'] == 1 else False
    #                 product.unit_of_measure_price = row['UnitOfMeasurePrice']
    #                 product.units = unit_detail[0]
    #                 product.unit_of_measure = unit_detail[1]
    #                 # product.manufacturer_id = manufacturer[0]
    #                 product.save()
    #
    #
    #             try:
    #                 price, created = Price.objects.update_or_create(product_id=product, retailer_id=retailer,
    #                             defaults={'price': row['ItemPrice'], 'unit_of_measure_price': row['UnitOfMeasurePrice'],
    #                                       'unit_of_measure': unit_detail[1], 'units': unit_detail[0]})
    #
    #             except IntegrityError as i:
    #                 print(i)
    #
    # except IntegrityError as i:
    #     print(i)
    #
    #
    # print(num)
    # end = time.time()
    # print(end - start)
    #
    # # Set product_status to False
    # unprocessed_products = Product.objects.exclude(catalog_number__in=processed_catalog_numbers)
    # count = unprocessed_products.update(product_status=False)
    # print(f"{count} products were updated")
    #
    # end = time.time()
    # print(end - start)

    # PRICE #

    # # PROMO #

    retailer = Retailer.objects.get(name='Shufersal')
    retailer_model_id = retailer.id


    counter = 0
    for promotion_elem in root.iter('Promotion'):
        counter += 1
        reward_type = promotion_elem.findtext('RewardType')
        promotion_id = promotion_elem.findtext('PromotionId')
        allow_multiple_discounts = promotion_elem.findtext('AllowMultipleDiscounts')
        description = promotion_elem.findtext('PromotionDescription')
        update_date = datetime.strptime(promotion_elem.findtext('PromotionUpdateDate'), '%Y-%m-%d %H:%M')
        start_date = promotion_elem.findtext('PromotionStartDate')
        start_hour = promotion_elem.findtext('PromotionStartHour')
        end_date = promotion_elem.findtext('PromotionEndDate')
        end_hour = promotion_elem.findtext('PromotionEndHour')
        is_weighted_promo = promotion_elem.findtext('IsWeightedPromo')
        min_qty = promotion_elem.findtext('MinQty')
        max_qty = promotion_elem.findtext('MaxQty')
        discount_rate = promotion_elem.findtext('DiscountRate')
        discount_type = promotion_elem.findtext('DiscountType')
        discounted_price = promotion_elem.findtext('DiscountedPrice')
        min_no_of_item_offered = promotion_elem.findtext('MinNoOfItemOfered')
        remark = promotion_elem.findtext('Remark')

        # Finding club_id
        club_id_elem = promotion_elem.find('Clubs/ClubId')
        if club_id_elem is not None:
            club_id = club_id_elem.text
        else:
            club_id = None

        # Finding additional_gift_count
        additional_gift_count_elem = promotion_elem.find('AdditionalRestrictions/AdditionalGiftCount')
        if additional_gift_count_elem is not None:
            additional_gift_count = additional_gift_count_elem.text
        else:
            additional_gift_count = None

        # print('reward_type - ', reward_type)
        # print('promotion_id - ', promotion_id)
        # print('allow_multiple_discounts - ', allow_multiple_discounts)
        # print('description - ', description)
        # print('update_date - ', update_date)
        # print('start_date - ', start_date)
        # print('start_hour - ', start_hour)
        # print('end_date - ', end_date)
        # print('end_hour - ', end_hour)
        # print('is_weighted_promo - ', is_weighted_promo)
        # print('min_qty - ', min_qty)
        # print('max_qty - ', max_qty)
        # print('discount_rate - ', discount_rate)
        # print('discount_type - ', discount_type)
        # print('discounted_price - ', discounted_price)
        # print('min_no_of_item_offered - ', min_no_of_item_offered)
        # print('remark - ', remark)
        # print('retailer_id', retailer)
        # print('club_id - ', club_id)
        # print('additional_gift_count - ', additional_gift_count)

        update_date = timezone.make_aware(update_date)

        promo, created = Promo.objects.get_or_create(promotion_id=promotion_id, defaults={
            'reward_type': reward_type,
            'allow_multiple_discounts': allow_multiple_discounts,
            'description': description,
            'update_date': update_date,
            'start_date': start_date,
            'start_hour': start_hour,
            'end_date': end_date,
            'end_hour': end_hour,
            'is_weighted_promo': is_weighted_promo,
            'min_qty': min_qty,
            'max_qty': max_qty,
            'discount_rate': discount_rate,
            'discount_type': discount_type,
            'discounted_price': discounted_price,
            'min_no_of_item_offered': min_no_of_item_offered,
            'remark': remark,
            'retailer_id': retailer,
            'club_id': club_id if club_id is not None else 0,
            'additional_gift_count': additional_gift_count if additional_gift_count is not None else 0,
        })

        promo_items = promotion_elem.find('PromotionItems')
        if promo_items is not None:
            for item in promo_items.iter('Item'):
                product_id = item.findtext('ItemCode')
                is_gift_item = item.findtext('IsGiftItem')

                print('product_id - ', product_id)
                print('is_gift_item - ', is_gift_item)

                try:
                    product = Product.objects.get(catalog_number=product_id)
                    product_model_id = product.id
                except:
                    continue

                promo_product, _ = PromoProduct.objects.get_or_create(
                    promo_id= promo,
                    product_id= product,
                    is_gift_item= is_gift_item == '1'  # Convert 'IsGiftItem' text to boolean
                )


    # PROMO #