import time

from lxml.html import etree

from config import sec
from tools import Aio, echo_log, process_video


class Openrec:
    def __init__(self):
        self.Aio = Aio()

    async def is_live(self, oprec_id):
        html = await self.Aio.main(f'https://www.openrec.tv/user/{oprec_id}', "get")
        dom = etree.HTML(html)
        is_live = dom.xpath('/html/body/div[1]/div[2]/div[18]/div[2]/div/div[3]/ul/li[1]/div/text()')[0]
        if 'Live' in is_live:
            info = dom.xpath('/html/body/div[1]/div[2]/div[18]/div[2]/div/div[3]/ul/li[1]/ul/li/a[2]')[0]
            ref = info.xpath('@href')[0]
            title = dom.xpath('/html/body/div[1]/div[2]/div[18]/div[2]/div/div[3]/ul/li[1]/ul/li/a[2]/text()')[0]
            return {'Title': title, 'Ref': ref}

    async def check(self, oprec_id):
        is_live = await self.is_live(oprec_id)
        if is_live:
            await process_video(is_live, 'Openrec')
        else:
            echo_log('Openrec' + time.strftime('|%m-%d %H:%M:%S|', time.localtime(time.time())) +
                     f'Not found Live, after {sec}s checking')
