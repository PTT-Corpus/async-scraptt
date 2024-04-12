from html.parser import HTMLParser


class HTMLParserService(HTMLParser):
    def __init__(self, *, convert_charrefs: bool = True) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed: list[str] = []

    def handle_data(self, data: str):
        return self.fed.append(data)

    def get_data(self):
        return "".join(self.fed)

    @classmethod
    def strip_tags(cls, html: str):
        html_stripper = cls()
        html_stripper.feed(html)
        return html_stripper.get_data()
