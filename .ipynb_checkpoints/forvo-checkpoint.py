from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait

from bs4 import BeautifulSoup, element
import argparse
from functools import total_ordering
import requests

if __name__ == "__main__":
    prog_desc = "Download pronunciation file from Forvo"
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(prog=prog_desc)
    parser.add_argument('--dest',
                        help="download directory",
                        type=str)
    parser.add_argument('--word',
                        help="Word to research",
                        type=str)

    args = parser.parse_args()
    word = args.word
    dest = args.dest
    
def get_forvo_page(url: str) -> BeautifulSoup:
    """Get the bs4 object from Forvo page

    url: str - the Forvo pronunciation page

    Returns
    -------
    BeautifulSoup 4 object for the page
    """
    driver = webdriver.Safari()
    driver.get(url)
    driver.implicitly_wait(1)
    # agree_button = driver.execute_script("""return document.querySelector("button[mode='primary']");""")
    # try:
    #     agree_button.click()
    # except AttributeError:
    #     pass
    # try:
    #     close_button = driver.execute_script("""return document.querySelector("button.mfp-close");""")
    #     close_button.click()
    # except AttributeError:
    #     pass
    # time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    ru_pronunciation_list = soup.find("ul", {"id": "pronunciations-list-ru"})
    if ru_pronunciation_list is None:
        print('ERROR - this word may not exist on Forvo!')
    return ru_pronunciation_list

@property
class Pronunciation(object):
    def __init__(self, uname:str, positive: int, path: str):
        self.user_name = uname
        self.positive: int = positive
        self.path: str = path
        
from typing import Optional
def pronunciation_for_li(element: element.Tag):
    # -> Optional[Pronunciation]:
    """Pronunciation object from its <li> element

    Returns an optional Pronunciation object from a
    <li> element that contains the required info.

    Returns
    -------
    Pronunciation object, or None
    """
    info_span = element.find("span", {"class": "info"})
    if info_span is not None:
        user = user_from_info_span(info_span)
    votes = num_votes_from_li(element)
    url = audio_link_for_li(element)
    if url is not None:
        pronunciation = Pronunciation(user, votes, url)
        return pronunciation
    return None

@property
def score(self) -> int:
    subscore = 0
    if self.user_name in FAVS:
        subscore = 2
    return self.positive + subscore
   
def __eq__(self, other):
    if not isinstance(other, type(self)): return NotImplemented
    return self.score == other.score

def __lt__(self, other):
    if not isinstance(other, type(self)): return NotImplemented
    return self.score < other.score

