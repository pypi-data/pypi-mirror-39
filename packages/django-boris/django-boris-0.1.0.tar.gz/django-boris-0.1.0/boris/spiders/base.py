import logging
import socket
from io import BytesIO
from urllib.parse import urlparse

from bs4 import BeautifulSoup
import magic
from PIL import Image
import requests

from .exceptions import SpiderCrawlError, CapableSpiderNotFound


logger = logging.getLogger(__name__)
_registry = {}
_BLOCKED_DOMAINS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    socket.gethostbyname(socket.getfqdn())
]


def get_site_url(url):
    parsed = urlparse(url)
    return '{}://{}'.format(parsed.scheme, parsed.netloc)


class SpiderMeta(type):
    def __new__(meta, name, bases, class_dict):
        global _registry
        cls = type.__new__(meta, name, bases, class_dict)
        _registry[cls.__qualname__] = cls
        return cls


class Spider(object, metaclass=SpiderMeta):
    BASE_EXTRACTION_SCORE = 0
    USER_AGENT = 'Mozilla/5.0 Gecko/20100101 Firefox/63.0'
    CONTENT_TYPES = [
        'text/html', 'text/xhtml', 'text/xml',
        'application/rss+xml', 'application/atom+xml', 'application/xml'
    ]

    @classmethod
    def fetch(cls, url):
        response = requests.get(url, headers={'User-Agent': cls.USER_AGENT})
        response.raise_for_status()
        if cls.get_content_type(response) not in cls.CONTENT_TYPES:
            raise SpiderCrawlError(
                '{} return with an unacceptable content type'.format(url)
            )
        return response

    @classmethod
    def get_content_type(cls, response):
        if 'Content-Type' in response.headers:
            content_header = response.headers['Content-Type']
            return content_header and content_header.split(';')[0]

        with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as m:
            return m.id_buffer(response.content)

    @classmethod
    def make_image_buffer(cls, url, height=None, width=None):
        response = requests.get(url, headers={'User-Agent': cls.USER_AGENT})
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))

        buf = BytesIO()
        image.save(buf, 'PNG', height=height, width=width)
        buf.seek(0)
        return buf

    @classmethod
    def can_crawl_url(cls, url, **credentials):
        return False

    @classmethod
    def get_extraction_score(cls, url, **credentials):
        if not cls.can_crawl_url(url, **credentials):
            return 0

        return cls.BASE_EXTRACTION_SCORE

    @staticmethod
    def find_spider_classes(url, **credentials):
        parse_results = urlparse(url)
        url_scheme, url_domain = parse_results.scheme, parse_results.netloc

        if not url_scheme:
            raise ValueError('Missing URL Protocol schema')

        if url_domain in _BLOCKED_DOMAINS:
            raise ValueError('Invalid domain')

        candidates = [
            klass for klass in _registry.values()
            if klass.can_crawl_url(url, **credentials)
        ]
        return sorted(
            candidates,
            key=lambda k: float(k.get_extraction_score(url, **credentials))
        )

    @staticmethod
    def find_best_spider(url, **credentials):
        spider_classes = Spider.find_spider_classes(url, **credentials)
        try:
            spider_class = spider_classes[-1]
            return spider_class(url, **credentials)
        except IndexError:
            raise CapableSpiderNotFound('No spider for {}'.format(url))

    @staticmethod
    def make_spiders(url, **credentials):
        return [
            klass(url, **credentials)
            for klass in Spider.find_spider_classes(url, **credentials)
        ]

    @staticmethod
    def get_favicon(url, size=32):
        response = Spider.fetch(url)
        soup = BeautifulSoup(response.text, features='lxml')

        def make_icon(icon_url):
            return Spider.make_image_buffer(icon_url, 64, 64)

        def shortcut_attr():
            return make_icon(
                soup.find('link', rel='shortcut icon').attrs.get('href')
            )

        def icon_attr():
            return make_icon(
                soup.find('link', rel='icon').attrs.get('href')
            )

        def apple_icon():
            return make_icon(
                soup.find('link', rel='apple-touch-icon').attrs.get('href')
            )

        def hardcoded_url():
            return make_icon('{}/favicon.ico'.format(get_site_url(url)))

        for fn in [shortcut_attr, icon_attr, apple_icon, hardcoded_url]:
            try:
                return fn()
            except Exception as exc:
                logger.warn('Could not get favicon for {} via {}'.format(
                    url, fn.__name__)
                )
        return None

    def __init__(self, url, **credentials):
        self._url = url
        self._credentials = credentials
        self.extraction_score = self.__class__.get_extraction_score(url, **credentials)
        self._urlparse_results = urlparse(url)

    def crawl(self):
        raise NotImplementedError('Missing implementation of crawl method')

    @property
    def site(self):
        return get_site_url(self._url)

    @property
    def domain(self):
        return self._urlparse_results.netloc

    @property
    def url_path(self):
        return self._urlparse_results.path

    @property
    def name(self):
        return self.__class__.__qualname__
