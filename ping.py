import pandas as pd
import logging
import time
from datetime import datetime
from typing import Union
import httpx
import asyncio

logger = logging.getLogger(__name__)
logger.setLevel("INFO")


class Ping:
    def __init__(self, filename: str, loop):
        self.sites = pd.read_csv(filename, delimiter=';')
        self.sites.dropna(subset=['Host'], inplace=True)
        self.loop = loop
        self.task = self.loop.create_task(self.start())
        self.urls: set = self._create_urls()

    @staticmethod
    async def _log_response(url: Union[str, None] = None,
                            status: str = "???", error=False, res_time: float = 0):

        now = datetime.now()
        if not error:
            logger.warning(f"{now} | GET | http://{url} | {res_time} sec | Opened")
        else:
            logger.warning(f"{now} | GET | http://{url} | {res_time} | {status}")

    async def _send_request(self, url: str) -> None:
        async with httpx.AsyncClient(verify=False, timeout=1.5) as client:
            start_time = time.time()
            try:
                r = await client.get(f"http://{url}")
                await self._log_response(url=url, res_time=time.time() - start_time)
            except httpx.ConnectError:
                await self._log_response(url=url, error=True, res_time=time.time() - start_time)
            except httpx.ConnectTimeout:
                await self._log_response(url=url, status="Not opened", error=True, res_time=time.time() - start_time)
            except httpx.UnsupportedProtocol:
                await self._log_response(url=url, status="Not opened", error=True, res_time=time.time() - start_time)
            except httpx.RemoteProtocolError:
                await self._log_response(url=url, status="Not opened", error=True, res_time=time.time() - start_time)

    def sigint_handler(self, signal, frame):
        self.loop.stop()

    def _create_urls(self) -> set:
        hosts = self.sites["Host"].to_list()
        ports = self.sites["Ports"].to_list()
        urls = set()
        for i in range(len(ports)):
            urls.add(hosts[i])
            if pd.isna(ports[i]):
                continue
            ports[i] = ports[i].split(',')
            for j in range(len(ports[i])):
                urls.add(f"{hosts[i]}:{ports[i][j]}")
        return urls

    async def ping(self):
        tasks = []
        for url in self.urls:
            tasks.append(self._send_request(url))
        await asyncio.gather(*tasks)

    async def start(self):
        while True:
            await self.ping()
            await asyncio.sleep(2)
