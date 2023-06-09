# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ColumbusItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ProjectItem(scrapy.Item):
    """Scrapy item of project

    Args:
        scrapy (_type_): _description_
    """
    project_id = scrapy.Field()
    project_url = scrapy.Field()
    title = scrapy.Field()
    last_modified_date = scrapy.Field()
    description = scrapy.Field()
    html_page = scrapy.Field()
    ## zip or pdf document
    document = scrapy.Field()
    metadata = scrapy.Field()
    document_link = scrapy.Field()
    document_type = scrapy.Field()
    document_name = scrapy.Field()
