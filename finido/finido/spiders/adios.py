# -*- coding: utf-8 -*-
from finido.crawl import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request, FormRequest
import re
import datetime 
from finido.items import FinidoItem
from scrapy.exceptions import CloseSpider
from finido.urls import start_urls
from finido.accounts import accounts
from finido.required import required1,required2,required3
from scrapy.conf import settings

class AdiosSpider(CrawlSpider):
    name = "adios"
    allowed_domains = ["linkedin.com"]
    login_page = 'http://www.linkedin.com/'
    visited = dict()
    pprojects = []
    crawled = 0
    if settings.get('follow_rules',False):
        rules = [Rule( 
                 LinkExtractor(
                                allow=(),
                                restrict_xpaths = ('//div[@class="insights-browse-map"]')
                               ),
                
                 callback='parse_start_url',
                 follow=True
                    ),
            ]   

    pattern1 =  re.compile(required1)
    pattern2 = re.compile(required2)
    pattern3 = re.compile(required3)
    
    
    def start_requests(self):
        self.gen = self.gen_req()
        self.length = len(accounts)
        self.start_length = len(start_urls)
        print( '========================================INIT================================================')
        yield Request(url=self.login_page, callback=self.login, dont_filter=True)
      
    def login(self, response):
        requests = []
            
        for account in accounts:
            request = FormRequest.from_response(
                                               response,
                                               formdata={'session_key': account[0], 'session_password': account[1]},
                                               callback=self.check_login,
                                               dont_filter = True,priority=5,
                                          )
            print('[+] Signing In with',account[0]) 
            yield request

    def gen_req(self):
        req = []
        count = 0
        for urls in start_urls:
            yield urls
    
    def check_login(self,response):
        if "sign out" in response.body.lower():
          user = response.xpath('//a[@class="act-set-name-split-link"]/text()').extract()
          print("[+] Succesfully LoggedIn!" + user[0])
          n= 0
          calls = self.start_length/self.length
          while n < calls:
                n += 1
                try:
                    req = self.gen.next()
                except StopIteration:
                    print('[+] created start requests')
                    break
                else:
                    yield Request(url = req,priority=3) 
          
        else:
              print('[!] Login Failed!!')

    def ex_parser(self, response ):
          container = response.xpath('//div[@id="background-experience"]')
          workField = container.xpath('div/div')
          current = container.xpath('./div[@class = "editable-item section-item current-position"]/div/header')
          current_h4 = current.xpath('h4')
          current_position = current_h4.xpath('./a/text()').extract()
          current_company = current_h4.xpath('./following-sibling::h5/a/text()').extract() + current_h4.xpath('./following-sibling::h5/span/strong/a/text()').extract()
          companies_workField = workField.xpath('header/h4/following-sibling::h5')
          companies_worked = companies_workField.xpath('a/text()').extract() + companies_workField.xpath('span/strong/a/text()').extract()
          comp_cont = container.xpath('./div[not(@class="editable-item section-item current-position")]/div/header')
          companies_worked_positions = comp_cont.xpath('./h4/a/text()').extract()
          try:
            dates,exk,__current = self._find_required(current,current_position,comp_cont,companies_worked_positions)
          except TypeError:
            print('entered this')
            return False
          else:
            print('[+] scraping started!!')
            _date = self.set_time(dates)
            work_experience = self.time_calc(_date)
            print('-------------------------------------------------')
            print(companies_worked,work_experience,current_company,exk,__current)
            return companies_worked,work_experience,current_company,exk,__current
          
              
    def _find_required(self,current,current_position,comp_cont,companies_worked_positions):
          self.pprojects = []     
          val = False  
          _dates = [] 
          _project = []
          __current = []
          exk = set()
          
          
          if current_position:
              for i in range(len(current_position)):
                  if re.search(self.pattern1,current_position[i].strip().lower()):        
                      val = True  
                      time = current[i].xpath('./following-sibling::span[@class="experience-date-locale"]/time/text()').extract()
                      if time: 
                        _dates.append(time)                  
                      pro = current[i].xpath('./following-sibling::dl[@class="education-associated"]/dt[@data-trk-code="prof-exp-project-open"]/following-sibling::dd[1]/ul/li/h6/span/text()').extract()
                      _project += pro
                      __current.append(current_position[i])
                            
                  elif re.search(self.pattern2,current_position[i].strip().lower()):
                       time = current[i].xpath('./following-sibling::span[@class="experience-date-locale"]/time/text()').extract()
                       text = current[i].xpath('./following-sibling::p/text()').extract()
                       print(text)
                       if text:
                          if re.search(self.pattern1,text[0].lower()):
                            val = True
                            if time:
                                _dates.append(time)
                            pro = current[i].xpath('./following-sibling::dl[@class="education-associated"]/dt[@data-trk-code="prof-exp-project-open"]/following-sibling::dd[1]/ul/li/h6/span/text()').extract()          
                            _project += pro 
                            __current.append(current_position[i])  
                       else:
                            val = True
                            if time:
                                _dates.append(time)
                            pro = current[i].xpath('./following-sibling::dl[@class="education-associated"]/dt[@data-trk-code="prof-exp-project-open"]/following-sibling::dd[1]/ul/li/h6/span/text()').extract()          
                            _project += pro 
                            __current.append(current_position[i])
                  elif re.search(self.pattern3,current_position[i].strip().lower()):                    
                        text = current[i].xpath('./following-sibling::p/text()').extract()
                        if text and re.search(self.pattern1,text[0].lower()):
                                 val = True
                                 pro = current[i].xpath('./following-sibling::dl[@class="education-associated"]/dt[@data-trk-code="prof-exp-project-open"]/following-sibling::dd[1]/ul/li/h6/span/text()').extract()
                                 time = current[i].xpath('./following-sibling::span[@class="experience-date-locale"]/time/text()').extract()
                                 if time: 
                                    _dates.append(time)
                                 _project += pro
                                 __current.append(current_position[i])
                  else:
                        exk.add(current_position[i].strip())
          else:
                val = True 
 
          if val and companies_worked_positions:
              
              for i in range(len(companies_worked_positions)):
                    if re.search(self.pattern1,companies_worked_positions[i].strip().lower()):        
                       time = comp_cont[i].xpath('./following-sibling::span[@class="experience-date-locale"]/time/text()').extract()
                       val = True
                       if time:
                                _dates.append(time)
                       pro = comp_cont[i].xpath('./following-sibling::dl[@class="education-associated"]/dt[@data-trk-code="prof-exp-project-open"]/following-sibling::dd[1]/ul/li/h6/span/text()').extract()          
                       _project += pro   
                    elif re.search(self.pattern2,companies_worked_positions[i].strip().lower()):
                       time = comp_cont[i].xpath('./following-sibling::span[@class="experience-date-locale"]/time/text()').extract()
                       text = comp_cont[i].xpath('./following-sibling::p/text()').extract()
                       
                       if text:
                         if re.search(self.pattern1,text[0].lower()):
                            val = True
                            if time:
                                _dates.append(time)
                            pro = comp_cont[i].xpath('./following-sibling::dl[@class="education-associated"]/dt[@data-trk-code="prof-exp-project-open"]/following-sibling::dd[1]/ul/li/h6/span/text()').extract()          
                            _project += pro   
                       else:
                           val = True
                           if time:
                                _dates.append(time)
                           pro = comp_cont[i].xpath('./following-sibling::dl[@class="education-associated"]/dt[@data-trk-code="prof-exp-project-open"]/following-sibling::dd[1]/ul/li/h6/span/text()').extract()          
                           _project += pro 
                    elif re.search(self.pattern3,companies_worked_positions[i].strip().lower()):
                        
                        text = comp_cont[i].xpath('./following-sibling::p/text()').extract()
                        if text and re.search(self.pattern1,text[0].lower()):
                             val = True
                             time = comp_cont[i].xpath('./following-sibling::span[@class="experience-date-locale"]/time/text()').extract()
                             if time:
                                _dates.append(time)
                             pro = comp_cont[i].xpath('./following-sibling::dl[@class="education-associated"]/dt[@data-trk-code="prof-exp-project-open"]/following-sibling::dd[1]/ul/li/h6/span/text()').extract()
                             _project += pro
                    
                    else:
                          exk.add(companies_worked_positions[i].strip()) 
          if val:
            self.pprojects += _project
            exk = list(exk)  
            return _dates,exk,__current
          


    def set_time(self,dates):
      _date = []
      for y in dates:
          if len(y)<2:
             try:
                _date.append((datetime.datetime.strptime(y[0].strip(),"%B %Y").date(),datetime.date.today()))
             except:
                try:
                    _date.append((datetime.datetime.strptime(y[0].strip(),"%Y").date(),datetime.date.today()))
                except:
                    print('[!!] No experience time in the profile')
          else:
              try:
                _date.append((datetime.datetime.strptime(y[0].strip(),"%B %Y").date(),datetime.datetime.strptime(y[1].strip(),"%B %Y").date()))
              except:
                 try:
                    _date.append((datetime.datetime.strptime(y[0].strip(),"%Y").date(),datetime.date.strptime(y[1].strip(),"%Y").date()))
                 except:
                    try:
                       _date.append((datetime.datetime.strptime(y[0].strip(),"%Y").date(),datetime.date.strptime(y[1].strip(),"%B %Y").date()))
                    except:
                        try:
                           _date.append((datetime.datetime.strptime(y[0].strip(),"%B %Y").date(),datetime.date.strptime(y[1].strip(),"%Y").date()))
                        except:
                           print('[!!] No experience time in the profile')
      return _date

    def time_calc(self,times):
        times.sort()
        sub=0
        seconds=0
        for i in range(len(times)):
               if times[i][1] == datetime.date.today() or times[i][1] == times[-1][1]:
                       seconds = (times[i][1]-times[0][0]).total_seconds()-sub
               else:
                       if (times[i+1][0]-times[i][1]).total_seconds() > 0:
                            sub+=(times[i+1][0]-times[i][1]).total_seconds()  
                       else:
                            continue
        return seconds/(3600*24*365)   
    
    def projects(self,response):
        project_container = response.xpath('//div[@id = "background-projects"]')
        no_of_projects = 0
        hgroup = project_container.xpath('./div/div/hgroup')
        _project = [] 
        for hgr in hgroup:
            project_headers = hgr.xpath('./h4/a/span[@dir="auto"]/text()').extract() + hgr.xpath('./h4/span[@dir="auto"]/text()').extract()
            pro = hgr.xpath('./following-sibling::p[@class="description summary-field-show-more"]/text()').extract()
            if re.search(self.pattern1,project_headers[0].strip().lower()):
                _project.append(project_headers[0].strip())
            elif pro and re.search(self.pattern1, pro[0].strip().lower()):
                _project.append(project_headers[0].strip())
            else:
                continue
        s = set(self.pprojects + _project)
        no_of_projects = len(s)
        print(no_of_projects)   
        return no_of_projects
    
    def endorsements(self,response):
        endorsements = []
        for en in response.xpath('//span[@class="skill-pill"]'):
            a = en.xpath('a/span/text()').extract()
            b = en.xpath('span/a/text()').extract()
            if a:
               a = int(a[0].replace('+','').strip())
            else:
                a=0
            if b:
               b = b[0]
            else:
               b=None
            endorsements.append((a,b))
        endorsements.sort(reverse=True)
        endorsed = 0
        high = 0
        highest = []
        for ele in endorsements:
            if re.search(self.pattern1,ele[1].lower()):
                endorsed += ele[0]
            if ele[0]>high:
                high = ele[0]
                highest.append((ele[0],ele[1]))
        return endorsements,endorsed,highest
    
    def recommendations(self,response):
        rec = response.xpath('//div[@class="endorsements-received"]/ol/li').xpath('.//div[@class="endorsement-full"]')
        no_of_recommendations = len(rec)
        print(no_of_recommendations)  
        return no_of_recommendations
    
    def connections(self,response):
        connections = response.xpath('//a[@class="connections-link"]/text()').extract()
        if connections:
            return connections[0]
        connections = response.xpath('//div[@class="member-connections"]/strong/text()').extract()
        if connections:
           return connections[0]
         
    def contacts(self,response):
        container =  response.xpath('//div[@id="contact-info-section"]')
        contacts =  container.xpath('table').xpath('.//td/div/div/ul/li/text()').extract()
        email = ''
        links = []
        absolute = []
        for i in container.xpath('table').xpath('.//td/div/div/ul/li/a/@href').extract():
            if 'mailto:' in i:
                email = i.split(':')[1]
                continue
           
            links.append(response.urljoin(i))
        absolute.append(email)
        absolute += contacts
        return absolute,links
    
    
    def honors(self,response):
        container =  response.xpath('//div[@id="background-honors"]')
        honors = container.xpath('div')
        return len(honors)


    def _name(self,response):
        _name = response.xpath('//span[@class="full-name"]/text()').extract()   
        return _name     

  
    def linkedin(self,response):
        linkedin = response.xpath('//a[@class="view-public-profile"]/text()').extract()
        if linkedin:
            linkedin =  linkedin[0]
        else:
            linkedin = response.url
        return linkedin  
    
    def certifications(self,response):
        container = response.xpath('//div[@id="background-certifications"]')
        certifications = []
        cer = container.xpath('./div/div')
        for c in cer:
            field = c.xpath('./hgroup/h4/a/text()').extract()
            if field:
                certifications.append((field[0]))
        return certifications

    def degree(self,response):
        degree = response.xpath('//abbr[@class="degree-icon"]/text()').extract()
        if degree:
            return container[0].strip()
        
    def find_preference(self,ex,p,c,r,h,e):
        if ex>=5:
            ex=5
        elif ex>=4:
            ex=4
        elif ex>=3:
            ex=3
        elif ex>=2:
            ex=2
        elif ex>=1:
            ex= 1
        else:
            ex= 0.5
        
        if p>=10:
            p=5
        elif p>=8:
            p=4
        elif p>=6:
            p=3
        elif p>=4:
            p=2
        elif p>=2:
            p = 1
        elif p>=1:
            p= 0.5
        else:
            p=0

        try:        
            c = int(c.replace('+','').strip())
        except:
            print('check this url')
            c = int(input('Enter the connections.!!!ONLY INTEGERS'))
        else:
            if c>=500:
                c = 5
            elif c>=400:
                c= 4
            elif c>=300:
                c=3
            elif c>=200:
                c=2
            elif c>=100:
                c=1
            else:
                c = 0.5 
        if r>0:
            r=5
        else:
            r= 0
        if h>0:
            h=5
        else:
            h=0
        
        if e>=10:
            e=5
        elif e>=8:
            e=4
        elif e>=6:
            e=3
        elif e>=4:
            e=2
        elif e>=2:
            e = 1
        elif e>=1:
            e= 0.5
        else:
            e=0
        numerator = ex*40+p*40+c*5+r*5+h*5+e*5
        denomerator = 500
        preference = (float(numerator)/denomerator)*5
        return preference

    def summary_and_additional_info(self,response):
         def check(data):
            try:
                float(data);return False
            except ValueError:
                return True
         datas = response.xpath('//div[@id="summary-item"]/div[@id="summary-item-view"]/div[@class="summary"]/p/text()').re(ur'([a-zA-Z0-9-_.]+@[a-zA-Z0-9]+?[.][a-z0-9.]+|[htpsf:/0-9]*[a-z0-9]+[.][a-z0-9A-Z/.]+)')+response.xpath('//div[@id="background-additional-info"]/li[@id="contact-comments"]/div/p/text()').re(ur'([a-zA-Z0-9-_.]+@[a-zA-Z0-9]+?[.][a-z0-9.]+|[htpsf:/0-9]*[a-z0-9]+[.][a-z0-9A-Z/.]+)')
         return [data for data in datas if check(data)]
    
    def parse_start_url(self,response):
        self.crawled += 1
        linkedin = self.linkedin(response)

