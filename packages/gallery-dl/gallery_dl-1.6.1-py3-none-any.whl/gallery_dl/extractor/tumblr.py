# -*- coding: utf-8 -*-

# Copyright 2016-2018 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extract images from https://www.tumblr.com/"""

from .common import Extractor, Message
from .. import text, oauth, exception
from datetime import datetime, timedelta
import re
import time


def _original_inline_image(url):
    return re.sub(
        (r"https?://(\d+\.media\.tumblr\.com(?:/[0-9a-f]+)?"
         r"/tumblr(?:_inline)?_[^_]+)_\d+\.([0-9a-z]+)"),
        r"https://\1_1280.\2", url
    )


def _original_video(url):
    return re.sub(
        (r"https?://(vt+(?:\.media)?\.tumblr\.com"
         r"/tumblr_[^_]+)_\d+\.([0-9a-z]+)"),
        r"https://\1.\2", url
    )


POST_TYPES = frozenset((
    "text", "quote", "link", "answer", "video", "audio", "photo", "chat"))

BASE_PATTERN = (
    r"(?:tumblr:(?:https?://)?([^/]+)|"
    r"(?:https?://)?([^.]+\.tumblr\.com))")


class TumblrExtractor(Extractor):
    """Base class for tumblr extractors"""
    category = "tumblr"
    directory_fmt = ["{category}", "{name}"]
    filename_fmt = "{category}_{blog_name}_{id}_{num:>02}.{extension}"
    archive_fmt = "{id}_{num}"

    def __init__(self, match):
        Extractor.__init__(self)
        self.blog = match.group(1) or match.group(2)
        self.api = TumblrAPI(self)

        self.types = self._setup_posttypes()
        self.inline = self.config("inline", False)
        self.reblogs = self.config("reblogs", True)
        self.external = self.config("external", False)

        if len(self.types) == 1:
            self.api.posts_type = next(iter(self.types))
        elif not self.types:
            self.log.warning("no valid post types selected")

        if self.reblogs == "same-blog":
            self._skip_reblog = self._skip_reblog_same_blog

    def items(self):
        blog = None
        yield Message.Version, 1

        for post in self.posts():
            if post["type"] not in self.types:
                continue
            if not blog:
                blog = self.api.info(self.blog)
                blog["uuid"] = self.blog
                yield Message.Directory, blog.copy()

            reblog = "reblogged_from_id" in post
            if reblog and self._skip_reblog(post):
                continue
            post["reblogged"] = reblog

            post["blog"] = blog
            post["num"] = 0

            if "trail" in post:
                del post["trail"]

            if "photos" in post:  # type "photo" or "link"
                photos = post["photos"]
                del post["photos"]

                for photo in photos:
                    post["photo"] = photo
                    photo.update(photo["original_size"])
                    del photo["original_size"]
                    del photo["alt_sizes"]
                    yield self._prepare_image(photo["url"], post)

            if "audio_url" in post:  # type: "audio"
                yield self._prepare(post["audio_url"], post)

            if "video_url" in post:  # type: "video"
                yield self._prepare(_original_video(post["video_url"]), post)

            if self.inline:  # inline media
                for key in ("body", "description", "source"):
                    if key not in post:
                        continue
                    for url in re.findall('<img src="([^"]+)"', post[key]):
                        url = _original_inline_image(url)
                        yield self._prepare_image(url, post)
                    for url in re.findall('<source src="([^"]+)"', post[key]):
                        url = _original_video(url)
                        yield self._prepare(url, post)

            if self.external:  # external links
                post["extension"] = None
                for key in ("permalink_url", "url"):
                    if key in post:
                        yield Message.Queue, post[key], post

    def posts(self):
        """Return an iterable containing all relevant posts"""

    def _setup_posttypes(self):
        types = self.config("posts", ("photo",))

        if types == "all":
            return POST_TYPES

        elif not types:
            return frozenset()

        else:
            if isinstance(types, str):
                types = types.split(",")
            types = frozenset(types)

            invalid = types - POST_TYPES
            if invalid:
                types = types & POST_TYPES
                self.log.warning('invalid post types: "%s"',
                                 '", "'.join(sorted(invalid)))
            return types

    @staticmethod
    def _prepare(url, post):
        text.nameext_from_url(url, post)
        post["num"] += 1
        post["hash"] = post["name"].partition("_")[2]
        return Message.Url, url, post

    @staticmethod
    def _prepare_image(url, post):
        text.nameext_from_url(url, post)
        post["num"] += 1

        parts = post["name"].split("_")
        post["hash"] = parts[1] if parts[1] != "inline" else parts[2]

        return Message.Url, url, post

    def _skip_reblog(self, _):
        return not self.reblogs

    def _skip_reblog_same_blog(self, post):
        return self.blog != post["reblogged_root_uuid"]


class TumblrUserExtractor(TumblrExtractor):
    """Extractor for all images from a tumblr-user"""
    subcategory = "user"
    pattern = [BASE_PATTERN + r"(?:/page/\d+|/archive)?/?$"]
    test = [
        ("http://demo.tumblr.com/", {
            "pattern": (r"https://\d+\.media\.tumblr\.com"
                        r"/tumblr_[^/_]+_\d+\.jpg"),
            "count": 1,
        }),
        ("http://demo.tumblr.com/", {
            "pattern": (r"https?://(?:$|"
                        r"\d+\.media\.tumblr\.com/.+_1280\.jpg|"
                        r"w+\.tumblr\.com/audio_file/demo/\d+/tumblr_\w+)"),
            "count": 3,
            "options": (("posts", "all"), ("external", True),
                        ("inline", True), ("reblogs", True))
        }),
        ("https://demo.tumblr.com/page/2", None),
        ("https://demo.tumblr.com/archive", None),
        ("tumblr:http://www.b-authentique.com/", None),
        ("tumblr:www.b-authentique.com", None),
    ]

    def posts(self):
        return self.api.posts(self.blog, {})


