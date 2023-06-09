from pathlib import Path
import re

import scrapy
from columbus.settings import MAX_DOCUMENTS_TO_PROCESS

from columbus.items import ProjectItem


class SthjjSpider(scrapy.Spider):
    name = "sthjj"
    count = 0
    documents_to_process = MAX_DOCUMENTS_TO_PROCESS

    def start_requests(self):
        urls = [
            "http://sthjj.pds.gov.cn/channels/11266.html",
        ]
        for url in urls:
            self.count = 0
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for project_url in response.xpath('//div[@class="xxgk"]//a/@href').getall():
            self.count+=1
            if self.count <= self.documents_to_process: 
                yield response.follow(project_url, callback = self.parse_project)

        is_enabled = not bool(response.css('a:contains("下一页"):not([disabled])'))

        if is_enabled and self.count <= self.documents_to_process:
            # Extract the link URL from the parent <a> element
            link_url = response.css('a:contains("下一页")::attr(href)').get()
            # Follow the link URL
            yield response.follow(link_url, callback=self.parse)

    def parse_project(self,  response):
        
        project_item = ProjectItem()
        project_item['company_name'] = response.css('div.teaser-logo-partner img::attr(title)').get()
        project_item['project_id'] = response.url.split("/")[-1]
        project_item['project_url'] = response.url
        project_item['title'] = response.css("h1::text").get() ## Done
        date_string = response.css("div.page-date::text").get()
        date_match = re.search(r'\d{4}-\d{2}-\d{2}', date_string)
        if date_match:
            project_item['last_modified_date'] = date_match.group()
        project_item['description'] = response.css('div.article ::text').getall()
        project_item['html_page'] = response.body
        # project_item['document_link'] = response.css("div.zip-download a::attr(href)").get()
        # Follow the document link and pass the project_item as a meta argument
        # yield response.follow(project_item['document_link'], callback=self.download_document, meta={'project_item': project_item})
        yield project_item
# 
    # def download_document(self, response):
        # project_item = response.meta['project_item']
        # project_item['document'] = response.body
        # project_item['document_type'] = response.headers.get('Content-Type').decode('utf-8').split('/')[-1]
        # project_item['document_name'] = response.url.split('/')[-1]
# 
        # yield project_item