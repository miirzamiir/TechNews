from news.models import News, Tag
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


class ZoomitCrawler:

    def __init__(self) -> None:
        self.service = webdriver.ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service)

    def run_crawler(self, from_page, to_page, archive="https://www.zoomit.ir/archive/") -> list:
        # This method iterates over a given range of pages and collects all news links in a list.
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
        # This method gets a link to a news and saves that news and its tags in the database.
        self.driver.get(news_url)

        title = self._get_news_title()
        text = self._get_news_text()

        if (not title) or (not text):
            return None

        tags = self._get_news_tags()
        self._save_news(title, text, news_url, tags)
        
    def _get_news_title(self) -> str:
        try:
            title_xpath = '//h1[@class="typography__StyledDynamicTypographyComponent-t787b7-0 jQMKGt" or @class="typography__StyledDynamicTypographyComponent-t787b7-0 fzMmhL"]'
            title_element = self.driver.find_element(By.XPATH, title_xpath)
            return title_element.text.strip()
        except NoSuchElementException:
            return None

    def _get_news_text(self) -> str:
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

    def _get_news_tags(self) -> list:
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

    def _save_news(self, title, text, resource, tags) -> None:
        if not News.objects.filter(title=title).exists():
            news_item = News(title=title, text=text, resource=resource)
            news_item.save()
            news_item.tags.set(tags)

    def quit(self) -> None:
        self.driver.quit()