import aiohttp
import asyncio
from lxml import etree
from collections import defaultdict
import tempfile
import os
import json

DB = os.path.join(tempfile.gettempdir(), "dummy_useragent.json")
from .dummy_useragent import DUMMY_AGENT
import random


class Agent(object):
    def __init__(self, pc=[], phone=[], hardware="compute"):
        """
        hardware: compute or phone
        """
        self.pc = pc
        self.phone = phone
        self.hardware = hardware

    def choice(self):
        if self.hardware == "computer":
            return random.choice(self.pc)
        else:
            return random.choice(self.phone)


class UserAgent(object):
    def __init__(self):
        self.params = {
            "Chrome": "https://developers.whatismybrowser.com/useragents/explore/software_name/chrome/",
            "Chromium": "https://developers.whatismybrowser.com/useragents/explore/software_name/chromium/",
            "Edge": "https://developers.whatismybrowser.com/useragents/explore/software_name/edge/",
            "Firefox": "https://developers.whatismybrowser.com/useragents/explore/software_name/firefox/",
            "Internet-Explorer": "https://developers.whatismybrowser.com/useragents/explore/software_name/internet-explorer/",
            "Opera": "https://developers.whatismybrowser.com/useragents/explore/software_name/opera/",
            "QQ": "https://developers.whatismybrowser.com/useragents/explore/software_name/qq-browser/",
            "Safari": "https://developers.whatismybrowser.com/useragents/explore/software_name/safari/",
            "Sougou": "https://developers.whatismybrowser.com/useragents/explore/software_name/sogou-search-dog/",
            "UC": "https://developers.whatismybrowser.com/useragents/explore/software_name/uc-browser/",
            "TheWorld": "https://developers.whatismybrowser.com/useragents/explore/software_name/theworld-browser/",
        }
        self.map = defaultdict(lambda: defaultdict(list))
        self.Chrome = Agent()
        self.Chromium = Agent()
        self.IE = Agent()
        self.Edge = Agent()
        self.Firefox = Agent()
        self.UC = Agent()
        self.QQ = Agent()
        self.Opera = Agent()
        self.TheWorld = Agent()
        self.Sougou = Agent()
        self.Safari = Agent()
        if not os.path.exists(DB):
            with open(DB, "w") as f:
                json.dump(DUMMY_AGENT, f)
            self.cache = DUMMY_AGENT
        else:
            with open(DB, "r") as f:
                self.cache = json.load(f)
        for browser in self.cache["PC"].keys():
            setattr(
                self,
                browser.title(),
                Agent(
                    self.cache["PC"].get(browser, []),
                    self.cache["Phone"].get(browser, []),
                ),
            )

    def random(self):
        key = random.choice(list(self.cache["PC"].keys()))
        rst = random.choice(self.cache["PC"][key])
        if not rst:
            return self.random()
        return rst

    async def get(self, url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, proxy="http://127.0.0.1:1080") as res:
                    content = await res.read()
                    return content
        except Exception as e:
            return ""

    async def run(self):
        for param in self.params.items():
            [browser, url] = param
            await asyncio.ensure_future(self.handle(browser, url))
        await self.save_cache()

    async def save_cache(self):
        with open(DB, "w") as f:
            json.dump(self.map, f)

    def refresh(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(self.run()))

    async def handle(self, browser, url):
        content = await self.get(url)
        if not content:
            return
        doc = etree.HTML(content)
        useragents = doc.xpath("//table//tr[position()>1]")
        if not useragents:
            return
        for useragent in useragents:
            try:
                ua = useragent.xpath(".//a/text()")[0]
                hy = useragent.xpath("./td[position()=4]/text()")[0]
            except Exception:
                continue
            if hy == "Computer":
                self.map["PC"][browser].append(ua)
            else:
                self.map["Phone"][browser].append(ua)

