from bs4 import BeautifulSoup
import pandas as pd
import requests
import urllib.request
import gzip
import io

# http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=0&storeId=413



if __name__ == '__main__':

    # response = requests.get('http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=0&storeId=413')
    #
    # soup = BeautifulSoup(response.text, 'html.parser')
    #
    # price_full_url = soup.find("td", string='pricefull')
    # a = price_full_url.parent
    # print('price full data link:')
    # print(a.find('a')['href'])
    #
    # promo_full_url = soup.find("td", string='promofull')
    # a = promo_full_url.parent
    # print('promos full data link:')
    # print(a.find('a')['href'])


    outFile = io.StringIO()

    # Set the URL for the gzipped file
    url = 'http://pricesprodpublic.blob.core.windows.net/pricefull/PriceFull7290027600007-413-202303300340.gz?sv=2014-02-14&sr=b&sig=cydmUqV%2BjfGzgw9eI%2FEl5O562EMZbyOM77cT8u87Z7I%3D&se=2023-03-30T16%3A19%3A05Z&sp=r'
    # Send a request to the URL and get the gzipped data
    response = urllib.request.urlopen(url)

    # Read the gzipped data into memory
    compressed_file = io.BytesIO(response.read())
    print(compressed_file.read())

    # Decompress the gzipped data
    decompressed_file = gzip.GzipFile(fileobj=compressed_file)
    print(decompressed_file)

    # Read the XML data using pandas
    xml_data = pd.read_xml(decompressed_file)n

    # Print the XML data
    print(xml_data)