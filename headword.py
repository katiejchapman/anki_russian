from urllib.request import urlopen, Request
import urllib.parse
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem, HardwareType
import copy
import re
import sys
from bs4 import BeautifulSoup
__version__ = 0.9

# accept word as either argument or on stdin
try:
    raw_word = sys.argv[1]
except IndexError:
    raw_word = sys.stdin.read()

raw_word = raw_word.replace(" ", "_").strip()
word = urllib.parse.quote(raw_word)
url =  f'https://en.wiktionary.org/wiki/{word}#Russian'
#url =  f'https://ru.wiktionary.org/wiki/{word}'

hn = [HardwareType.COMPUTER.value]
user_agent_rotator = UserAgent(hardware_types=hn,limit=20)
user_agent = user_agent_rotator.get_random_user_agent()
headers = {'user-agent': user_agent}
try:
    response = urlopen(Request(url, headers = headers))
except urllib.error.HTTPError as e:
    if e.code == 404:
        print("Error - no such word")
    else:
        print(f"Error: status {e.code}")
    sys.exit(1)

# first extract the Russian content because
# we may have other languages. This just
# simplifies the parsing for the headword
new_soup = BeautifulSoup('', 'html.parser')
soup = BeautifulSoup(response.read(), 'html.parser')
for h2 in soup.find_all('h2'):
    for span in h2.children:
        try:
            if 'Russian' in span['id']:
                new_soup.append(copy.copy(h2))
                # capture everything in the Russian section
                for curr_sibling in h2.next_siblings:
                    if curr_sibling.name == "h2":
                        break
                    else:
                        new_soup.append(copy.copy(curr_sibling))
                break
        except:
            pass

# use the derived soup to pick out the headword from
# the Russian-specific content
headwords = []
for strong in new_soup.find_all('strong'):
    node_lang = strong.get('lang')
    node_class = strong.get('class')
    if node_lang == "ru":
        if "Cyrl" in node_class:
            if "headword" in node_class:
                raw_headword = strong.text
                headwords.append(raw_headword)

try:
    print(headwords[0])
    sys.exit(0)
except SystemExit:
   # this just avoids triggering an exception due
   # to a normal exit
    pass
except IndexError:
   # we didn't find any words
    print("Error")
    sys.exit(1)