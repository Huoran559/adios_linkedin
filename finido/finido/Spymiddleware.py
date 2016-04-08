from scrapy.exceptions import IgnoreRequest
import re
from finido.required import required,location
class Custom(object):
    compiled = re.compile(required)
    def process_response(self,request,response,spider):
        if re.search(r'^https://www.linkedin.com/profile/view',response.url):
            locality = response.xpath('//span[@class="locality"]/a/text()').extract()
            if locality and locality[0].strip().lower() != location:
                print("Not of," + location)
                raise IgnoreRequest()
            else:
                req = response.xpath('//div[@id="background-experience"]/div/div/header/h4/a/text()').extract() +response.xpath('//div[@id="background-experience"]/div/div/header/h4/a/strong/text()').extract()
                if req:
                    for requ in req:
                        if re.search(self.compiled,requ.strip().lower()):
                            return response
                        else:
                            raise IgnoreRequest()
                else:
                    req = response.xpath('//div[@id="headline"]/p/text()').extract()
                    if req and re.search(self.compiled,req[0].strip().lower()):
                        return response
                    else:
                        raise IgnoreRequest()
        else:
                return response

