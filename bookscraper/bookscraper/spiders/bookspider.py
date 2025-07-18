import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        
        books = response.css("article.product_pod")
        for book in books:
            book_page = book.css("article.product_pod h3 a::attr(href)").get()
            if "catalogue" in  book_page:
                book_page_url = f"https://books.toscrape.com/{book_page}"
            else :
                book_page_url = f"https://books.toscrape.com/catalogue/{book_page}"

            
            yield response.follow(book_page_url,callback = self.parse_books)
        next_page = response.css("li.next a").attrib["href"]
        if next_page:
            if "catalogue" in  next_page:
                next_page_url = f"https://books.toscrape.com/{next_page}"
            else :
                next_page_url = f"https://books.toscrape.com/catalogue/{next_page}"

            yield response.follow(next_page_url,callback = self.parse)

    def parse_books(self,response):
            rows =response.css("table.table  tr")
            table_data = {
                row.css("th::text").get(): row.css("td::text").get()
                for row in rows
            }
            yield{                
                'title' :response.css("div.product_main h1::text").get(),
                "category":response.xpath("//ul[@class = 'breadcrumb']/li[@class = 'active']/preceding-sibling::li[1]/a/text()").get(),
                'price' :response.css("div.product_main p.price_color::text").get() ,
                "rating":response.css("p.star-rating::attr(class)").get().split()[1],
                **table_data,
                "description":response.xpath("//div[@id ='product_description']/following-sibling::p/text()").get(),
                "url":response,
               
            }