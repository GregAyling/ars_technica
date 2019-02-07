import os
import requests

_ARS_FILENAME = 'arsfile.html'

# General tag adder...
def _tagged(tag,textin):
	return("<" + tag + ">" + textin + "</" + tag + ">")

# Page linker...
def _linked(linktext,linkto):
	return('<a href="' + linkto + '">' + linktext + "</a>")

# Remove anything which isn't part of the title.
def _important_bit(title_string: str) -> str:

    if "ArsAB" not in title_string:
        return title_string
    
    impression_loc = title_string.find('ars_ab.impression')
    string1 = title_string[impression_loc:]

    semicolon_loc = string1.find(';')
    string2 = string1[semicolon_loc+1:]

    arsab_loc = string2.find('ars_ab')
    string3 = string2[:arsab_loc]

    return string3

if __name__ == "__main__":

	# Get web page...
	page = requests.get("https://www.arstechnica.com")

	# Parse web page...
	from bs4 import BeautifulSoup
	soup = BeautifulSoup(page.content, 'html.parser')

	# Find article components...
	articles = soup.find_all('h2')
	excerpts = soup.find_all(class_='excerpt')

	# Open HTML file...
	htmlfile = open(_ARS_FILENAME,'w')
	htmlfile.write("<head>")
	htmlfile.write('<link rel="stylesheet" type="text/css" href="default.css">')
	htmlfile.write("</head>")
	htmlfile.write("<body>")

	# Write all articles to file...
	duplicate_excerpts = 0
	for article_no in range(len(articles)):
		article = articles[article_no]
		linkpage = article.find('a')['href']
		raw_title = article.get_text()
		htmlfile.write(_tagged("p",_tagged("h1",_important_bit(raw_title))))
		# If excerpt is repeated, it is a duplicate and needs to be ignored...
		if article_no > 0 and excerpts[article_no + duplicate_excerpts].get_text() == excerpts[article_no + duplicate_excerpts - 1].get_text():
			duplicate_excerpts = duplicate_excerpts + 1
		excerpt = excerpts[article_no + duplicate_excerpts].get_text()
		htmlfile.write(_tagged("p",_tagged("h2","- " + excerpt)))
		htmlfile.write(_tagged("p",_tagged("h3",_linked('LINK',linkpage))))
		
	# Close HTML file...
	htmlfile.write("</body>")
	htmlfile.close()

	# Display file.
	os.startfile(_ARS_FILENAME)