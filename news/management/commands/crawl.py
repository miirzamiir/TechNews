from django.core.management.base import BaseCommand
from ...utils.zoomit_crawler import ZoomitCrawler

class Command(BaseCommand):
    """
    Custom Django command for crawling news and saving it to the database.

    Attributes:
        help: A description of what the command does and how to use it.
    """
    help = """Crawls news from https://zoomit.ir and save to the database.
              Example: python3 manage.py crawl 1 3 --> Crawls zoomit news archive from page 1 to page 3."""

    def add_arguments(self, parser) -> None:
        """Adds arguments to the command parser for specifying the page range."""

        parser.add_argument('from_page', type=int, nargs='?', help='The starting page number')
        parser.add_argument('to_page', type=int, nargs='?', help='The ending page number')

    def handle(self, *args, **kwargs) -> None:
        """ 
        Handles the command execution:
            if arguments from_page and to_page were given, crawls the given range;
            but if none were given, crawls all the news beginning from the first page until it see a duplicate news.
        """

        from_page = kwargs.get('from_page')
        to_page = kwargs.get('to_page')

        crawler = ZoomitCrawler()

        if from_page is None and to_page is None:
            # This means that we should crawl unseen news
            crawler.crawl_unseen_news(stop=5)
            self.stdout.write(self.style.SUCCESS(f'Successfully crawled all unseen news from Zoomit.'))        
        
        elif from_page is not None and to_page is not None:
            # This means that we should crawl in the given range
            crawler.crawl_over_a_range(from_page, to_page)
            self.stdout.write(self.style.SUCCESS(f'Successfully crawled Zoomit from page {from_page} to page {to_page}.'))
        
        crawler.quit()

