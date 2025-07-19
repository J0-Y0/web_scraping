import scrapy
from bookscraper.items import BookItem


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):

        books = response.css("article.product_pod")
        for book in books:
            book_page = book.css("article.product_pod h3 a::attr(href)").get()
            if "catalogue" in book_page:
                book_page_url = f"https://books.toscrape.com/{book_page}"
            else:
                book_page_url = f"https://books.toscrape.com/catalogue/{book_page}"

            yield response.follow(book_page_url, callback=self.parse_books)
        next_page = response.css("li.next a").attrib["href"]
        if next_page:
            if "catalogue" in next_page:
                next_page_url = f"https://books.toscrape.com/{next_page}"
            else:
                next_page_url = f"https://books.toscrape.com/catalogue/{next_page}"

            yield response.follow(next_page_url, callback=self.parse)

    def parse_books(self, response):
        rows = response.css("table.table  tr")

        book_item = BookItem()

        book_item["title"] = response.css("div.product_main h1::text").get()
        book_item["category"] = response.xpath(
            "//ul[@class = 'breadcrumb']/li[@class = 'active']/preceding-sibling::li[1]/a/text()"
        ).get()
        book_item["price"] = response.css("div.product_main p.price_color::text").get()
        book_item["rating"] = (
            response.css("p.star-rating::attr(class)").get().split()[1]
        )

        # table data

        book_item["upc"] = rows[0].css("td::text").get()
        book_item["product_type"] = rows[1].css("td::text").get()
        book_item["price_excl_tax"] = rows[2].css("td::text").get()
        book_item["price_incl_tax"] = rows[3].css("td::text").get()
        book_item["tax"] = rows[4].css("td::text").get()
        book_item["availability"] = rows[5].css("td::text").get()
        book_item["num_reviews"] = rows[6].css("td::text").get()

        book_item["description"] = response.xpath(
            "//div[@id ='product_description']/following-sibling::p/text()"
        ).get()
        book_item["url"] = response.url
        yield book_item
