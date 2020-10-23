#!/usr/bin/env python3

import requests
import re
import bs4
import yaml

re.MULTILINE = True

# TODO: don't forget to add http://scp-int.wikidot.com/ later. script won't get to it since its hosted on another domain
#		OR CHANGE HOW SITES ARE PICKED TO ALLOW some external sites with a WHITELIST
initialSite = requests.get("http://www.scpwiki.com/")
siteBuffer = [initialSite]
addedSites = []

with open("lists.yaml") as f: listFile = yaml.load(f, Loader=yaml.FullLoader) # load blacklist file

def siteGet(targeted_websites):
	target = targeted_websites.pop() # remove site from buffer
	if type(target) == str:
		target = requests.get(target)
	curSoup = bs4.BeautifulSoup(target.content, "html.parser") # make soup object out of site
	addedSites.append(target.url) # add the url to list of already downloaded sites
	for newLink in getLinks(target, curSoup):
		if newLink not in addedSites and newLink not in siteBuffer:
			siteBuffer.append(newLink)
	open("downloaded/" + curSoup.title.string + ".html", "w+").write(curSoup.prettify())

def getLinks(parent_link, cleaned_soup):
	newLinks = []
	for link in cleaned_soup.find_all("a"): # all links
		if link.has_attr("href"): 
			if link.get("href")[0] == "/": # if a link does not direct to an external site (we want to stay inside the wiki)
				if not any(re.search(exp, link.get("href")) for exp in listFile["blacklists"]["links_re"]): # matches every link with multiple regex patterns
					absoluteLink = parent_link.url + str(link["href"])[1:] # relative to absolute url
					newLinks.append(absoluteLink)
	return newLinks

#TODO: after downloading all the links go back to them and remove sidebars, licenses, media links etc. keep regular css tho, to keep unique pages unique

siteGet(siteBuffer)
for i in siteBuffer:
	print(i)