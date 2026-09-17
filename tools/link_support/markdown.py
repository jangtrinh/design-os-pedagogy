"""Parse CommonMark links, references, HTML and Obsidian wikilinks."""
from __future__ import annotations

from dataclasses import dataclass, field
from html.parser import HTMLParser
import re

from markdown_it import MarkdownIt


@dataclass(frozen=True)
class Link:
    target: str
    line: int
    kind: str = "link"


@dataclass
class ParsedMarkdown:
    links: list[Link] = field(default_factory=list)
    anchors: set[str] = field(default_factory=set)
    headings: list[tuple[int, str, int]] = field(default_factory=list)


def _wiki(state, silent):
    pos = state.pos
    if state.src[pos:pos + 2] != "[[":
        return False
    end = state.src.find("]]", pos + 2)
    if end < 0 or "\n" in state.src[pos:end]:
        return False
    if not silent:
        token = state.push("wikilink", "", 0)
        token.content = state.src[pos + 2:end]
        token.meta = {"embedded": pos > 0 and state.src[pos - 1] == "!"}
    state.pos = end + 2
    return True


def plain_text(tokens):
    return "".join(
        plain_text(token.children) if token.children else token.content
        for token in tokens or []
        if token.type not in {"html_inline", "link_open", "link_close"}
    )


def heading_slug(text):
    return re.sub(r"[^\w\- ]", "", text.lower()).replace(" ", "-")


class _HTMLLinks(HTMLParser):
    def __init__(self, parsed, line):
        super().__init__(convert_charrefs=True)
        self.parsed, self.line = parsed, line

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for name in ("id", "name" if tag == "a" else "id"):
            if attrs.get(name):
                self.parsed.anchors.add(attrs[name])
        key = "href" if tag == "a" else "src" if tag in {"img", "source"} else None
        if key and attrs.get(key):
            kind = "image" if key == "src" else "link"
            self.parsed.links.append(Link(attrs[key], self.line + self.getpos()[0] - 1, kind))

    handle_startendtag = handle_starttag


def parse_markdown(body: str, offset: int = 0) -> ParsedMarkdown:
    parser = MarkdownIt("commonmark", {"html": True})
    # This parser only extracts metadata. Let the auditor reject URL schemes
    # instead of silently losing links that a renderer would suppress.
    parser.validateLink = lambda url: True
    parser.inline.ruler.before("link", "wikilink", _wiki)
    tokens = parser.parse(body)
    parsed, used = ParsedMarkdown(), set()
    for index, token in enumerate(tokens):
        line = (token.map[0] if token.map else 0) + offset + 1
        if token.type == "heading_open" and index + 1 < len(tokens):
            title = plain_text(tokens[index + 1].children)
            base, suffix = heading_slug(title), 0
            slug = base
            while slug in used:
                suffix += 1
                slug = f"{base}-{suffix}"
            used.add(slug)
            parsed.anchors.add(slug)
            parsed.headings.append((int(token.tag[1:]), title, line))
        if token.type == "html_block":
            _HTMLLinks(parsed, line).feed(token.content)
        stack = list(token.children or [])
        while stack:
            child = stack.pop(0)
            if child.type == "link_open":
                parsed.links.append(Link(child.attrGet("href") or "", line))
            elif child.type == "image":
                parsed.links.append(Link(child.attrGet("src") or "", line, "image"))
            elif child.type == "wikilink":
                kind = "wiki-image" if child.meta.get("embedded") else "wiki"
                parsed.links.append(Link(child.content.split("|", 1)[0], line, kind))
            elif child.type == "html_inline":
                _HTMLLinks(parsed, line).feed(child.content)
            if child.children:
                stack.extend(child.children)
    return parsed
