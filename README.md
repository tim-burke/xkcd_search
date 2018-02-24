# xkcd_search
Project that scrapes info about xkcd webcomics and implements free text search with cosine and Jacccard similarity

## Comic_parser.py 
* Takes a URL from Explain XKCD and outputs the title, title text, main text and explanation of a comic from Explain XKCD 

## organizer.py
* Runs the comic parser over a list of urls and writes them into CSV

## xkcd_comic_similarity.py
* Takes user queries and finds the most relevant comics based on the similarity score between tf-idf vectors of the comic text fields and the user query. 