#       Set crawling limit here       

#        if self.crawled >= 600:
#               raise CloseSpider(reason = 'Crawled More than 100')
        if self.visited.get(linkedin,0)==0 :
            self.visited[linkedin]=1
            try:
                companies,experience,currentComp,exk,__current = self.ex_parser(response)
            except TypeError:
                if self.degree(response) == '3':
                    print('****the connection is 3rd degree******')
                    fhand = open('3.txt','a')
                    fhand.write(response.url + '\n')
                    fhand.close()
                else:
                    print('Nope')
            else:
                projects = self.projects(response)
                endorsements,endorsed,highest = self.endorsements(response)
                recommendations = self.recommendations(response)
                connections = self.connections(response)
                contacts,links = self.contacts(response)
                certifications = self.certifications(response)
                honors = self.honors(response)
                _name = self._name(response)
                preference = self.find_preference(experience,projects,connections,recommendations,honors,endorsed)
                additional = self.summary_and_additional_info(response)
                if preference<3 and experience > 5:
                    flag = 1
                else:
                    flag = ''    
                _items = FinidoItem()
                _items["name"] =  _name
                _items["experience"] = experience
                _items["projects"] = projects
                _items["connections"] = connections
                _items["recommendations"] = recommendations
                _items["honors"] = honors
                _items['endorsed'] =  endorsed
                _items['preference'] = preference
                _items["extraKnowledge"] = exk
                _items["linkedin_link"]= linkedin
                _items["contacts"] = contacts
                _items["links"] = links
                _items["currentposition"] = __current
                _items["currentCompany"] = currentComp
                _items['flag'] = flag
                _items["companies"] = companies
                _items['highest_endorsed'] = highest
                _items['certifications'] = certifications
                _items["endorsements"] = endorsements
                _items["additional_info"] = additional
                yield _items
