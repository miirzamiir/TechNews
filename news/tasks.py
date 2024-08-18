from .utils.zoomit_crawler import ZoomitCrawler
from celery import shared_task

@shared_task
def crawl_zoomit_unseen_news():
    """ Celery task to call the zoomit crawler."""
    crawler = ZoomitCrawler()
    crawler.crawl_unseen_news()
    crawler.quit()
