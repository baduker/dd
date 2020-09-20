import datetime
import os

import requests
from lxml import html
from discord_webhook import DiscordWebhook, DiscordEmbed


today = datetime.datetime.today().date()
comic_src = '//*[@class="img-responsive img-comic"]/@src'
comic_title = '//*[@class="img-responsive img-comic"]/@alt'


def head_option(_iter: list) -> str:
    return next(iter(_iter), None)


def get_dilbert() -> list:
    response = requests.get(f"https://dilbert.com/strip/{today}").text
    tree = html.fromstring(response)
    src = head_option(tree.xpath(comic_src))
    title = head_option(tree.xpath(comic_title))
    return [src, title]


def send_dilbert(event, context):
    img_src, title = get_dilbert()
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
