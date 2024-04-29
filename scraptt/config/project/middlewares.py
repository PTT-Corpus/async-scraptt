# Spider middlewares (See https://docs.scrapy.org/en/latest/topics/spider-middleware.html)
SPIDER_MIDDLEWARES = {
    #    'scraptt.middlewares.ScrapttSpiderMiddleware': 543,
}

# Downloader middlewares (See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html)
DOWNLOADER_MIDDLEWARES = {
    "scraptt.middlewares.PyQueryMiddleware": 543,
    # "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
    # "scrapy_user_agents.middlewares.RandomUserAgentMiddleware": 400,
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": 550,
}
