# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
from itemadapter import ItemAdapter
import json
from scrapy.exporters import JsonItemExporter
import zipfile
from columbus.settings import OUT_DIR

class ColumbusPipeline:
    def process_item(self, item, spider):
        return item 

class HtmlPipeline:
    """save project's html file to local file system
    """
    def process_item(self, item, spider):
        project_id = item['project_id']
        html_page = item['html_page']
        domain = item['project_url'].split('/')[2]
        directory =  os.path.join(OUT_DIR,domain, project_id)
        os.makedirs(directory, exist_ok=True)

        # Save the HTML document to the directory
        html_document_path = os.path.join(directory, f'document.html')
        with open(html_document_path, 'wb') as f:
            f.write(item['html_page'])

        return item
    
class MetadataPipeline:
    """save metadata to local fle system
    """
    def process_item(self, item, spider):
        project_id = item['project_id']
        domain = item['project_url'].split('/')[2]
        directory = os.path.join(OUT_DIR,domain, project_id)
        meta_info_path = os.path.join(directory, 'Meta Information')
        os.makedirs(meta_info_path, exist_ok=True)
        
        with open(f'{meta_info_path}/info.json' , 'w') as f:
            meta_data = {
                'project_id': item['project_id'],
                'title': item['title'],
                'last_modified_date': item['last_modified_date'],
                'description': item['description'],
                'company_name': item['company_name']
            }
            if item.get('document_link'):
                meta_data['document_link'] = item['document_link']
            json.dump(meta_data, f, sort_keys=True, indent=4)

        return item


class DocumentPipeline:
    """save documents downloaded and unzips
    """
    def process_item(self, item, spider):
        project_id = item['project_id']
        domain = item['project_url'].split('/')[2]
        directory = os.path.join(OUT_DIR,domain, project_id)

        # Save document
        if item.get('document'):
            document_path = os.path.join(directory, 'Zip')
            os.makedirs(document_path, exist_ok=True)
            doc_path = f"{document_path}/{item['document_name']}"
            with open(doc_path, 'wb') as f:
                f.write(item['document'])
            if item['document_type'].startswith('zip'):
                # Unzip the file
                with zipfile.ZipFile(doc_path, 'r') as zip_ref:
                    # Extract the contents of the zip file to a directory
                    zip_ref.extractall(document_path)

        return item
