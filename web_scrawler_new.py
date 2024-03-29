import os

from django.db import IntegrityError
from django.db.models import Q

os.environ["DJANGO_SETTINGS_MODULE"] = "onlineStore.settings"

import django

django.setup()

from onlineStoreApp.models import Product, ProductInfo, Category, SubCategory, SubSubCategory, SubSubSubCategory, \
    Manufacturer

import requests
from bs4 import BeautifulSoup
import time
import json
import re
import sys
import re

# ProductInfo.objects.filter(id__gte=8).delete()
# Product.objects.filter(id__gte=1).update(checked=0)
# Product.objects.filter(id__range=(4500, 6500)).update(checked=0)
# sys.exit()
def remove_numbers_7290(number):
    print("here")
    number_str = str(number)
    index = number_str.find("729")

    if index != -1:
        index += len("729")
        while number_str[index] == "0":
            index += 1

    result = number_str[index:]
    return result

# a = 7290000000022
# print(remove_numbers_7290(a))
# Product.objects.filter(Q(product_info_id__isnull=False) & Q(name__isnull=True)).update(checked=0)
products = Product.objects.filter(product_info_id__isnull=False, name__exact='')
# print(len(products))
# sys.exit()


# products_without_info = Product.objects.count()
# print(products_without_info)
# products_without_info = Product.objects.filter(product_info_id=None)
products_without_info = Product.objects.filter(checked=0)
print(products_without_info.count())
# fs = Product.objects.filter(catalog_number=3010470155299)
# product = fs.first()
# print(product.id)
# sys.exit()

