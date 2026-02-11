import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from keras.layers import Input, Dense, Dropout
from keras.models import Model
from keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
from sklearn.model_selection import StratifiedKFold
from keras.callbacks import History
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import sigmoid_kernel


class ProductRecommender( ):
    
    def __init__(self, product_file):
        self.product = pd.read_excel(product_file)
        self.data = self.product
        self.product_df = self.product.drop(["product","usual_storage","product_id","shelf_life","serving_size_g"],axis=1)
        self.product_df.reset_index(inplace = True, drop = True)
        self.corr_features = self.correlation(self.product_df, 0.70)
        self.product_df = self.product_df.drop(list(self.corr_features), axis=1)
        self.scaler = MinMaxScaler()
        self.product_df = self.scaler.fit_transform(self.product_df)
        self.history = History()
        # Train encoder-decoder model
        self.history = History()
        self.autoencoder = self.build(training=True)
        self.autoencoder.compile(optimizer=Adam(lr=0.001), loss='binary_crossentropy',metrics=['accuracy'])
        self.autoencoder.fit(self.product_df, self.product_df, epochs=100, batch_size=128,validation_split=0.33,callbacks=[self.history])
        self.autoencoder.save_weights("output.h5")
        # Encode product features
        self.prediction_model = self.build(training=False)
        self.prediction_model.load_weights("output.h5", by_name=True)
        self.encoded_product_features = self.prediction_model.predict(self.product_df)
        self.similarity_matrix = self.encoded_product_features
        #.foods = self.get_recommendations()
        #print(self.foods)


    def correlation(self, dataset, threshold):
        col_corr = set()  # Set of all the names of correlated columns
        corr_matrix = dataset.corr()
        for i in range(len(corr_matrix.columns)):
            for j in range(i):
                if (corr_matrix.iloc[i, j]) > threshold: # we are interested in absolute coeff value
                    colname = corr_matrix.columns[i]  # getting the name of column
                    col_corr.add(colname)
        return col_corr
    


    def build(self, training=True):
        input_layer = Input(shape=(self.product_df.shape[1],))
        encoder_layer = Dense(256, activation='relu')(input_layer)
        encoder_layer = Dropout(0.2)(encoder_layer)
        encoder_layer = Dense(128, activation='relu')(encoder_layer)
        encoder_layer = Dropout(0.2)(encoder_layer)
        encoder_layer = Dense(64, activation='relu')(encoder_layer)
        encoded = Dense(32, activation='sigmoid')(encoder_layer)

        # Define decoder model
        decoder_layer = Dense(64, activation='relu')(encoded)
        decoder_layer = Dropout(0.2)(decoder_layer)
        decoder_layer = Dense(128, activation='relu')(decoder_layer)
        decoder_layer = Dropout(0.2)(decoder_layer)
        decoder_layer = Dense(256, activation='relu')(decoder_layer)
        decoded = Dense(self.product_df.shape[1], activation='sigmoid')(decoder_layer)

        # Define encoder-decoder model
        if training:
            autoencoder = Model(input_layer, decoded)
        else:
            autoencoder = Model(input_layer, encoded)
        return autoencoder




    def get_recommendations(self,food):
        
        # Get the index of the given food
        idx = self.data.index[self.data['product']==food][0]
        
        # Get the cosine similarity scores between the given food and all other foods
        sim_scores =  self.similarity_matrix[idx]
        
        # Get indices of top 10 foods based on similarity scores
        top_indices = np.argsort(sim_scores)[::-1][:5]
        
        # Get recommended foods from data based on top indices
        recommended_foods = self.data.iloc[top_indices]
        
        return recommended_foods['product'].tolist()
       





y = ProductRecommender('D:\\UoE_Notes\\Assignment\\Group_Project\\Recommadation_Engine\\_nosh_product_data.xlsx')
x = y.get_recommendations('strawberry')
print(x)






















































































