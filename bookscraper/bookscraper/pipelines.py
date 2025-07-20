# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # --- Clean price fields ---
        price_fields = ["price", "price_excl_tax", "price_incl_tax",'tax']
        for field in price_fields:
            if field in adapter and adapter[field]:
                adapter[field] = float(adapter[field].replace("£", "").strip())

        # --- change rating fields to number ---
        rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
        if "rating" in adapter and adapter["rating"]:
            adapter["rating"] = rating_map.get(adapter["rating"], 0)

        # --- extract number from stock availability ---
        if "availability" in adapter and adapter["availability"]:
            adapter["availability"] = int(
                adapter["availability"].split(" (")[1].split(" ")[0]
            )


        # In stock (11 available)
        return item