class TumblrPostExtractor(TumblrExtractor):
    """Extractor for images from a single post on tumblr"""
    subcategory = "post"
    pattern = [BASE_PATTERN + r"/(?:post|image)/(\d+)"]
    test = [
        ("http://demo.tumblr.com/post/459265350", {
            "pattern": (r"https://\d+\.media\.tumblr\.com"
                        r"/tumblr_[^/_]+_1280.jpg"),
            "count": 1,
        }),
        ("http://demo.tumblr.com/image/459265350", None),
    ]

    def __init__(self, match):
        TumblrExtractor.__init__(self, match)
        self.post_id = match.group(3)
        self.reblogs = True

    def posts(self):
        return self.api.posts(self.blog, {"id": self.post_id})

    @staticmethod
    def _setup_posttypes():
        return POST_TYPES


class TumblrTagExtractor(TumblrExtractor):
    """Extractor for images from a tumblr-user by tag"""
    subcategory = "tag"
    pattern = [BASE_PATTERN + r"/tagged/([^/?&#]+)"]
    test = [("http://demo.tumblr.com/tagged/Times%20Square", {
        "pattern": (r"https://\d+\.media\.tumblr\.com/tumblr_[^/_]+_1280.jpg"),
        "count": 1,
    })]

    def __init__(self, match):
        TumblrExtractor.__init__(self, match)
        self.tag = text.unquote(match.group(3))

    def posts(self):
        return self.api.posts(self.blog, {"tag": self.tag})


class TumblrLikesExtractor(TumblrExtractor):
    """Extractor for images from a tumblr-user's liked posts"""
    subcategory = "likes"
    directory_fmt = ["{category}", "{name}", "likes"]
    archive_fmt = "f_{blog[name]}_{id}_{num}"
    pattern = [BASE_PATTERN + r"/likes"]
    test = [("http://mikf123.tumblr.com/likes", {
        "count": 1,
    })]

    def posts(self):
        return self.api.likes(self.blog)


class TumblrAPI(oauth.OAuth1API):
    """Minimal interface for the Tumblr API v2"""
    API_KEY = "O3hU2tMi5e4Qs5t3vezEi6L0qRORJ5y9oUpSGsrWu8iA3UCc3B"
    API_SECRET = "sFdsK3PDdP2QpYMRAoq0oDnw0sFS24XigXmdfnaeNZpJpqAn03"
    BLOG_CACHE = {}

    def __init__(self, extractor):
        oauth.OAuth1API.__init__(self, extractor)
        self.posts_type = None

    def info(self, blog):
        """Return general information about a blog"""
        if blog not in self.BLOG_CACHE:
            self.BLOG_CACHE[blog] = self._call(blog, "info", {})["blog"]
        return self.BLOG_CACHE[blog]

    def posts(self, blog, params):
        """Retrieve published posts"""
        params.update({"offset": 0, "limit": 50, "reblog_info": "true"})
        if self.posts_type:
            params["type"] = self.posts_type
        while True:
            data = self._call(blog, "posts", params)
            self.BLOG_CACHE[blog] = data["blog"]
            yield from data["posts"]
            params["offset"] += params["limit"]
            if params["offset"] >= data["total_posts"]:
                return

    def likes(self, blog):
        """Retrieve liked posts"""
        params = {"limit": 50}
        while True:
            posts = self._call(blog, "likes", params)["liked_posts"]
            if not posts:
                return
            yield from posts
            params["before"] = posts[-1]["liked_timestamp"]

    def _call(self, blog, endpoint, params):
        if self.api_key:
            params["api_key"] = self.api_key
        url = "https://api.tumblr.com/v2/blog/{}/{}".format(
            blog, endpoint)

        response = self.session.get(url, params=params)
        data = response.json()
        status = data["meta"]["status"]

        if 200 <= status < 400:
            return data["response"]
        elif status == 403:
            raise exception.AuthorizationError()
        elif status == 404:
            raise exception.NotFoundError("user or post")
        elif status == 429:

            # daily rate limit
            if response.headers.get("x-ratelimit-perday-remaining") == "0":
                reset = response.headers.get("x-ratelimit-perday-reset")
                self.log.error(
                    "Daily API rate limit exceeded: aborting; "
                    "rate limit will reset at %s",
                    self._to_time(reset),
                )
                raise exception.StopExtraction()

            # hourly rate limit
            reset = response.headers.get("x-ratelimit-perhour-reset")
            if reset:
                self.log.info(
                    "Hourly API rate limit exceeded; "
                    "waiting until %s for rate limit reset",
                    self._to_time(reset),
                )
                time.sleep(int(reset) + 1)
                return self._call(blog, endpoint, params)

        self.log.error(data)
        raise exception.StopExtraction()

    @staticmethod
    def _to_time(reset):
        try:
            reset_time = datetime.now() + timedelta(seconds=int(reset))
        except (ValueError, TypeError):
            return "?"
        return reset_time.strftime("%H:%M:%S")
