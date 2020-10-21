#!/usr/bin/env python3

import requests
import re
import bs4
import yaml

re.MULTILINE = True

initialSite = requests.get("http://www.scpwiki.com/")
siteBuffer = [initialSite]
addedSites = []

with open("blacklist.yaml") as f: blacklisted = yaml.load(f, Loader=yaml.FullLoader) # load blacklist file

def siteGet(targeted_websites):
	target = targeted_websites.pop() # remove site from buffer
	curSoup = bs4.BeautifulSoup(target.content, "html.parser")
	addedSites.append(target.url) # add the url to list of already downloaded sites
	for newLink in getLinks(target, curSoup):
		if newLink not in addedSites:
			siteBuffer.append(newLink)
	open(curSoup.title.string + ".html", "w+").write(curSoup.prettify())

def getLinks(parent_link, cleaned_soup):
	newLinks = []
	for link in cleaned_soup.find_all("a"): # all links
		if link.has_attr("href"): 
			if link.get("href")[0] == "/": # if a link does not direct to an external site (we want to stay inside the wiki)
				if not any(re.search(exp, link.get("href")) for exp in blacklisted["links_re"]): # matches every link with multiple regex patterns
					absoluteLink = parent_link.url + str(link["href"])[1:] # relative link to absolute url
					newLinks.append(absoluteLink)
	return newLinks

#TODO: after downloading all the links go back to them and remove sidebars, licenses, media links etc

siteGet(siteBuffer)