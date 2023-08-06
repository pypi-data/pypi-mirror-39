from urllib.parse import urlparse

from mercury_parser.client import MercuryParser

from ..app_settings import get_setting
from .base import Spider


MERCURY_PARSER_KEY = get_setting('MERCURY_PARSER_KEY', None)


class MercuryReaderSpider(Spider):
    BASE_EXTRACTION_SCORE = 0.5

    CONTENT_TYPES = ['text/html', 'text/xhtml']

    @classmethod
    def can_crawl_url(cls, url, **credentials):
        return bool(MERCURY_PARSER_KEY) and bool(urlparse(url).path.strip('/'))

    def crawl(self):
        parser = MercuryParser(MERCURY_PARSER_KEY)
        response = parser.parse_article(self._url)
        data = response.json()
        lead_image_url = data['lead_image_url']
        lead_image = lead_image_url and Spider.make_image_buffer(lead_image_url)

        data.update({
            'extracted_content': data['content'],
            'lead_image': lead_image
        })

        return data
