import discord
from discord.ext import commands
import random
import asyncio
import re
import requests
from bs4 import BeautifulSoup

site = "https://thispersondoesnotexist.com/"
response = requests.get(site)
soup = BeautifulSoup(response.text, 'html.parser')
img_tags = soup.find_all('img')

urls = [img['src'] for img in img_tags]
for url in urls:
    with open('image.jpg', 'wb') as f:
        if 'http' not in url:
            # sometimes an image source can be relative
            # if it is provide the base url which also happens
            # to be the site variable atm.
            url = '{}{}'.format(site, url)
        response = requests.get(url)
        f.write(response.content)