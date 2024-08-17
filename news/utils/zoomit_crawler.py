from news.models import News, Tag
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import pytz
from datetime import datetime
from typing import List, Optional


class ZoomitCrawler:
    """
    Crawler class for retrieving news articles from the Zoomit website. Handles the process
    of navigating through pages, collecting news links, and extracting and saving news content.
    Save news data and tags into database if not existed.

    Attributes:
        service: Selenium service object to manage the ChromeDriver instance.
        driver: Selenium WebDriver instance to automate chrome browser interaction.
    """

    def __init__(self) -> None:
        """Class constructor. Sets initial value for class attributes."""
        self.service = webdriver.ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service)

    def crawl_unseen_news(self, stop=10, archive="https://www.zoomit.ir/archive/") -> None:
        """
        Iterates over zoomit archive pages and collects every news link which is not stored in database
        and passes them to crawl_news method in order to crawl them.
        stop: max page number that this method is allowed to crawl.
        """

        collected_links = []
        existing_links = list(resource[0] for resource in News.objects.values_list('resource'))
        
        for page_number in range(1, stop+1):
            url = archive + '?pageNumber=' + str(page_number)
            self.driver.get(url=url)
            self.driver.implicitly_wait(0.5) # waits for page to load
            links_x_path = '//a[@class="link__CustomNextLink-sc-1r7l32j-0 eoKbWT BrowseArticleListItemDesktop__WrapperLink-zb6c6m-6 bzMtyO"]'
            news_links = self.driver.find_elements(By.XPATH, links_x_path)
            
            for news_link in news_links:
                href = news_link.get_attribute('href')
                if href in existing_links:
                    break  # Stops crawling if an existing link was found
                
                collected_links.append(href)

            else:
                continue  # Only continue to the next page if we did not break the loop

            break  # Break the outer loop if we found an existing link

        print(f'Crawling {len(collected_links)} news from https://zoomit.ir')
        for news_link in collected_links:
            self.crawl_news(news_link)

    def crawl_over_a_range(self, from_page, to_page, archive="https://www.zoomit.ir/archive/") -> None:
        """Iterates over a range of pages to collect news links and passes each news link to crawl_news method in order to crawl them."""
        collected_links = []
        for page_number in range(from_page, to_page + 1):
            url = archive + '?pageNumber=' + str(page_number)
            self.driver.get(url=url)
            self.driver.implicitly_wait(0.5) # waits for page to load
            links_x_path = '//a[@class="link__CustomNextLink-sc-1r7l32j-0 eoKbWT BrowseArticleListItemDesktop__WrapperLink-zb6c6m-6 bzMtyO"]'
            news_links = self.driver.find_elements(By.XPATH, links_x_path)
            collected_links.extend([news_link.get_attribute('href') for news_link in news_links])        

        print(f'Crawling {len(collected_links)} news from https://zoomit.ir')
        for news_link in collected_links:
            self.crawl_news(news_link)

    def crawl_news(self, news_url) -> None:
        """
        Crawls a single news article, finds html elements related to News attributes(title, text, and tags),
        and extracts information from them by passing them to the related methods.
        At the end, saves news if not existed.
        """
        self.driver.get(news_url)

        title = self._get_news_title()
        text = self._get_news_text()
        date_time = self._get_news_datetime()

        if (not title) or (not text):
            return None

        tags = self._get_news_tags()
        self._save_news(title, text, news_url, date_time, tags)
        
    def _get_news_title(self) -> Optional[str]:
        """Extracts the title of a news article from the page and returns it. If no title was found, simply returns None."""
        try:
            title_xpath = '//h1[@class="typography__StyledDynamicTypographyComponent-t787b7-0 jQMKGt" or @class="typography__StyledDynamicTypographyComponent-t787b7-0 fzMmhL"]'
            title_element = self.driver.find_element(By.XPATH, title_xpath)
            return title_element.text.strip()
        except NoSuchElementException:
            return None

    def _get_news_text(self) -> Optional[str]:
        """Extracts the text of a news article from the page and returns it. If no text was found, simply returns None."""
        try:
            text_xpath = (
                '//p[@class="typography__StyledDynamicTypographyComponent-t787b7-0 fZZfUi ParagraphElement__ParagraphBase-sc-1soo3i3-0 gOVZGU"] | '
                '//h2[@class="typography__StyledDynamicTypographyComponent-t787b7-0 cAPRcR HeadingTwo__HeadingTwoBase-sc-3nstjw-1 aMVhn"] | '
                '//span[@font-size="1.6" and @class="typography__StyledDynamicTypographyComponent-t787b7-0 fNeDiY"]'
            )
            text_elements = self.driver.find_elements(By.XPATH, text_xpath)
            return '\n'.join([element.text for element in text_elements])
        except NoSuchElementException:
            return None

    def _get_news_tags(self) -> List[Tag]:
        """
        Extracts tags associated with a news article, saves new tags to the database and returns the list of 
        associated tags. If no tag was found returns an empty list.
        """
        try:
            tag_xpath = '//span[@class="typography__StyledDynamicTypographyComponent-t787b7-0 cHbulB" or @class="typography__StyledDynamicTypographyComponent-t787b7-0 bLZGOP"]'
            tag_elements = self.driver.find_elements(By.XPATH, tag_xpath)
            tag_labels = [element.text.strip() for element in tag_elements]
            existing_tags = Tag.objects.filter(tag_label__in=tag_labels)
            existing_tags_lables = set([tag.tag_label for tag in existing_tags])
            new_tags = [Tag(tag_label=label) for label in tag_labels if label not in existing_tags_lables]
            Tag.objects.bulk_create(new_tags)
            
            tags = list(existing_tags) + new_tags
        except NoSuchElementException:
            tags = []

        return tags

    def _get_news_datetime(self) -> Optional[datetime]:
        PERSIAN_MONTHS = {
            "فروردین": 1,
            "اردیبهشت": 2,
            "خرداد": 3,
            "تیر": 4,
            "مرداد": 5,
            "شهریور": 6,
            "مهر": 7,
            "آبان": 8,
            "آذر": 9,
            "دی": 10,
            "بهمن": 11,
            "اسفند": 12
        }

        try:
            datetime_xpath = '//span[@class="typography__StyledDynamicTypographyComponent-t787b7-0 fTxyQo fa" or @class="typography__StyledDynamicTypographyComponent-t787b7-0 cHbulB fa"]'
            datetime_element = self.driver.find_element(By.XPATH, datetime_xpath)
            dt = datetime_element.text.split()
            date_time = datetime(int(dt[3]), PERSIAN_MONTHS.get(dt[2]), int(dt[1]), int(dt[-1].split(':')[0]),
                                          int(dt[-1].split(':')[1]),
                                          tzinfo=pytz.timezone('Asia/Tehran'))

            return date_time

        except NoSuchElementException:
            return None

    def _save_news(self, title, text, resource, date, tags) -> None:
        """Saves a news item and its associated tags to the database."""
        if not News.objects.filter(title=title).exists():
            news_item = News(title=title, text=text, resource=resource, date=date)
            news_item.save()
            news_item.tags.set(tags)

    def quit(self) -> None:
        """Shuts down the WebDriver instance."""
        self.driver.quit()