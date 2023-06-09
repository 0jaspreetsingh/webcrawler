from pathlib import Path
import re

import scrapy
from columbus.settings import MAX_DOCUMENTS_TO_PROCESS

from columbus.items import ProjectItem


class UvpSpider(scrapy.Spider):
    name = "uvp"
    count = 0
    documents_to_process = MAX_DOCUMENTS_TO_PROCESS

    def start_requests(self):
        urls = [
            "https://www.uvp-verbund.de/freitextsuche?rstart=0&currentSelectorPage=1",
        ]
        for url in urls:
            self.count = 0
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for project in response.css("div.teaser-data"):
            self.count+=1
            project_url = project.css('a::attr(href)').get()
            if self.count <= self.documents_to_process: 
                yield response.follow(project_url, callback = self.parse_project)

        # Find the <a> element with the desired <span> child
        link_selector = response.css('a.icon.small-button span.ic-ic-arrow-right').xpath('parent::a')

        if link_selector and self.count <= self.documents_to_process:
            # Extract the link URL from the parent <a> element
            link_url = link_selector.css('::attr(href)').get()
            # Follow the link URL
            yield response.follow(link_url, callback=self.parse)

    def parse_project(self,  response):
        
        project_item = ProjectItem()
        project_item['company_name'] = response.css('div.teaser-logo-partner img::attr(title)').get()
        project_item['project_id'] = response.url.split("=")[-1]
        project_item['project_url'] = response.url
        project_item['title'] = response.css("h1::text").get()
        date_string = response.css("div.date span::text").get()
        date_match = re.search(r'\d{2}\.\d{2}\.\d{4}', date_string)
        if date_match:
            project_item['last_modified_date'] = date_match.group()
        project_item['description'] = response.css('h3:contains("Allgemeine Vorhabenbeschreibung")').xpath('parent::div').css('p::text').getall()
        project_item['html_page'] = response.body
        project_item['document_link'] = response.css("div.zip-download a::attr(href)").get()
        # Follow the document link and pass the project_item as a meta argument
        yield response.follow(project_item['document_link'], callback=self.download_document, meta={'project_item': project_item})

    def download_document(self, response):
        project_item = response.meta['project_item']
        project_item['document'] = response.body
        project_item['document_type'] = response.headers.get('Content-Type').decode('utf-8').split('/')[-1]
        project_item['document_name'] = response.url.split('/')[-1]

        yield project_item