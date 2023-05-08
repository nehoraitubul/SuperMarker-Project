import os
import requests
from PIL import Image
from io import BytesIO

os.environ["DJANGO_SETTINGS_MODULE"] = "onlineStore.settings"

import django

django.setup()

from onlineStoreApp.models import Product

products = Product.objects.exclude(image=None)

output_dir = 'C:\SuperMarker-Project\images-all'

os.makedirs(output_dir, exist_ok=True)


num = 0

for product in products:
    if num >= 1:
        break

    print('img url ', product.image)

    response = requests.get(product.image)
    print('response ', response)

    img = Image.open(BytesIO(response.content))
    print('img ', img)

    img = img.convert('RGB')

    img.resize((80, 80))

    filename = f"{product.catalog_number}.jpg"

    img.save(os.path.join(output_dir, filename))

    num += 1