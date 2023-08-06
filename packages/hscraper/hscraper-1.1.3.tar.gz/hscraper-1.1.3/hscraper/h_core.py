#Somehow, this is needed because when run from the .exe, it doesnt know where package is :P
#So to find all the subpackages, we must add them to sys path during run time
#This is achieved by appending the real path to this very script to the sys path
import os
import sys
import traceback
local = os.path.dirname(os.path.realpath(__file__))
sys.path.append(local)

from plugins.danbooru import danbooru_scraper
from plugins.r34 import r34_scraper
from plugins.ehen import ehen_scraper
from plugins.hitomi import hitomi_scraper

import click

class HCore():
    
    def __init__(self):
        self.dan = danbooru_scraper.Danbooru()
        self.hen = ehen_scraper.EhenScraper()
        self.r34 = r34_scraper.R34Scraper()
        self.hit = hitomi_scraper.HitomiScraper()
    
    def core_start(self, url, skip_from, pages, wait, retry, wait_retry, output, debug):
        """
        Starts the scraping and downloading process.
        """
        try:
            
            if self.dan.validate_url(self.dan.clean_url(url)):
                self.dan.start(url, pages, skip_from, wait, retry, wait_retry, output)
            elif self.hen.validate_url(url):
                self.hen.start(url, pages, skip_from, wait, retry, wait_retry, output)
            elif self.r34.validate_url(url):
                self.r34.start(url, pages, skip_from, wait, retry, wait_retry, output)
            elif self.hit.validate_url(url):
                self.hit.start(url=url, from_img=skip_from, to_img=pages, wait=wait, retry=retry, wait_retry=wait_retry, output=output)
            else:
                print("\nWhat the hell just happened? No valid url found :c")
                
        except Exception as w:
            if debug:
                traceback.print_exc(file=sys.stdout)
                print(w)
                
@click.command()
@click.option('-b',help="(Absolute) Path to a txt with multiple urls as: url,page[,skip_from]. One per line."+
              " This option overrides -u, -p and -f. Throw it (the path to txt) between quotes for safe measure.")
@click.option('-u',help="Gallery url, throw it between quotes for safe measure.")
@click.option('-f',help="Skip from page -f to page -p.",default=None)
@click.option('-p',help="Pages to scrap. Default is 1",default=1)
@click.option("-o",help="Output directory, throw it between quotes for safe measure.")
@click.option('-w',help="Wait time between http requests, defaut is 3.0 seconds.",default=3.0)
@click.option('-r',help="Set number of retries. Default is 3.",default=3)
@click.option('-x',help="Set wait time between retries. Default is 3.0 seconds.",default=3.0)
@click.option('-d/--no-d', help="Debug mode", default=False)
def clickerino(b, u, f, p, o, w, r, x, d):
    """Scraps images from the following sites: danbooru.donmai, r34.xxx, ehentai.org and hitomi.la"""
    if f:
        f = int(f)
    if u is None and b is None:
        click.echo("Hey, there is no url, nor text file with links here!")
        click.echo("type --help to know more")
        exit()

    if o is None:
        click.echo("No output path specified. Type --help for more.")
        exit()

    if b is not None:
        batch_start(batch=b, wait=w, retry=r, wait_retry=x, output=o, debug=d)
    else:
        core = HCore()
        core.core_start(url=u, pages=p, skip_from=f, wait=w, retry=r, wait_retry=x, output=o, debug=d)

def batch_start(batch, wait, retry, wait_retry, output, debug):
    """
    Calls core_start for each line in the text file.
    """
    with open(batch) as bat:
        lines = bat.readlines()
    core = HCore()
    for line in lines:
        tmp = line.strip().split(",")
        url = tmp[0]
        pages = int(tmp[1])
        try:
            if tmp[1]:
                skip_from = int(tmp[2])
        except:
            skip_from = None
        try:
            core.core_start(url=url, pages=pages, skip_from=skip_from, wait=wait, retry=retry, wait_retry=wait_retry, output=output, debug=debug)
        except:
            continue

if __name__ == '__main__':
    clickerino()