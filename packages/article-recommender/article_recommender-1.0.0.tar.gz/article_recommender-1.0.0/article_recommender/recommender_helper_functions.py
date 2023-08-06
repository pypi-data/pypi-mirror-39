import numpy as np
import pandas as pd
import nltk
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
nltk.download(['punkt', 'wordnet', 'stopwords'])
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re


def get_top_article_ids(n, df):
    '''
    INPUT:
    n - (int) the number of top articles to return
    df - (pandas dataframe) dataframe containing user-article interactions, containing article_id,
    title and user_id

    OUTPUT:
    top_articles - (list) A list of the top 'n' article titles

    '''
    top_articles = df.groupby('article_id')['article_id'].count().sort_values(ascending=False).iloc[:n].index.tolist()

    return top_articles  # Return the top article ids

def rank_articles(df):
    '''

    :param df: (pandas dataframe) dataframe containing user-article interactions, containing article_id,
    title and user_id
    :return: ranked_articles: pandas dataframe with articles ranked by number of interactions
    '''

    grouped = df.groupby(['article_id', 'title'], as_index=False)['user_id'].count()
    grouped.rename(columns={'user_id': 'num_interactions'}, inplace=True)

    ranked_articles = grouped.sort_values(by='num_interactions', axis=0, ascending=False)

    return ranked_articles

def get_top_articles(n, ranked_df):
    '''
    INPUT:
    n - (int) the number of top articles to return
    ranked_df - (pandas dataframe) dataframe containing articles ranked based on their popularity

    OUTPUT:
    top_articles - (list) A list of the top 'n' article titles
    '''

    top_articles = ranked_df.iloc[:n]['title'].values.tolist()

    return top_articles  # Return the top article titles from df (not df_content)

def create_user_item_matrix(df):
    '''
    INPUT:
    df - pandas dataframe with article_id, title, user_id columns

    OUTPUT:
    user_item - user item matrix

    Description:
    Return a matrix with user ids as rows and article ids on the columns with the values
    the number of interactions between a given user and an article where one existed,
    missing value otherwise. This is a sparse matrix
    '''

    user_item = df.groupby(['user_id', 'article_id'])['user_id'].count().unstack()

    return user_item  # return the user_item matrix


def get_article_names(article_ids, df):
    '''
    INPUT:
    article_ids - (list) a list of article ids
    df - pandas dataframe with article_id, title, user_id columns

    OUTPUT:
    article_names - (list) a list of article names associated with the list of article ids
                    (this is identified by the title column)
    '''
    # we have to proceed through a for loop to keep the same order
    article_rep_names = []
    article_names = []

    # We first get a list of lists containing repetitions of the article name
    for id in article_ids:
        article_rep_names.append(df.loc[df.article_id == float(id), 'title'].values.tolist())

    # then we make a new list with the unique values
    for names in article_rep_names:
        try:
            article_names.append(names[0])
        except:
            article_names.append('No title available')

    return article_names  # Return the article names associated with list of article ids

def tokenize(text):
    '''
    :param text: a string of text
    :return: a list of tokens for the text which has been normalized,
    tokenized and lemmatized
    '''

    # We first normalize and tokenize the test
    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())
    tokens = word_tokenize(text)

    # Then we remove stopwords
    tokens = [w for w in tokens if w not in stopwords.words("english")]

    # We instantiate our lemmatizer and apply it to all of our tokens
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).strip()
        clean_tokens.append(clean_tok)

    return clean_tokens


def make_content_recs(article_id, df_content, m=10, tokenizer=tokenize):
    '''
    INPUT:
    article_id - (int) the article we want to find similar articles to
    m - (int) the number of similar articles we want to find
    df_content - (Pandas dataframe) a dataframe containing content information
    about the articles containing doc_description, article_id as an int

    OUTPUT:
    similar_articles - (list) a list of similar article ID's

    DESCRIPTION:
    We leverage the doc_description (good tradeoff between being descriptive and concise) and use NLP techniques along with
    cosine similarity measure to find documents most similar to one another
    '''
    # first, we drop the elements with missing doc_descriptions
    df_content.dropna(subset=['doc_description'], inplace=True)

    # we create a pipeline to do our processing
    pipeline = Pipeline([
        ('vect', CountVectorizer(tokenizer=tokenizer, stop_words='english')),
        ('tfidf', TfidfTransformer())
    ])

    # we get the representation of the doc and compute the cosine similarity between the doc and all the others
    transformed_text = pipeline.fit_transform(df_content.doc_description)
    article_idx = np.where(df_content.article_id == article_id)[0][0]
    similarity = cosine_similarity(transformed_text[article_idx], transformed_text)[0]

    # we can create a dictionary with the cosine similarity of each article with the article of interest
    similar_articles = dict()
    for idx in range(len(df_content)):
        similar_articles[df_content.iloc[idx]['article_id']] = similarity[idx]

    # we remove the own article, and return the keys associated with the highest value of similarity
    similar_articles.pop(article_id)
    similar_articles = sorted(similar_articles, key=similar_articles.get, reverse=True)[:m]
    similar_articles = [float(int(i)) for i in similar_articles]

    return similar_articles


