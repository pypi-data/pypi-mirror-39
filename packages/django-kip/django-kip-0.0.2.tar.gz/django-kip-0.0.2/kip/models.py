import logging
import mimetypes
from io import BytesIO

from django.db import models
from ipfs_storage import InterPlanetaryFileSystemStorage
import lxml
from model_utils.models import TimeStampedModel
import requests

from boris.models import CrawledItem


logger = logging.getLogger(__name__)


class IPFSFile(TimeStampedModel):
    content = models.FileField(storage=InterPlanetaryFileSystemStorage())
    is_pinned = models.BooleanField(default=True)

    @property
    def url(self):
        return self.content and self.content.url

    @classmethod
    def make(cls, buf, name):
        storage = InterPlanetaryFileSystemStorage()
        return cls.objects.create(content=storage.save(name, buf))


class IPFSLink(TimeStampedModel):
    crawled_item = models.ForeignKey(
        CrawledItem, on_delete=models.PROTECT
    )
    document = models.ForeignKey(
        IPFSFile, on_delete=models.PROTECT, related_name='ipfs_page'
    )
    embedded_files = models.ManyToManyField(IPFSFile)

    @property
    def url(self):
        return self.document and self.document.url

    @classmethod
    def make(cls, crawled_item):
        content = crawled_item.extracted_content

        content_file = BytesIO(content.encode('utf-8'))

        ipfs_document = IPFSFile.make(content_file, crawled_item.title)
        ipfs_link = crawled_item.ipfslink_set.create(
            document=ipfs_document
        )

        html = lxml.html.fromstring(content)
        image_urls = html.xpath('//img/@src')
        link_urls = html.xpath('//a/@href')

        for url in image_urls + link_urls:
            mimetype, _ = mimetypes.guess_type(url)
            if mimetype and 'image' in mimetype:
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    ipfs_image = IPFSFile.make(BytesIO(response.content), url)
                    ipfs_link.embedded_files.add(ipfs_image)
                except requests.HTTPError as exc:
                    logger.error('Failed to download {}: {}'.format(url, exc))

        return ipfs_link
