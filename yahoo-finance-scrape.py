#!/usr/bin/env python
# -*- coding: utf-8 -*

from lxml import html
import requests, csv

csvFile = "results.csv" #where to store results

## Ticker symbols to pull data for ##
tickers = [
	"CSCO",
	"INTC",
	"MAT",
	"T",
	"AAPL",
	"TGT",
	"STX",
	"SO",
	"WMT"
]

## Statistics to pull from Yahoo Finance "Key Statistcs" Page i.e. http://finance.yahoo.com/q/ks?s=YHOO+Key+Statistics
keyStatistics = [
	"Trailing P/E",
	"Forward P/E",
	"Revenue (ttm)",
	"EBITDA (ttm)",
	"Total Cash (mrq)",
	"Total Debt (mrq)",
	"Forward Annual Dividend Yield",
	"Payout Ratio",
	"52-Week Change",
	"Short % of Float ",
]

## Search tree to find value based upon sibling text ##
def findTDValue(searchTree,tdRelatedText):
	tdValue = searchTree.xpath('//td[contains(text(), "'+tdRelatedText+'")]/following-sibling::td[1]/text()')
	if tdValue:
		return [tdValue[0]] #return first result as list item
	else:
		return ["N/A"]

resultTable = [["Ticker"] + keyStatistics] #append ticker as first column of results

for ticker in tickers: #iterate through tickers
	page = requests.get('http://finance.yahoo.com/q/ks?s='+ticker+'+Key+Statistics') #pull page data
	tree = html.fromstring(page.text) #parse
	resultRow = [ticker] #start new result row with first item as the ticker symbol
	for keyStatistic in keyStatistics: #iterate through remaining statistic items, and append to row
		resultRow += findTDValue(tree, keyStatistic)
	resultTable += [resultRow] #write entire row as new record in table
	
print(resultTable) #print result

## write result to csv file specified above ##
with open(csvFile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(resultTable)
