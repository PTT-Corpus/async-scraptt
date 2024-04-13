from __future__ import annotations

from typing import TYPE_CHECKING

from dependency_injector.wiring import inject
from scrapy import Spider
from scrapy.http import Request
from scrapy.signalmanager import dispatcher
from scrapy.utils.defer import maybe_deferred_to_future
from scrapy.utils.reactor import is_asyncio_reactor_installed

from scraptt.config import (
    COOKIES,
    PTT_BASE_URL,
    PTT_DOMAINS,
)
from scraptt.interfaces import (
    Post,
    SpiderArguments,
)
from scraptt.ioc import (
    Container,
    Provide,
)
from scraptt.services import (
    LatestIndexFetchService,
    PostCommentReactionService,
    PostCommentService,
    PostContentService,
    PostLinkService,
    PostMetadataService,
)
from scraptt.singals import error_post_signal

if TYPE_CHECKING:
    from scrapy.http.response.html import HtmlResponse
    from twisted.internet.defer import DeferredList


class PttSpider(Spider):
    name = "ptt"
    allowed_domains = PTT_DOMAINS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._arguments = SpiderArguments(**kwargs)
        self._container = Container()
        self._container.wire(modules=[__name__])
        if not is_asyncio_reactor_installed():
            raise ValueError(
                "PttSpider requires the asyncio Twisted "
                "reactor. Make sure you have it configured in the "
                "TWISTED_REACTOR setting. See the asyncio documentation "
                "of Scrapy for more information."
            )

    @inject
    def start_requests(
        self,
        latest_index_fetch_service: LatestIndexFetchService = Provide[
            LatestIndexFetchService
        ],
    ):
        with_range = all([self._arguments.index_from, self._arguments.index_to])
        for board in self._arguments.boards:
            if not with_range:
                url = f"{PTT_BASE_URL}/{board}/index.html"
                yield Request(
                    url,
                    cookies=COOKIES,
                    callback=latest_index_fetch_service.fetch(self.parse),
                    meta={"board": board},
                )
            else:
                for index in range(
                    self._arguments.index_from, self._arguments.index_to + 1
                ):
                    url = f"{PTT_BASE_URL}/{board}/index{index}.html"
                    yield Request(
                        url, cookies=COOKIES, callback=self.parse, meta={"board": board}
                    )

    @inject
    async def parse(
        self,
        response: HtmlResponse,
        post_link_service: PostLinkService = Provide[PostLinkService],
        post_content_service: PostContentService = Provide[PostContentService],
        post_metadata_service: PostMetadataService = Provide[PostMetadataService],
        post_comment_service: PostCommentService = Provide[PostCommentService],
        post_comment_reaction_service: PostCommentReactionService = Provide[
            PostCommentReactionService
        ],
        **kwargs,
    ):
        post_links = post_link_service.get(
            response, self.crawler.engine, self._arguments.scrape_from
        )
        if not post_links:
            return

        responses, errors = await self.fetch_posts(post_links)
        if errors:
            dispatcher.send(
                signal=error_post_signal, errors=errors, board=response.meta["board"]
            )

        for resp in responses:
            post_content = post_content_service.get(resp)
            if not post_content:
                return

            metadata = post_metadata_service.get(resp)
            comments = post_comment_service.get(resp)
            comment_reaction = post_comment_reaction_service.count(resp)
            yield Post(
                **metadata,
                content=post_content,
                comment_reaction=comment_reaction,
                comments=comments,
            ).model_dump()

    async def fetch_posts(self, post_links: DeferredList):
        result = await maybe_deferred_to_future(post_links)
        responses, error = [], []
        for success, response in result:
            if not success or response.status != 200:
                error.append(response)
            else:
                responses.append(response)
        return responses, error
