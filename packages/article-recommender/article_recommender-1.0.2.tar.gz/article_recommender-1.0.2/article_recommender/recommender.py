import numpy as np
import pandas as pd
from . import recommender_helper_functions as rf

class ArticleRecommender():
    '''
    This Recommender uses a mix of FunkSVD and content-based methods to make recommendations
    for existing users, both for existing and brand new articles.
    For brand new users, in absence of any information the top rated articles (calculated as
    the number of interactions) will be recommended
    This recommender can also predict ratings for all user-article pairs (including brand new
    articles), with the exception of brand new users
    '''
    def __init__(self):
        '''
        We initialize all the attributes
        '''
        self.df = None
        self.df_content = None
        self.user_item_df = None
        self.user_item = None
        self.iters = None
        self.latent_features = None
        self.user_mat = None
        self.article_mat = None
        self.n_articles = None
        self.n_users = None
        self.learning_rate = None
        self.user_ids_series = None
        self.article_ids_series = None
        self.num_interactions = None
        self.ranked_articles = None

    def load_data(self, interactions_path, content_path, csv=True,
                  interactions=None, content=None):
        '''
        INPUT
        interactions_path - (str) path to a CSV file containing information about interactions
        between users and articles. It must include user_id (int), article_id (a float of the form
        20.0) and title
        content_path - (str) path to a CSV file containing information about the content of the
        articles. It must include article_id (as an int) and doc_description
        between users and articles. It must include user_id, article_id and title
        csv -(bool) a Boolean specifying whether the document is a CSV file or an already
        existing Pandas dataframe
        interactions - (pandas dataframe) contains information about interactions
        between users and articles. It must contain user_id, article_id (a string of the form
        '20.0') and title
        content -(pandas dataframe) contains information about the content of the
        articles. It must include article_id (as an int) and doc_description

        OUTPUT
        None, updates the following attributes
        self.df - (pandas dataframe) (pandas dataframe) contains information about interactions
        between users and articles
        self.df_content - (pandas dataframe) contains information about the content of the
        articles
        '''

        if csv:
            self.df = pd.read_csv(interactions_path)
            self.df_content = pd.read_csv(content_path)

        else:
            self.df = interactions
            self.df_content = content

        if not self.df.user_id.dtype == 'int64':
            try:
                self.df.user_id.astype('int64')
            except:
                print('The user ID in the interactions dataset cannot be converted to an integer. Please modify and reload the data')

        if not self.df.article_id.dtype == 'float64':
            try:
                self.df.article_id.astype('float64')
            except:
                print('The article ID in the interactions dataset cannot be converted to a float. Please modify and reload the data')

        if not self.df_content.article_id.dtype == 'int64':
            try:
                self.df_content.article_id.astype('int64')
            except:
                print('The article ID in the content dataset cannot be converted to an integer. Please modify and reload the data')

    def fit(self, latent_features=12, learning_rate=0.0001, iters=100):
        '''
        This function performs matrix factorization using a basic form of FunkSVD with no regularization

        INPUT:
        latent_features - (int) the number of latent features used
        learning_rate - (float) the learning rate
        iters - (int) the number of iterations

        OUTPUT:
        None - stores the following as attributes:
        n_users - the number of users (int)
        n_articles - the number of articles (int)
        num_interactions - the number of interactions calculated (int)
        user_item_df - (pandas df) a user by item dataframe with interactions and nans for values
        user_item - (np array) a user by item numpy array with interactions and nans for values
        latent_features - (int) the number of latent features used
        learning_rate - (float) the learning rate
        iters - (int) the number of iterations
        user_ids_series - (series) all the user_id's contained in our dataset
        article_ids_series - (series) all the article id's contained in our dataset
        user_mat - (np array) the user matrix resulting from FunkSVD
        article_mat - (np array) the item matrix resulting from FunkSVD
        ranked_articles - (pandas dataframe) a dataframe with articles ranked by their number of interactions
        '''

        # Create user-item matrix
        self.user_item_df = rf.create_user_item_matrix(self.df)
        self.user_item = np.array(self.user_item_df)

        # Store more inputs
        self.latent_features = latent_features
        self.learning_rate = learning_rate
        self.iters = iters

        # Set up useful values to be used through the rest of the function
        self.n_users = self.user_item_df.shape[0]
        self.n_articles = self.user_item_df.shape[1]
        self.num_interactions = self.user_item_df.sum().sum()
        self.user_ids_series = np.array(self.user_item_df.index)
        self.article_ids_series = np.array(self.user_item_df.columns)

        # initialize the user and article matrices with random values
        user_mat = np.random.rand(self.n_users, self.latent_features)
        article_mat = np.random.rand(self.latent_features, self.n_articles)

        # initialize sse at 0 for first iteration
        sse_accum = 0

        # keep track of iteration and MSE
        print("Optimization Statistics")
        print("Iterations | Mean Squared Error ")

        # for each iteration
        for iteration in range(self.iters):

            # update our sse
            old_sse = sse_accum
            sse_accum = 0

            # For each user-article pair
            for i in range(self.n_users):
                for j in range(self.n_articles):

                    # if the rating exists
                    if self.user_item[i, j] > 0:

                        # compute the error as the actual minus the dot product of the user and article latent features
                        diff = self.user_item[i, j] - np.dot(user_mat[i, :], article_mat[:, j])

                        # Keep track of the sum of squared errors for the matrix
                        sse_accum += diff**2

                        # update the values in each matrix in the direction of the gradient
                        for k in range(self.latent_features):
                            user_mat[i, k] += self.learning_rate * (2*diff*article_mat[k, j])
                            article_mat[k, j] += self.learning_rate * (2*diff*user_mat[i, k])

            # print results
            print("%d \t\t %f" % (iteration+1, sse_accum / self.num_interactions))

        # SVD based fit
        # Keep user_mat and article_mat for safe keeping
        self.user_mat = user_mat
        self.article_mat = article_mat

        # Knowledge based fit
        self.ranked_articles = rf.rank_articles(self.df)

    def predict_interactions(self, user_id, article_id):
        '''
        INPUT:
        user_id - (int) the user_id from interactions df
        article_id - (int) the article_id according the interactions df
        doc_description
        df_content - updated content dataframe with the new article to predict

        OUTPUT:
        pred - the predicted rating for user_id-movie_id according to FunkSVD

        Description: we have four cases that we want to treat differently:
            - if both the user_id and article_id are in the interactions df, we use the
            results from FunkSVD
            - if the user_id is in interactions df but the article ID is not (it is brand new),
            if it is in the content dataframe then we use content-based filtering to predict ratings
            based on ratings of similar movies
            - if the user_id is not in the interactions df, we cannot make any predictions
            - if the article_id is neither in the content or interaction dataset then we cannot predict anything
        '''

        # we first deal with the case where both user and article are in the interactions dataframe
        try:
            user_row = np.where(self.user_ids_series == user_id)[0][0]
            article_col = np.where(self.article_ids_series == float(article_id))[0][0]

            # Take dot product of that row and column in U and V to make prediction
            pred = np.dot(self.user_mat[user_row, :], self.article_mat[:, article_col])

            article_name = rf.get_article_names([article_id], self.df)[0]
            print("For user {} we predict {} interactions with the article: '{}'.".format(user_id,
                                                                                      round(pred, 2),
                                                                                      article_name))

            return pred

        except:
            # then we deal with the case where this is a new article (in the content dataset), we find the rating
            # based on rating of similar movies. If no interaction with any similar article, we
            # predict 0
            if (article_id in self.df_content.article_id.values.tolist()) | (article_id in self.article_ids_series):
                if user_id in self.user_ids_series:
                    similar_articles = rf.make_content_recs(article_id, self.df_content)
                    user_row = np.where(self.user_ids_series == user_id)[0][0]
                    article_col = np.where(np.isin(self.article_ids_series, similar_articles))[0][0]
                    ratings = self.user_item[user_row,article_col]
                    article_name = self.df_content.loc[self.df_content.article_id == article_id,
                                                       'doc_full_name'].values[0]
                    if np.isnan(ratings.mean()):
                        pred = 0
                    else:
                        pred = ratings.mean()
                    print("For user {}, using ratings on similar articles, we predict {} interactions with the article: '{}'.".format(user_id,
                                                                                        round(pred,2),
                                                                                        article_name))

                    return pred
                else:
                    print('The user ID provided is not in the interactions df. No prediction can be made')
                    return None

            # finally, if the article ID isn't in the content dataset, we cannot make a prediction
            else:
                print('The provided article ID is not in the interactions nor content dataset. No prediction can be made')
                return None

    def make_recommendations(self, _id, _id_type='user', rec_num=5):
        '''
        INPUT:
        _id - either a user or movie id (int)
        _id_type - "article" or "user" (str)
        rec_num - number of recommendations to return (int)

        OUTPUT:
        recs - (array) a list or numpy array of recommended movies like the
                       given movie, or recs for a user_id given

        DESCRIPTION:
        If the user is available in the interactions dataset, we use the matrix factorization data.
        If the user is new we simply return the top rec_num articles
        If we are trying to recommend based on an article, we will use a content-based recommendation system
        '''
        rec_ids, rec_names = None, None
        if _id_type == 'user':
            if _id in self.user_ids_series:
                # Get the index of which row the user is in for use in U matrix
                idx = np.where(self.user_ids_series == _id)[0][0]

                # take the dot product of that row and the V matrix
                preds = np.dot(self.user_mat[idx,:],self.article_mat)

                # pull the top articles according to the prediction
                indices = preds.argsort()[-rec_num:][::-1] #indices
                rec_ids = self.article_ids_series[indices].tolist()
                rec_names = rf.get_article_names(rec_ids, self.df)
                print('For user ID {}, we recommend the article IDs {} with titles {}'.format(_id, rec_ids, rec_names))

            else:
                # if we don't have this user, give just top ratings back
                rec_ids = self.ranked_articles.iloc[:rec_num]['article_id'].values.tolist()
                rec_names = self.ranked_articles.iloc[:rec_num]['title'].values.tolist()
                print("Because this user with ID {} wasn't in our database, we are giving back the top movie recommendations for all users. \n".format(_id))
                print("The top article ID's are {}, with titles {}".format(rec_ids, rec_names))

        # Find similar articles if it is a movie that is passed
        else:
            if _id in self.df_content.article_id.tolist():
                rec_ids = rf.make_content_recs(_id, self.df_content, m=rec_num)
                rec_names = rf.get_article_names(rec_ids, self.df)
                print('The articles most similar to article ID {} have IDs {}, and titles {}'.format(_id, rec_ids, rec_names))
            else:
                print("That article doesn't exist in our database.  Sorry, we don't have any recommendations for you.")

        return rec_ids, rec_names

