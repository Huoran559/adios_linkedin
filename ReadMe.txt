First save the search results in urls folder.
Go to this folder from command line.
Then type python link_extract.py
  -> This will create urls.py file inside finido folder.
  -> This is your start_urls
The to start the crawl type "scrapy crawl adios" this will only crawl, not save the data. 
To save the data and crawl type "scrapy crawl adios -o data.csv" Here -o [...] represents output file. At present the program is customized for csv files.


--------Playing with the settings-----------
-> In settings file if you set follow_rules to True. Then the crawler will crawl the links extracted from a certain profile i.e. people also viewed
   links.(This is not recommended unless you have very less start urls numbers)

----------required.py------------
-> In required.py file you define your required fields. They must be regular expressions. Further details are enlisted there.

----------accounts.py--------
-> In this file you define the accounts to crawl linkedin profiles.
-> You can have multiple accounts crawling at the same time.
    -> In case of this, the start_urls requests are divided for different accounts.


--------------------Quality of crawl-----------------------
-> The quality of crawl pretty much depends on the start urls provided.
-> Better the start urls better the crawled datas


----------------Further Improvements------------------------
-> The crawler at present does not solve captchas. Linkedin generally throws captchas of identifying photos. To solve this a manual touch is must.
-> However, what the crawler may do is to login with different account when it is provided with captchas.



----------------------link_extract.py----------------------
-> This file extracts the links from the save searched results.
-> If the search results are from linkedin premium account's sales navigator then minor changes must be made in this file. (The process is listed in it)
-> However, the sales navigator search results should not be accessed from a premium account as it loads the page provided by the sales navigator which loads content by executing script which is not done by the scraper. (It can be done by using a webdriver element. At present it is not done by the program)
 
