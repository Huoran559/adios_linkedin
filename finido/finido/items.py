# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FinidoItem(scrapy.Item):
    experience = scrapy.Field()
    companies  = scrapy.Field()
    connections = scrapy.Field()
    projects  = scrapy.Field()
    recommendations = scrapy.Field()
    endorsements = scrapy.Field()
    contacts = scrapy.Field()
    honors = scrapy.Field()
    currentCompany = scrapy.Field()
    name = scrapy.Field()
    extraKnowledge = scrapy.Field()
    linkedin_link = scrapy.Field()
    links = scrapy.Field()
    currentposition = scrapy.Field()
    endorsed = scrapy.Field()
    highest_endorsed = scrapy.Field()
    certifications = scrapy.Field()
    preference = scrapy.Field()
    flag = scrapy.Field()
    additional_info = scrapy.Field()
    github_or_bitbucket_link = scrapy.Field()
    stackoverflow_link = scrapy.Field() 
    no_of_repo = scrapy.Field()
    no_of_answers = scrapy.Field()
