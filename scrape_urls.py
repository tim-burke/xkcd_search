import xlwt
import xlrd
import csv
from comic_parser import * # Get the comic parsing function (written separately)

# Start by creating a list of the urls to iterate over.
urls = []
with open('input.csv', 'r+') as file: # Any input csv with a list of URLs
    comic_csv = csv.reader(file)
    for row in comic_csv:
    	urls.append(row[1])


# Now we try to parse the info out of each URL
comic_text = [] # Will be list of [title,title_text,explanation,transcript] lists for each comic
for url in urls:
	try:
		title, title_text, explanation, transcript = parse_comic(url)
		comic_text.append([title,title_text,explanation,transcript]) # Separate the text so excel functions can break it out
	except:
		print(url)
		comic_text.append(["NOTHING RECOVERED"])

# Finally, we write the info into a CSV in your working directory
writer = csv.writer(open('undo_mistakes.csv','w+'))
for c in comic_text:
	writer.writerow(c)

