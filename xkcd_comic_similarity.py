"""
This program implements the retrieval of XKCD comics
Written by Tim Burke and Anuj Ramakrishnan
"""
import numpy as np
import pandas as pd
import xlwt
import xlrd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk import word_tokenize # Tokenization tool


########################################################################################################################
# Read in the data 
########################################################################################################################
# def read_file():



########################################################################################################################
# Get the similarity score matrix between a query and comic texts 
########################################################################################################################
def jaccard_similarity(str1,str2):
		"""Takes Jaccard similarity of two strings (tokenized using NLTK word_tokenize)"""
		str1 = set(word_tokenize(str1))
		str2 = set(word_tokenize(str2))
		return float(len(str1 & str2)) / float(len(str1 | str2)) 


def get_similar(input_query,vectorizer_1, df ,vecs , similarity_type = 1):
	"""
	input_query: Takes a free text query (e.g. 'drones')
	vectorizer_1: A scikit learn tf_idf vectorizer instance, fit over the XKCD text
	df: Pandas dataframe containing the text data (columns: title, title_text, all_categories, explanation, transcript)
	vecs: The tf-idf vectors representing the different text fields of each comic
	similarity_type: 1 for cosine, 2 for jaccard

	This function takes a free-text query and prints the most similar three comics' titles and index numbers
	"""
	
	results = ''	
	query = [input_query]
	query_vec = vectorizer_1.transform(query)

	if similarity_type == 1:
		# Take cosine similarity over each field of the comic text
		title_sim = cosine_similarity(query_vec,vecs[0]).transpose()
		rollover_sim = cosine_similarity(query_vec,vecs[1]).transpose()
		category_sim = cosine_similarity(query_vec,vecs[2]).transpose()
		explanation_sim = cosine_similarity(query_vec,vecs[3]).transpose()
		transcript_sim = cosine_similarity(query_vec,vecs[4]).transpose()
		
		# Stack them into a matrix
		score_matrix = np.column_stack((title_sim,rollover_sim,category_sim,explanation_sim,transcript_sim))

		# Result is the similarity scores, multiplied by the weights for each text field. 
		weights = np.array([5,3,6,1,3]) # Weights in order title, rollover, category, explanation, transcript
		results = np.matmul(score_matrix,weights)

	elif similarity_type == 2:
		
		# Take cosine similarity over each field of the comic text
		jaccard_title = np.array([jaccard_similarity(query[0],string) for string in df['title']]).reshape((len(df['title']),1))
		jaccard_rollover = np.array([jaccard_similarity(query[0],string) for string in df['title_text']]).reshape((len(df['title']),1))
		jaccard_category = np.array([jaccard_similarity(query[0],string) for string in df['all_categories']]).reshape((len(df['title']),1))
		jaccard_explanation = np.array([jaccard_similarity(query[0],string) for string in df['explanation']]).reshape((len(df['title']),1))
		jaccard_transcript = np.array([jaccard_similarity(query[0],string) for string in df['transcript']]).reshape((len(df['title']),1))

		# Stack them into a matrix
		jaccard_matrix = np.column_stack((jaccard_title,jaccard_rollover,jaccard_category,jaccard_explanation,jaccard_transcript))

		# Result is the similarity scores, multiplied by the weights for each text field. 
		j_weights = np.array([1,1,1,1,1])
		results = np.matmul(jaccard_matrix,j_weights)

	count = 1
	for idx in results.argsort()[:-4:-1]:
		print("RESULT #%i" % count,": ",df['title'].loc[idx],"\n",df.loc[idx],"\n")
		count += 1

	return 0

def main():
	"""Create tf-idf vectors over the data, and then make queries"""
	df = pd.read_csv('data/comic_final_data.csv',encoding='UTF-8')
	df = df.fillna(" ")
	df["all_text"] = df["title"] + " " + df["topic_category"] + " " + df["title_text"] + " " + df["explanation"] + " " + df["transcript"]

	# To remove duplicates of comics in multiple categories, first find all categories for all comics
	def get_all_categories(row):
		categories = df['topic_category'].loc[df['url'] == row['url']]
		cats = categories.str.cat(sep=' ')
		return cats
	df['all_categories'] = df.apply(get_all_categories,axis=1)

	# Now we remove duplicate comics, keeping only 1 of each
	df = df.drop_duplicates(subset='url',keep='first')
	df = df.drop('topic_category', axis = 1)

	# Create a tf-idf vectorizer to create representations of text
	vectorizer = TfidfVectorizer(norm='l2', min_df=0, use_idf=True, smooth_idf=False, sublinear_tf=True, tokenizer=word_tokenize, lowercase = True)
	vectorizer = vectorizer.fit(df['all_text']) # Fit the vectorizer on all the text in XKCD

	title_vectors = vectorizer.transform(df['title'])
	rollover_vectors = vectorizer.transform(df['title_text'])
	category_vectors = vectorizer.transform(df['all_categories'])
	explanation_vectors = vectorizer.transform(df['explanation'])
	transcript_vectors = vectorizer.transform(df['transcript'])
	
	tfidf_vectors = [title_vectors,rollover_vectors,category_vectors,explanation_vectors,transcript_vectors]


	loop = 'Y'
	while(loop == 'Y'):
		input_query = input("Enter your query:")
		similarity_type = int(input("Enter 1 for Cosine Similarity and 2 for Jaccard Similarity "))
		get_similar(input_query, vectorizer, df,tfidf_vectors, similarity_type)
		loop = input("Want to try again? (Y/N)").upper()


if __name__ == "__main__":
	main()
