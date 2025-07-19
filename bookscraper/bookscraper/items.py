# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def price_serializer(value):
    if "£" in value:
        return value.replace("£", "Birr ")
    return f"Birr {value}"


class BookItem(scrapy.Item):
    title = scrapy.Field()
    category = scrapy.Field()
    price = scrapy.Field()
    # price = scrapy.Field(
    #     serializer=price_serializer
    # )
    rating = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()

    # Additional fields from table rows
    upc = scrapy.Field()
    product_type = scrapy.Field()
    price_excl_tax = scrapy.Field()
    price_incl_tax = scrapy.Field()
    tax = scrapy.Field()
    availability = scrapy.Field()
    num_reviews = scrapy.Field()
