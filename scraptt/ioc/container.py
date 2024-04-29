from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from scraptt.services import (
    HTMLParserService,
    LatestIndexFetchService,
    PostCommentReactionService,
    PostCommentService,
    PostContentService,
    PostLinkService,
    PostMetadataService,
)


class Container(DeclarativeContainer):
    PostLinkService = Singleton(PostLinkService)
    LatestIndexFetchService = Singleton(LatestIndexFetchService)
    HTMLParserService = Singleton(HTMLParserService)
    PostContentService = Singleton(
        PostContentService, html_parser_service=HTMLParserService
    )
    PostMetadataService = Singleton(PostMetadataService)
    PostCommentService = Singleton(PostCommentService)
    PostCommentReactionService = Singleton(PostCommentReactionService)
