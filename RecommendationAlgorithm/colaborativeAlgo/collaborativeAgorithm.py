class CollaborativeRecommender:
    def __init__(self, ratings_data):       #initializes an instance of the class with ratings_data
        #error handling to ensure the input data is valid.
        if not isinstance(ratings_data, dict):
            raise ValueError("ratings data should be a dictionary")

        # Check if all keys are strings and all values are lists
        for key, value in ratings_data.items():
            if not isinstance(key, str) or not isinstance(value, list):
                raise ValueError("All keys should be strings and all values should be lists")
            
            if not all(isinstance(x, (int, float)) or pandas.isna(x) for x in value):
                raise ValueError("All values in lists should be numeric or NaN.")

        self.ratings = pandas.DataFrame(ratings_data).T
        self.similarity_matrix = None       #will be computed later based on ratings.
    
    def calculate_similarity(self):     #likely between users or items in the dataset based on their ratings.
        self.similarity_matrix = cosine_similarity(self.ratings.fillna(0))      #reeplace any missing values with 0 or null values.
        self.similarity_matrix = pandas.DataFrame(self.similarity_matrix,index=self.ratings.index,columns=self.ratings.index)
        
        """
            similariy_df = pandas.DataFrame(self.similarity_matrix)    #Dataframe creation
            similarity_df.index = self.ratings.index
            similarity_df.columns = self.ratings.index
            self.similarity_matrix = similarity_df
        """

    def Collaborative(self, user, n_recommendations=3):        
        if self.similarity_matrix is None:
            self.calculate_similarity()

        # Get and sort similar users
        similar_users = self.similarity_matrix[user].sort_values(ascending=False)

        # Gather items from similar users
        recommendations = pandas.Series(dtype=float)
        for similar_user in similar_users.index[1:]:  # Skip the user themselves
            user_ratings = self.ratings.loc[similar_user]
            recommendations = pandas.concat([recommendations, user_ratings[user_ratings > 0]])

        # Remove items already rated by the same user
        recommendations = recommendations[~recommendations.index.isin(
            self.ratings.loc[user][self.ratings.loc[user] > 0].index)]

        return recommendations.sort_values(ascending=False).head(n_recommendations)