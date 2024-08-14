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
        """
        Adds arguments to the command parser for specifying the page range.
        """
        parser.add_argument('from_page', type=int, help='The starting page number')
        parser.add_argument('to_page', type=int, help='The ending page number')

    def handle(self, *args, **kwargs) -> None:
        """
        Handles the command execution, triggering the crawling process in the given range of pages.
        """
        from_page = kwargs['from_page']
        to_page = kwargs['to_page']

        crawler = ZoomitCrawler()
        crawler.run_crawler(from_page, to_page)
        crawler.quit()

        self.stdout.write(self.style.SUCCESS(f'Successfully crawled Zoomit from page {from_page} to page {to_page}.'))
