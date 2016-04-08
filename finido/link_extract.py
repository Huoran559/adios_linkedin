# -*- coding: utf-8 -*-
from scrapy.selector import Selector
import os
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(BASE_DIR, 'urls')
urls = set()

for html in glob.glob(os.path.join(path, '*.html')):
    response = Selector(text=open(html).read())
    href = response.xpath('//ol[@id="results"]/li[not(@class="mod paywall")]/a/@href').extract()
#this is for premium    href = response.xpath('//ul[@class="results"]/li[@class="entity"]/a/@href').extract()
    for link in href:
          if 'https://www.linkedin.com/profile/view?id=' in link:
                urls.add(link)

furl = open('./finido/urls.py','w')

furl.write('start_urls = [\n')
for url in urls:
    furl.write("'"+url+"'"+',\n')    
furl.write(']')

print('Extracted urls:',len(urls))
furl.close()            
        
        
        
        
    
        
        

