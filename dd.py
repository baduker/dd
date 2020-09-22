import datetime
import logging
import os

from typing import List

import requests
from lxml import html
from discord_webhook import DiscordWebhook, DiscordEmbed


def head_option(_iter: list) -> str:
    return next(iter(_iter), "")


def get_page():
    today = datetime.datetime.today().date()
    return requests.get(f"https://dilbert.com/strip/{today}").text


def get_dilbert() -> List[str]:
    _xpath_root = '//*[@class="img-responsive img-comic"]'
    tree = html.fromstring(get_page())
    src = head_option(tree.xpath(f"{_xpath_root}/@src"))
    title = head_option(tree.xpath(f"{_xpath_root}/@alt"))
    return [src, title]


def send_dilbert(event, context):
    img_src, title = get_dilbert()
    print(title, img_src)
    webhook = DiscordWebhook(url=os.getenv("WEBHOOK"))
    embed = DiscordEmbed(
        title=title,
        color=242424
    )
    embed.set_image(url=img_src)
    embed.set_footer(text='Proudly delivered by baduker!')
    webhook.add_embed(embed)
    webhook.execute()
    return {"StatusCode": 200, "Payload": [img_src, title]}
