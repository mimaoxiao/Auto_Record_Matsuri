import asyncio
from urllib import error
from config import (
    sec, enable_mirrativ, enable_youtube, enable_openrec, enable_proxy, oprec_id,
    userid, ddir, proxy, channel_id, api_key, quality, download_in_live)
from mirrativ import Mirrativ
from youtube import Youtube
from tools import m_error
from openrec import Openrec


# 定时器，以后考虑用scheduler代替？
class Localtimer:

    def __init__(self):
        if enable_youtube:
            self.y = Youtube(channel_id, enable_proxy, proxy, ddir, api_key, quality, download_in_live)
        if enable_mirrativ:
            self.m = Mirrativ(userid, enable_proxy, proxy, ddir)
        if enable_openrec:
            self.o = Openrec(oprec_id, enable_proxy, proxy, ddir)

    async def youtube_timer(self):
        self.y.check()
        await asyncio.sleep(sec)

    async def mirrativ_timer(self):
        self.m.check()
        await asyncio.sleep(sec)

    async def openrec_timer(self):
        self.o.check()
        await asyncio.sleep(sec)


# 这个异步功能有限，考虑在每个模块请求IO时也加入异步处理
async def main():
    t = Localtimer()
    if enable_youtube:
        task_y = asyncio.create_task(t.youtube_timer())
    if enable_mirrativ:
        task_m = asyncio.create_task(t.mirrativ_timer())
    if enable_openrec:
        task_o = asyncio.create_task(t.openrec_timer())
    if enable_youtube:
        await task_y
    if enable_mirrativ:
        await task_m
    if enable_openrec:
        await task_o
    del t


if __name__ == '__main__':
    while True:
        try:
            asyncio.run(main())
        except error.URLError:
            m_error('URL error!')
