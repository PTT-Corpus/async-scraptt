# Scrapy settings for scraptt project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy.utils.reactor import install_reactor

from .project import *  # noqa: F403

install_reactor(TWISTED_REACTOR)  # noqa: F405
