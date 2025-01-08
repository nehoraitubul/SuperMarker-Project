from rest_framework.response import Response
from onlineStoreApp.models import Product, Price, Retailer
from onlineStoreApp.serializers.checkoutComparation import ProductSerializer
from rest_framework.decorators import api_view

@api_view(['GET'])
def get_retailers_with_products_and_prices(request):
    # Retrieve catalog numbers from query parameters
    catalog_numbers_param = request.query_params.get('catalog_numbers', '')
    catalog_numbers = [int(num) for num in catalog_numbers_param.split(',') if num.isdigit()]

    # Fetch all retailers
    retailers = Retailer.objects.all()

    # Initialize the response data
    response_data = {}

    # Iterate over each retailer
    for retailer in retailers:
        retailer_data = {
            'name': retailer.name,
            'last_scan': retailer.last_scan,
            'products': {}
        }

        # Iterate over each catalog number
        for catalog_number in catalog_numbers:
            product = Product.objects.filter(catalog_number=catalog_number).first()
            if product:
                price = Price.objects.filter(product_id=product.id, retailer_id=retailer.id).first()
                if price:
                    retailer_data['products'][catalog_number] = {
                        'price': price.price,
                        'unit_of_measure_price': price.unit_of_measure_price,
                        'unit_of_measure': price.unit_of_measure,
                        'units': price.units
                    }

        # Add retailer data to the response
        response_data[retailer.name] = retailer_data

    return Response({'retailers': response_data})