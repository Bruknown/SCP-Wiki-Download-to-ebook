#!/usr/bin/env python3

import requests
import bs4
import yaml

initialSite = requests.get("http://www.scpwiki.com/")
siteBuffer = [initialSite]
addedSites = []

with open("blacklist.yaml") as f: blacklisted = yaml.load(f, Loader=yaml.FullLoader) # load blacklist file

def siteGet(targeted_websites):
	target = targeted_websites.pop() # remove site from buffer
	soup = bs4.BeautifulSoup(target.content, "html.parser")
	cleanSoup(soup)
	addedSites.append(target.url) # add the url to list of already downloaded sites
	for newLink in getLinks(target, soup):
		if newLink not in addedSites:
			siteBuffer.append(newLink)
	open(soup.title.string + ".html", "w+").write(soup.prettify())

def cleanSoup(dirty_soup): # removes the bulk of unwanted links
	dirtyTags = []
	for script in dirty_soup.find_all("script"): dirtyTags.append(script) # add it for cleaning
	for div in dirty_soup.find_all("div"): # for all divs in webpage
		if div.has_attr("class"): # handle div's classes
			for foo in div["class"]:
				if foo in blacklisted["classes"]:
					if div not in dirtyTags: dirtyTags.append(div)
		if div.has_attr("id"):
			if div["id"] in blacklisted["ids"]:
				if div not in dirtyTags: dirtyTags.append(div)
	for tag in dirtyTags:
		tag.decompose()

def getLinks(parent_link, cleaned_soup): # get all non-blacklisted links from a webpage
	newLinks = []
	for link in cleaned_soup.find_all("a"):
		if link.has_attr("href"):
			if link["href"] not in blacklisted["links"]:
				if str(link["href"])[0] == "/":
					newLinks.append(parent_link.url + str(link["href"])[1:]) # relative link to absolute url
				else:
					newLinks.append(link["href"])
	return newLinks

siteGet(siteBuffer)