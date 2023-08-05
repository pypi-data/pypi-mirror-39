import logging
from urllib.parse import urlparse

from django.db import models
from django.db.models import Max
from html_sanitizer.django import get_sanitizer
from model_utils import Choices
from model_utils.models import TimeStampedModel

from .spiders import Spider, CapableSpiderNotFound, SpiderCrawlError


logger = logging.getLogger(__name__)


SITE_CRAWLING_FREQUENCIES = Choices(
    (30, 'half_minute', 'half_minute'),
    (60, 'minute', 'minute'),
    (15 * 60, 'quarter_hourly', 'quarter_hourly'),
    (60 * 60, 'hourly', 'hourly')
)


class Site(models.Model):
    domain = models.URLField(unique=True, editable=False)
    favicon = models.ImageField(null=True, blank=True, upload_to='favicons')
    crawling_frequency = models.PositiveIntegerField(
        choices=SITE_CRAWLING_FREQUENCIES,
        default=SITE_CRAWLING_FREQUENCIES.half_minute
    )

    @property
    def last_crawled(self):
        return self.link_set.select_related('crawleditem').aggregate(
            last_crawled=Max('crawleditem__created')
        ).get('last_crawled')

    def update_favicon(self):
        logger.info('Updating favicon for {}'.format(self))
        try:
            buf = Spider.get_favicon(self.domain)
            if buf:
                self.favicon.save('{}.png'.format(self.id), buf)
        except Exception as exc:
            logger.exception(exc)

    @classmethod
    def make(cls, url):
        parsed = urlparse(url)
        website_url = '{}://{}/'.format(parsed.scheme, parsed.netloc)
        site, _ = cls.objects.get_or_create(domain=website_url)
        return site

    def __str__(self):
        return self.domain


class Link(models.Model):
    site = models.ForeignKey(Site, on_delete=models.PROTECT)
    url = models.URLField(unique=True, editable=False)

    def crawl(self):
        try:
            for spider in Spider.make_spiders(self.url):
                if self.crawleditem_set.filter(spider_name=spider.name).exists():
                    logger.info('{} crawled this link already'.format(spider.name))
                    continue

                logger.info('Crawling link {} with {}'.format(self, spider.name))
                results = spider.crawl()
                sanitizer = get_sanitizer()

                extracted_html = results.get('extracted_content') or ''

                item = self.crawleditem_set.create(
                    title=results.get('title'),
                    original_content=results.get('original_content'),
                    extracted_content=sanitizer.sanitize(extracted_html),
                    extraction_score=results.get('extraction_score', spider.extraction_score),
                    spider_name=spider.name
                )
                lead_image = results.get('lead_image')
                if lead_image:
                    item.lead_image.save('{}.png'.format(self.id), lead_image)
        except (CapableSpiderNotFound, SpiderCrawlError) as exc:
            logger.warn(str(exc))

    def __str__(self):
        return self.url

    @property
    def best_extraction(self):
        return self.crawleditem_set.order_by('-extraction_score').first()

    @property
    def title(self):
        return self.best_extraction and self.best_extraction.title

    @classmethod
    def make(cls, url):
        site = Site.make(url)
        link, _ = cls.objects.get_or_create(url=url, defaults={
            'site': site
        })
        return link


class CrawledItem(TimeStampedModel):
    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    lead_image = models.ImageField(null=True, editable=False, upload_to='leads')
    title = models.TextField(null=True, editable=False)
    original_content = models.TextField(null=True, editable=False)
    extracted_content = models.TextField(null=True, editable=False)
    extraction_score = models.FloatField(default=0)
    spider_name = models.CharField(max_length=512, db_index=True)

    class Meta:
        unique_together = ('link', 'spider_name')
