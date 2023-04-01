from bs4 import BeautifulSoup
import pandas as pd
import requests
# import urllib.request
# import gzip
# import io

# import urllib.request as urllib2
import json
import gzip
import io

import urllib.request


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


    # outFile = io.StringIO()

    # # Set the URL for the gzipped file
    # url = 'http://pricesprodpublic.blob.core.windows.net/pricefull/PriceFull7290027600007-413-202304010340.gz?sv=2014-02-14&sr=b&sig=zJ5Mr3ef18UjO0a%2F%2Bh0rzLWWMZUoMNDLN2TzWOEUQSk%3D&se=2023-04-01T19%3A43%3A38Z&sp=r'
    # # Send a request to the URL and get the gzipped data
    # response = urllib.request.urlopen(url)
    #
    # # Read the gzipped data into memory
    # compressed_file = io.BytesIO(response.read())
    # print(compressed_file)
    #
    # # Decompress the gzipped data
    # decompressed_file = gzip.GzipFile()
    # print(type(decompressed_file))
    #
    # with gzip.open(decompressed_file, mode='rb') as f:
    #     file_content = f.read()
    #     print(file_content)
    #
    # # Read the XML data using pandas
    # # xml_data = pd.read_xml(decompressed_file)
    #
    # # Print the XML data
    # # print(xml_data)

    # url = 'http://pricesprodpublic.blob.core.windows.net/pricefull/PriceFull7290027600007-413-202304010340.gz?sv=2014-02-14&sr=b&sig=zJ5Mr3ef18UjO0a%2F%2Bh0rzLWWMZUoMNDLN2TzWOEUQSk%3D&se=2023-04-01T19%3A43%3A38Z&sp=r'
    # page = urllib2.urlopen(url)
    # gzip_filehandle = gzip.GzipFile(fileobj=io.BytesIO(page.read()))
    # print(gzip_filehandle)
    # json_data = json.loads(gzip_filehandle.read())
    # print(json_data)

    response = urllib.request.urlopen('http://pricesprodpublic.blob.core.windows.net/pricefull/PriceFull7290027600007-413-202304010340.gz?sv=2014-02-14&sr=b&sig=I0u4mqYQtGoQFf%2FHDNFq0tI5WTPM4nbb1od0DPXqzYk%3D&se=2023-04-01T20%3A21%3A51Z&sp=r')
    with gzip.GzipFile(fileobj=response) as f:
        # df = pd.read_xml(f.read(), compression='gzip')
        xml_parser = BeautifulSoup(open(f), 'xml')
    # # df = pd.read_xml(f ,  parser='lxml', compression='gzip')
    # pd.set_option('display.max_columns', None)  # show all columns
    # pd.set_option('display.max_rows', None)  # show all rows
    # print(df)


