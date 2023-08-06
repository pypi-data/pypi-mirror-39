import asyncio
import time
from pyppeteer.launcher import launch
from pyppeteer import errors
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8'
class browser():
    def __init__(self,headless=True,ignoreHTTPSErrors=True):
        self.headless=headless
        self.ignoreHTTPSErrors=ignoreHTTPSErrors
        self.loop=asyncio.get_event_loop()
    def goto(self,url,timeout=20,wait=False):
        if not hasattr(self, "browser") or not hasattr(self, "page"):
            self.browser,self.page=self.loop.run_until_complete(self.__create_browser(headless=self.headless,ignoreHTTPSErrors=self.ignoreHTTPSErrors))
        self.loop.run_until_complete(self.__goto(url,timeout=timeout,wait=wait))
    async def __content(self):
        return await self.page.content()
    def send(self,selector,text):
        self.loop.run_until_complete(self.__send(selector,text))
    async def __send(self,selector,text):
        await self.page.type(selector,text)
    def onclick(self,selector,wait=False):
        self.loop.run_until_complete(self.__onclick(selector,wait=wait))
    async def __onclick(self,selector,wait=False):
        if wait:
            waitUntil=["networkidle0"]
        else:
            waitUntil=["networkidle2"]
        await asyncio.wait([
            self.page.click(selector),
            self.page.waitForNavigation(waitUntil=waitUntil)
            ])
    @property
    def content(self):
        return self.loop.run_until_complete(self.__content())
    @property
    def cookies(self):
        return self.loop.run_until_complete(self.__cookies())

    async def __cookies(self):
        cookies={}
        cks=await self.page.cookies()
        for ck in cks:
            cookies[ck["name"]]=ck["value"]
        return cookies
    async def __goto(self,url,timeout=20,wait=False):
        if wait:
            waitUntil=["networkidle0"]
        else:
            waitUntil=["networkidle2"]
        await self.page.goto(url,options={'timeout': int(timeout * 1000),"waitUntil":waitUntil})
    async def __create_browser(self,headless=True,ignoreHTTPSErrors=True):
        browser= await launch(headless=headless,ignoreHTTPSErrors=ignoreHTTPSErrors)
        pages = await browser.pages()
        page=pages[0]
        await page.setUserAgent(DEFAULT_USER_AGENT)
        return browser,page
    async def __close_browser(self):
        await self.browser.close()
    def __del__(self):
        if hasattr(self, "browser") and hasattr(self, "page"):
            self.loop.run_until_complete(self.__close_browser())
    def exit(self):
        if hasattr(self, "browser") and hasattr(self, "page"):
            self.loop.run_until_complete(self.__close_browser())