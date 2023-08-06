import logging

from celery import shared_task

from boris.models import CrawledItem
from .models import IPFSLink


logger = logging.getLogger(__name__)


@shared_task
def save_items_to_ipfs():
    for item in CrawledItem.objects.filter(ipfslink__isnull=True):
        logger.info('Saving {} to IPFS'.format(item))
        IPFSLink.make(item)
