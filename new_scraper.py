"""A script for scraping news sites and writing latest articles to
json.
"""

import sys
import json
from time import mktime
from datetime import datetime
import time
import feedparser as fp
import newspaper
from newspaper import Article
from newspaper import Config
from modules import Translator
import os
from datetime import date
import translators as ts
import pymongo
import json

HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
           
config = Config()
config.headers = HEADERS
config.request_timeout = 10

data = {}
data["newspapers"] = {}

def check_output_folder():
    MYDIR = (".output")
    CHECK_FOLDER = os.path.isdir(MYDIR)

    # If folder doesn't exist, then create it.
    if not CHECK_FOLDER:
        os.makedirs(MYDIR)
        print("created output folder : ", MYDIR)

    else:
        print(MYDIR, "output folder already exists.")

def parse_config(fname):
    # Loads the JSON files with news sites
    with open(fname, "r") as data_file:
        cfg = json.load(data_file)

    for company, value in cfg.items():
        if "link" not in value:
            raise ValueError(f"Configuration item {company} missing obligatory 'link'.")
    #_ = ts.preaccelerate_and_speedtest()
    return cfg


def _handle_rss(company, value):
    """If a RSS link is provided in the JSON file, this will be the first
    choice.

    Reason for this is that, RSS feeds often give more consistent and
    correct data.

    If you do not want to scrape from the RSS-feed, just leave the RSS
    attr empty in the JSON file.
    """
    count = 0
    fpd = fp.parse(value["rss"])
    print(f"Downloading articles from {company}")
    news_paper = []
    for entry in fpd.entries:
        # Check if publish date is provided, if no the article is
        # skipped.  This is done to keep consistency in the data and to
        # keep the script from crashing.
        if not hasattr(entry, "published"):
            continue
        article = {}
        article["link"] = entry.link
        date = entry.published_parsed
        article["published"] = datetime.fromtimestamp(mktime(date)).isoformat()
        try:
            content = Article(entry.link)
            content.download()
            content.parse()
            content.nlp()
        except Exception as err:
            # If the download for some reason fails (ex. 404) the
            # script will continue downloading the next article.
            print(err)
            print("continuing...")
            continue
        article["title"] = content.title
        article["text"] = content.text
        article["keywords"] = content.keywords
        article["source"] = company
        news_paper.append(article)
        print(f"{count} articles downloaded from {company}, url: {entry.link}")
        count = count + 1
    return count, news_paper


def _handle_fallback(company, value):
    """This is the fallback method if a RSS-feed link is not provided.

    It uses the python newspaper library to extract articles.

    """
    myclient = pymongo.MongoClient("mongodb://54.255.236.171:27017/")
    db = myclient["redwatcher"]
    collection = db[company]
    count = 0
    total_count = 0
    print(f"Scraping articles from {company}")
    paper = newspaper.build(value["link"], language=value["language"],memoize_articles=value["memoize"],verbose=True, browser_user_agent="AppleWebKit/535.19 (KHTML, like Gecko)")
    print(paper.size())
    news_paper = []
    none_type_count = 0
    for content in paper.articles:
        try:
            content.download()
            content.parse()
            content.nlp()
        except Exception as err:
            print(str(err)+" will cooloff for 20 secs")
            time.sleep(20)
            print("continuing...")
            continue
        # Again, for consistency, if there is no found publish date the
        # article will be skipped.
        #
        # After 10 downloaded articles from the same newspaper without
        # publish date, the company will be skipped.
        if content.publish_date is None:
            print(f" Article has date of type None...")
            content.publish_date = datetime.now()
            none_type_count = none_type_count + 1
            if none_type_count > 10:
                print("Too many noneType dates, aborting...")
                none_type_count = 0
                #break
            count = count + 1
            #continue
        
        if value["translate"]  == 'True':
            if len(str(content.title)) != 0:
                trans_title = Translator.random_translator(str(content.title))
                #print(trans_title)
            else:
                trans_title = str(content.title)
            if len(str(content.text)) != 0:
                if len(str(content.text)) < 5000:
                    trans_text = Translator.random_translator(str(content.text))
                else:
                    big_str = str(content.text)
                    trans_text = Translator.random_translator(big_str[0:5000])
                #print(trans_text)
            else:
                trans_text = str(content.text)
            if len(str(content.keywords)) != 0:
                if len(str(content.keywords)) < 5000:
                    trans_keywords = Translator.random_translator(str(content.keywords))
                else:
                    big_str2 = str(content.keywords)
                    trans_keywords = Translator.random_translator(big_str2[0:5000])
                #print(trans_keywords)
            else:
                trans_keywords = str(content.keywords)
            article = {
                "title": trans_title,
                "text": trans_text,
                "keywords": trans_keywords,
                "link": content.url,
                "source": company,
                "published": content.publish_date.isoformat(),
            }
        else:
             article = {
                "title": content.title,
                "text": content.text,
                "keywords": content.keywords,
                "link": content.url,
                "source": company,
                "published": content.publish_date.isoformat(),
            }
        news_paper.append(article)
        ins = collection.insert_one(article)
        print(
            f" articles downloaded from {company} , url: {content.url}"
        )
        count = count + 1
        total_count = total_count + 1
        none_type_count = 0
        print("Total articles processed =",total_count)
        time.sleep(5)
        if count > 100:
            count = 0
            print("Scraped 100 articles. Sleeping for 20 secs")
            time.sleep(20)
    return news_paper


def run(config):
    """Take a config object of sites and urls.

    Iterate through each news company.

    Write result to scraped_articles.json.
    """
    check_output_folder()

    for company, value in config.items():
        if "rss" in value:
            count, news_paper = _handle_rss(company, value)
        else:
            news_paper = _handle_fallback(company, value)
        data = news_paper

    # Finally it saves the articles as a JSON-file.
    '''
    try:
        with open(".output/scraped_articles_"+str(company)+"_"+str(date.today())+"_.json", "w", encoding='utf8') as outfile:
            json.dump(data, outfile, indent=2, ensure_ascii=False)
    except Exception as err:
        print(err)
    '''

def main():
    """News site scraper.

    Takes a command line argument containing json.
    """

    args = list(sys.argv)

    if len(args) < 2:
        sys.exit("Usage: new_scraper.py NewsPapers.json")

    fname = args[1]
    try:
        config = parse_config(fname)
    except Exception as err:
        sys.exit(err)
    run(config)


if __name__ == "__main__":
    main()
