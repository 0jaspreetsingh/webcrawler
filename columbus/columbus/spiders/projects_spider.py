from pathlib import Path

import scrapy


class ProjectsSpider(scrapy.Spider):
    name = "projects"
    count = 0

    def start_requests(self):
        urls = [
            "https://www.uvp-verbund.de/freitextsuche?rstart=0&currentSelectorPage=1",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.count+=1
        for project in response.css("div.teaser-data"):
            project_url = project.css('a::attr(href)').get()
            yield response.follow(project_url, callback = self.parse_project)
            print(project.css("h2.header::text").get())

        # Find the <a> element with the desired <span> child
        link_selector = response.css('a.icon.small-button span.ic-ic-arrow-right').xpath('parent::a')

        if link_selector and self.count< 3:  ## TODO: process only first 25 projects
            # Extract the link URL from the parent <a> element
            link_url = link_selector.css('::attr(href)').get()

            # Follow the link URL
            yield response.follow(link_url, callback=self.parse)
        # page = response.url.split("/")[-2]
        # filename = f"projects-{page}.html"
        # Path(filename).write_bytes(response.body)
        # self.log(f"Saved file {filename}")

    def parse_project(self,  response):
        print(response.body)