num = 0
# products_without_info = [product]
for k in products_without_info:
    # k = product
    print(k.pk)
    print(k.name)
    print(k.catalog_number)
    if num >= 5000:
        break
    # if k.checked == 1:
    #     continue
    # k.checked = 1
    # k.save()
    # sys.exit()
    num += 1
    time.sleep(1)


    # base_link = f'https://www.shufersal.co.il/online/he/p/P_3161911229199/json?cartContext%5BopenFrom%5D=CATEGORY&cartContext%5BrecommendationType%5D=PRODUCT'

    base_link = f'https://www.shufersal.co.il/online/he/p/P_{k.catalog_number}/json?cartContext%5BopenFrom%5D=CATEGORY&cartContext%5BrecommendationType%5D=PRODUCT'

    response = requests.get(base_link)
    # print(response)

    if response.status_code == 404:
        if re.search(r"729000", str(k.catalog_number)):
            new_num = remove_numbers_7290(k.catalog_number)
            base_link = f'https://www.shufersal.co.il/online/he/p/P_{new_num}/json?cartContext%5BopenFrom%5D=CATEGORY&cartContext%5BrecommendationType%5D=PRODUCT'
            response = requests.get(base_link)
            if response.status_code == 404:
                k.checked = 1
                k.save()
                continue
        else:
            k.checked = 1
            k.save()
            continue
    # time.sleep(6)
    soup = BeautifulSoup(response.content, "html.parser")
    oos = soup.find('div', class_='productDetails notOverlay miglog-prod-outOfStock')
    if oos:
        print('oos')
        k.checked = 1
        k.save()
        continue

    no_modal = soup.find('div', class_='modal-dialog nonfoodModal miglog-prod')
    error_page = soup.find('div', class_='errorPageWrap clearfix')
    if no_modal or error_page:
        print('no modal')
        # base_link = f'https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%95%D7%A8%D7%99%D7%95%D7%AA/%D7%A1%D7%95%D7%A4%D7%A8%D7%9E%D7%A8%D7%A7%D7%98/%D7%9E%D7%A9%D7%A7%D7%90%D7%95%D7%AA%2C-%D7%90%D7%9C%D7%9B%D7%95%D7%94%D7%95%D7%9C-%D7%95%D7%99%D7%99%D7%9F/%D7%99%D7%99%D7%A0%D7%95%D7%AA-%D7%95%D7%AA%D7%99%D7%A8%D7%95%D7%A9/%D7%9E%D7%99%D7%A5-%D7%A2%D7%A0%D7%91%D7%99%D7%9D-%D7%AA%D7%99%D7%A8%D7%95%D7%A9/%D7%9E%D7%99%D7%A5-%D7%A2%D7%A0%D7%91%D7%99%D7%9D-%D7%AA%D7%99%D7%A8%D7%95%D7%A9/p/P_3161911229199'


        base_link = f'https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%95%D7%A8%D7%99%D7%95%D7%AA/%D7%A1%D7%95%D7%A4%D7%A8%D7%9E%D7%A8%D7%A7%D7%98/%D7%9E%D7%A9%D7%A7%D7%90%D7%95%D7%AA%2C-%D7%90%D7%9C%D7%9B%D7%95%D7%94%D7%95%D7%9C-%D7%95%D7%99%D7%99%D7%9F/%D7%99%D7%99%D7%A0%D7%95%D7%AA-%D7%95%D7%AA%D7%99%D7%A8%D7%95%D7%A9/%D7%9E%D7%99%D7%A5-%D7%A2%D7%A0%D7%91%D7%99%D7%9D-%D7%AA%D7%99%D7%A8%D7%95%D7%A9/%D7%9E%D7%99%D7%A5-%D7%A2%D7%A0%D7%91%D7%99%D7%9D-%D7%AA%D7%99%D7%A8%D7%95%D7%A9/p/P_{k.catalog_number}'
        response = requests.get(base_link)
        if response.status_code == 404:
            if re.search(r"729000", str(k.catalog_number)):
                new_num = remove_numbers_7290(k.catalog_number)
                base_link = f'https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%95%D7%A8%D7%99%D7%95%D7%AA/%D7%A1%D7%95%D7%A4%D7%A8%D7%9E%D7%A8%D7%A7%D7%98/%D7%9E%D7%A9%D7%A7%D7%90%D7%95%D7%AA%2C-%D7%90%D7%9C%D7%9B%D7%95%D7%94%D7%95%D7%9C-%D7%95%D7%99%D7%99%D7%9F/%D7%99%D7%99%D7%A0%D7%95%D7%AA-%D7%95%D7%AA%D7%99%D7%A8%D7%95%D7%A9/%D7%9E%D7%99%D7%A5-%D7%A2%D7%A0%D7%91%D7%99%D7%9D-%D7%AA%D7%99%D7%A8%D7%95%D7%A9/%D7%9E%D7%99%D7%A5-%D7%A2%D7%A0%D7%91%D7%99%D7%9D-%D7%AA%D7%99%D7%A8%D7%95%D7%A9/p/P_{new_num}'
                response = requests.get(base_link)
                if response.status_code == 404:
                    k.checked = 1
                    k.save()
                    continue
            else:
                k.checked = 1
                k.save()
                continue
        soup = BeautifulSoup(response.content, "html.parser")

    # try:
    #     # שם מוצר בPRODUCT
    #     try:
    #         name = soup.find('h3', class_='description').text.strip()
    #         print('first', name)
    #     except Exception:
    #         name = soup.find('h1', class_='description').text.strip()
    #     k.name = name
    #     print('name', name)
    # except Exception:
    #     print('name', 'no name')
    #     pass
    #
    # k.save()


    product_info = ProductInfo()
    category_1 = Category()
    category_2 = SubCategory()
    category_3 = SubSubCategory()
    category_4 = SubSubSubCategory()


    try:
        if not no_modal and not error_page:
            categories = soup.find('div', class_='modal-dialog')
            data_gtm = categories.attrs['data-gtm']
            data_dict = json.loads(data_gtm)
            category_level1 = data_dict['categoryLevel1'].strip()
            category_level2 = data_dict['categoryLevel2'].strip()
            category_level3 = data_dict['categoryLevel3'].strip()
            category_level4 = data_dict['categoryLevel4'].strip()
            print("category_level1", category_level1)

        else:
            categories = soup.find_all('li', itemprop='itemListElement')
            category_names = []
            for category  in categories:
                if not category.get('class'):
                    category_name = category.find('span', itemprop='name').text.strip()
                    category_names.append(category_name)

            print(category_names)

            if len(category_names) == 0:
                k.checked = 1
                k.save()
                continue

            category_level1 = category_names[0]
            category_level2 = category_names[1]
            category_level3 = category_names[2]
            category_level4 = category_names[3]


        restricted_categories = ['יום העצמאות', 'שבועות', 'מה חדש', 'מתנות לחג', 'פסח בשופרסל Online', 'חדש על המדף', ]


        if any(category in restricted_categories for category in [category_level1, category_level2, category_level3, category_level4]):
            k.checked = 1
            k.save()
            continue
        if 'סופרמרקט' in category_level1:
            pass
        else:
            k.checked = 1
            k.save()
            continue

        print('category_level1->',category_level1,'|', 'category_level2->',category_level2, '|', 'category_level3 ->',category_level3, '|', 'category_level4 ->',category_level4)

        try:
            category_1 = Category.objects.get(name=category_level1)
            print(category_1)
        except Category.DoesNotExist as e:
            print(f"Error creating category 1: {e}")
            category_1 = Category(name=category_level1)
            category_1.save()

        try:
            category_2 = SubCategory.objects.get(name=category_level2, category_id=category_1)
            print(category_2)
        except SubCategory.DoesNotExist as e:
            print(f"Error creating category 2: {e}")
            category_2 = SubCategory(name=category_level2, category_id=category_1)
            category_2.save()

        try:
            category_3 = SubSubCategory.objects.get(name=category_level3, sub_category_id=category_2)
            print(category_3)
        except SubSubCategory.DoesNotExist as e:
            print(f"Error creating category 3: {e}")
            category_3 = SubSubCategory(name=category_level3, sub_category_id=category_2)
            category_3.save()

        try:
            category_4 = SubSubSubCategory.objects.get(name=category_level4, sub_sub_category_id=category_3)
            print(category_4)
        except SubSubSubCategory.DoesNotExist as e:
            print(f"Error creating category 4: {e}")
            category_4 = SubSubSubCategory(name=category_level4, sub_sub_category_id=category_3)
            category_4.save()
        # except IntegrityError:
        #     print('IntegrityError')


    except Exception:
        pass



    try:
        print("DESCRIPTION")
        if not no_modal:
            print("DESCRIPTION1")
            description = soup.find('div', class_='remarksText')
            description_text = description.find('div').prettify().strip()
            # print(description_text)
        else:
            print("DESCRIPTION2")
            description = soup.find('div', class_='paddingWrapper')
            description_text  = description.find('div', class_='desc').text.strip()
            # print(description_text)

        description_text = description_text.replace('\x00', '')
        product_info.description = description_text
    except Exception:
        pass






    info = soup.find_all('div', class_='box')

    # כשרות, חלבי/פרווה/בשרי
    for i in info:
        try:
            name = i.find('div', class_='name').text
            if name == 'חלבי/בשרי/פרווה:':
                product_info.kosher_type = i.find('div', class_='text').text
                print(i.find('div', class_='text').text)

            elif name == 'כשרות:':
                product_info.kosher = i.find('div', class_='text').text
                print(i.find('div', class_='text').text)

            elif name == 'פסח:':
                product_info.passover = i.find('div', class_='text').text
                print(i.find('div', class_='text').text)

            # ADDED

            elif name == 'רבנות מקומית:':
                product_info.local_rabbinate = i.find('div', class_='text').text
                print(i.find('div', class_='text').text)


            elif name == 'ארץ ייצור:':
                product_info.local_rabbinate = i.find('div', class_='text').text
                print(i.find('div', class_='text').text)


            elif name == 'אבקת חלב נוכרי:':
                product_info.foreign_milk = i.find('div', class_='text').text
                print(i.find('div', class_='text').text)


            elif name == 'מותג/יצרן:':
                manu_name = i.find('div', class_='text').text
                if manu_name is None or manu_name == 'None':
                    manu_name = 'כללי'

                manufacturer = Manufacturer.objects.get_or_create(name=manu_name)
                k.manufacturer_id = manufacturer[0]
                print(i.find('div', class_='text').text)

            # ADDED

        except Exception:
            pass

    try:
        print('סימון בריאותי')
        # סימון בריאותי
        markingList = soup.find('div', class_='markingList')
        mark_items = markingList.find_all('i')
        print(mark_items)
        for mark in mark_items:
            marking = ' '.join(mark['class'])
            if marking == 'icon icon-gluten-free':
                product_info.gluten_free = True
                print('gluten_free')
            elif marking == 'icon icon-lactose-free':
                product_info.lactose_free = True
                print('lactose_free')
            elif marking == 'icon icon-no-preserv':
                product_info.no_preserv = True
                print('no_preserv')
            elif marking == 'icon icon-organic-1':
                product_info.organic = True
                print('organic')
    except Exception:
        pass

    try:
        # רכיבים
        components = soup.find('div', class_='componentsText').text.strip()
        components = components.replace('\x00', '')
        product_info.component = components
        print('components', components)
    except Exception:
        pass

    try:
        # png
        png = soup.find('img', class_='img-responsive')
        k.image = png.get('src')
        print('png', png.get('src'))
    except Exception:
        pass


    try:
        # ערכים תזונתיים
        inde = soup.find_all('div', class_='nutritionItem')
        seen_values = []
        for i in inde:
            a = i.find('div', class_='text').text.strip()
            if a in seen_values:
                break
            seen_values.append(a)
            inde_amount = i.find('div', class_='number tooltip-js').text.strip()
            print(a, "    ", inde_amount)

            #insert into db:
            try:
                if a == 'סיבים תזונתיים':
                    product_info.dietary_fiber = inde_amount

                elif a == 'סוכרים מפחמימות' or a == 'סוכרים מתוך פחמימות':
                    product_info.sugars_from_carbohydrates = inde_amount

                elif a == 'אנרגיה':
                    product_info.energy = inde_amount

                elif a == 'חלבונים':
                    product_info.proteins = inde_amount

                elif a == 'פחמימות':
                    product_info.carbohydrates = inde_amount

                elif a == 'שומנים':
                    product_info.fats = inde_amount

                elif a == 'נתרן':
                    product_info.sodium = inde_amount

                elif a == 'מלח':
                    product_info.salt = inde_amount

                elif a == 'כולסטרול':
                    product_info.cholesterol = inde_amount

                elif a == 'מתוכם שומן רווי' or a == 'שומן רווי':
                    product_info.saturated_fat = inde_amount

                elif a == 'חומצות שומן טרנס':
                    product_info.trans_fatty_acids = inde_amount

                elif a == 'סוכר' or a == 'כפיות סוכר':
                    product_info.sugar = inde_amount

                elif a == 'ברזל':
                    product_info.iron = inde_amount

                elif a == 'סידן':
                    product_info.calcium = inde_amount

                # ADDED

                elif a == 'תאית':
                    product_info.cellulose = inde_amount

                elif a == 'טאורין':
                    product_info.taurine = inde_amount

                elif a == 'זרחן':
                    product_info.phosphorus = inde_amount

                elif a == 'לחות':
                    product_info.humidity = inde_amount

                # ADDED


            except Exception:
                pass


    except Exception:
        pass


    try:
        # מכיל לאלרגנים
        alergies_info = soup.find('div', class_='alergiesProperties').text.strip()
        alergies_info = ' '.join(alergies_info.split())
        product_info.allergies_properties = alergies_info
        print('alergies_info', alergies_info)
    except Exception:
        pass


    try:
        # עלול להכיל לאלרגנים
        alergiesTraces_info = soup.find('div', class_='alergiesTracesProperties').text.strip()
        alergiesTraces_info = ' '.join(alergiesTraces_info.split())
        product_info.allergies_traces = alergiesTraces_info
        print('alergiesTraces_info', alergiesTraces_info)
    except Exception:
        pass


    # ADDED
    try:
        # סימונים
        symbols = soup.find('li', class_='productSymbols')
        product_symbols_numbers = symbols.find_all('img')
        all_symbols = ''
        for symbol in product_symbols_numbers:
            alt_text = symbol['alt']
            number = alt_text.split('.')[-1]
            all_symbols += '-' + number
        product_info.product_symbols = all_symbols
        print('product_symbols', all_symbols)
    except Exception:
        pass


    try:
        # שם מוצר בPRODUCT
        try:
            name = soup.find('h3', class_='description').text.strip()
            print('first', name)
        except Exception:
            name = soup.find('h1', class_='description').text.strip()
        k.name = name
        print('name', name)
    except Exception:
        print('name', 'no name')
        pass
    # ADDED

    # print('here')
    product_info.save()
    # print('here')
    k.product_info_id = product_info
    # print('here')
    k.category_id = category_4
    # print('here')
    # print(category_1)
    # print(category_2)
    # print(category_3)
    # print(category_4)
    # print(k.category_id)
    k.checked = 1
    k.save()


print('DONE')