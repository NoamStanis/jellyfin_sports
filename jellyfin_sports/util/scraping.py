import time
import requests as reqs
import regex as re
import datetime
import json
import sys
from . import game_info
from .pretty_print import otype, colours, p, pind, pind2
#import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup

load_dotenv()


NBA = "nba"
NHL = "nhl"
NFL = "nfl"

# NHL Teams
nhl_teams = [
    "anaheim-ducks", "arizona-coyotes", "boston-bruins", "buffalo-sabres", "calgary-flames", 
    "carolina-hurricanes", "chicago-blackhawks", "colorado-avalanche", "columbus-blue-jackets", 
    "dallas-stars", "detroit-red-wings", "edmonton-oilers", "florida-panthers", "los-angeles-kings", 
    "minnesota-wild", "montreal-canadiens", "nashville-predators", "new-jersey-devils", 
    "new-york-islanders", "new-york-rangers", "ottawa-senators", "philadelphia-flyers", 
    "pittsburgh-penguins", "san-jose-sharks", "seattle-kraken", "st-louis-blues", "tampa-bay-lightning", 
    "toronto-maple-leafs", "vancouver-canucks", "vegas-golden-knights", "washington-capitals", 
    "winnipeg-jets"
]

# NFL Teams
nfl_teams = [
    "arizona-cardinals", "atlanta-falcons", "baltimore-ravens", "buffalo-bills", "carolina-panthers", 
    "chicago-bears", "cincinnati-bengals", "cleveland-browns", "dallas-cowboys", "denver-broncos", 
    "detroit-lions", "green-bay-packers", "houston-texans", "indianapolis-colts", "jacksonville-jaguars", 
    "kansas-city-chiefs", "las-vegas-raiders", "los-angeles-chargers", "los-angeles-rams", 
    "miami-dolphins", "minnesota-vikings", "new-england-patriots", "new-orleans-saints", 
    "new-york-giants", "new-york-jets", "philadelphia-eagles", "pittsburgh-steelers", 
    "san-francisco-49ers", "seattle-seahawks", "tampa-bay-buccaneers", "tennessee-titans", 
    "washington-commanders"
]

# NBA Teams
nba_teams = [
    "atlanta-hawks", "boston-celtics", "brooklyn-nets", "charlotte-hornets", "chicago-bulls", 
    "cleveland-cavaliers", "dallas-mavericks", "denver-nuggets", "detroit-pistons", 
    "golden-state-warriors", "houston-rockets", "indiana-pacers", "los-angeles-clippers", 
    "los-angeles-lakers", "memphis-grizzlies", "miami-heat", "milwaukee-bucks", "minnesota-timberwolves", 
    "new-orleans-pelicans", "new-york-knicks", "oklahoma-city-thunder", "orlando-magic", 
    "philadelphia-76ers", "phoenix-suns", "portland-trail-blazers", "sacramento-kings", 
    "san-antonio-spurs", "toronto-raptors", "utah-jazz", "washington-wizards"
]



def flatten_json(y: dict) -> dict:
    """
    Function capable of flattening an object.
    """
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            ix = 0
            for a in x:
                flatten(a, name + str(ix) + '_')
                ix += 1
        else:
            out[name[:-1]] = x
    flatten(y)
    return out


# Helper Functions
def selenium_find(link: str) -> list:
    """
    Looks for possible m3u8 links in network traffic from a streaming site.
    """
    pind(f"Trying to find m3u8 in network traffic - {link}", colours.OKCYAN, otype.DEBUG)
    res = []
    try:
        try:

            caps = DesiredCapabilities.CHROME
            caps['goog:loggingPrefs'] = {'performance': 'ALL'}
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome(desired_capabilities=caps, options=chrome_options)
        except Exception as e:
            print(e.with_traceback())
        driver.get(link)
        time.sleep(1)  # wait for all the data to arrive.
        perf = driver.get_log('performance')
        for j in perf:
            try:
                if "m3u8" in json.dumps(j):
                    obj = flatten_json(json.loads(j["message"]))
                    list_of_dict_values = list(obj.values())
                    for value in list_of_dict_values:
                        if str(value).find("m3u8") > -1 and str(value) not in res:
                            if int(reqs.get(value, allow_redirects=True).status_code) == 200:
                                pind2(f"Found a stream - {str(value)}", colours.OKGREEN, otype.REGULAR)
                            res.append(value)
            except KeyboardInterrupt:
                sys.exit()
                pass
            except Exception as e:
                p("Something went wrong pulling a m3u8 link", colours.FAIL, otype.ERROR, e)
                continue
    except KeyboardInterrupt:
        sys.exit()
        pass
    except Exception as e:
        print(e.with_traceback())
        p("Something went wrong with Selenium", colours.FAIL, otype.ERROR, e)
    return list(dict.fromkeys(res))


