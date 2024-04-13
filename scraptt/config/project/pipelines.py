# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "scraptt.pipelines.CkipPipeline": 301,
    "scraptt.pipelines.JsonPipeline": 300,
}
