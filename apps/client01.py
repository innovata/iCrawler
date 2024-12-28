


import pprint 
pp = pprint.PrettyPrinter(indent=2)
import os 
from importlib import reload


from pytubefix import YouTube 
from pytubefix.cli import on_progress


import sys 
sys.path.append("D:\pypjts\iCrawler\src")

from ipycrawl.crawlers.youtube import _pytubefix 
# reload(pytubefix)

# url = input("https://youtu.be/Jrmb07ku6ZY?feature=shared")

# print('URL: %s' % url)

# yt = YouTube(
#     url, 
#     use_oauth=True, 
#     allow_oauth_cache=True, 
#     on_progress_callback=on_progress
# )
# print(yt)
# print(yt.title)
# ys = yt.streams.get_highest_resolution()
# print(ys)
# ys.download()

# for st in yt.streams:
#     print(st)
# print(yt.fmt_streams)



_pytubefix.download_video("https://youtu.be/-ZwuJgl5YFQ?feature=shared")