def html_find(link: str) -> list:
    """
    Looks for possible m3u8 links in html traffic from a streaming site.
    """
    pind(f"Trying to find m3u8 in page content - {link}", colours.OKCYAN, otype.DEBUG)
    res = []
    try:
        content = reqs.get(link).text
        for match in re.findall(r"([\'][^\'\"]+(\.m3u8)[^\'\"]*[\'])|([\"][^\'\"]+(\.m3u8)[^\'\"]*[\"])", content):
            for i in match:
                if (i.count("\'") == 2 and i.count("\"") == 0) or (i.count("\"") == 2 and i.count("\'") == 0) and ".m3u8" in i and i[1:-1] not in res:
                    if int(reqs.get(i[1:-1], allow_redirects=True).status_code) == 200:
                        res.append(i[1:-1])
                        pind2(f"Found a stream - {str(i[1:-1])}", colours.OKGREEN, otype.REGULAR)
    except Exception as e:
        pass
    return res


def find_urls(ll: list) -> list:
    """
    Helper function used to scrape html and network traffic from a provided link.
    """
    res = []
    if len(ll) == 0:
        return res
    try:
        for link in ll:
            if os.environ.get('selenium') == "0":
                res.extend(x for x in selenium_find(link) if x not in res)
            res.extend(x for x in html_find(link) if x not in res)
    except KeyboardInterrupt:
        sys.exit()
        pass
    except Exception as e:
        return list(dict.fromkeys(res))
    if len(res) == 0:
        p("Did not find streams", colours.FAIL, otype.DEBUG)
    return list(dict.fromkeys(res))


def bypass_bitly(ll: list) -> list:
    """
    Ability to bypass bitly pages to get streaming site url.
    """
    res = []
    for link in ll:
        parsed_html = BeautifulSoup(reqs.request("GET", link).text, features="lxml")
        try:
            url = parsed_html.body.find('a', attrs={'id': 'skip-btn'}).get('href')
            if url:
                res.append(url)
        except KeyboardInterrupt:
            sys.exit()
            pass
        except Exception as e:
            p(f"Error occurred bypassing bitly - {link}", colours.FAIL, otype.ERROR)
            pass
    return list(dict.fromkeys(res))


def pull_bitly_link(link) -> list:
    """
    Pull bitly link from main streaming site.
    """
    parsed_html_next = BeautifulSoup(reqs.request("GET", link).text, features="lxml")
    res = []
    try:
        for tag in parsed_html_next.body.find_all('tr'):
            if tag.get('data-stream-link'):
                res.append(tag.get('data-stream-link'))
    except KeyboardInterrupt:
        sys.exit()
        pass
    except Exception as e:
        p(f"Error getting stream link from {link}", colours.FAIL, otype.DEBUG)
        return res
    return res

def make_match(game_links, lg) -> list:
    games = {}
    for i, url in enumerate(game_links):
        response = reqs.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract team names from the URL
        match = re.search(r'live-([\w-]+)-vs-([\w-]+)-stream', url)
        if match:
            home_team = match.group(1).replace("-", " ").title()
            away_team = match.group(2).replace("-", " ").title()
        else:
            away_team, home_team = "Unknown", "Unknown"
        
        games["game_" + str(i+1)] = {
        "url" : url,
        "Home Team": home_team,
        "Away Team": away_team,
        "Name": home_team + " vs. " + away_team
        }

    return games

def find_streams(lg: str) -> list:
    """
    Finds current games that are active for a given league.
    """
    STREAM_LINK = os.environ.get('stream_link')
    scraping_url = STREAM_LINK
    p(f"COLLECTING {lg.upper()} STREAMING LINKS", colours.HEADER, otype.REGULAR)
    res = []
    games = []
    hosts = [f"{STREAM_LINK}"]
    path = None
    if lg == NHL:
         scraping_url += "/live/basketball-stream"
    elif lg == NFL:
         scraping_url += "/live/football-stream"
    elif lg == NBA:
        scraping_url += "/live/basketball-stream"
    
    # Fetch page content
    response = reqs.get(scraping_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract all links
    extracted_links = [a['href'] for a in soup.find_all('a', href=True)]

    # Filter links containing any NBA team name
    if lg == NHL:
        sports_links = [link for link in extracted_links if any(team in link for team in nhl_teams)]
    elif lg == NFL:
        sports_links = [link for link in extracted_links if any(team in link for team in nfl_teams)]
    elif lg == NBA:
        sports_links = [link for link in extracted_links if any(team in link for team in nba_teams)]

    # Print the filtered links
    for i, link in enumerate(sports_links):
        sports_links[i] = STREAM_LINK + link
    
    
    return make_match(sports_links, lg)

def get_streams(s: list) -> list:
    return find_urls(bypass_bitly(s))
