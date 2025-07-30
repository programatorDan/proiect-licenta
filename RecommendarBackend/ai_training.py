from sklearn.model_selection import train_test_split
from keras.layers import Input, Embedding, Flatten, Dense, Concatenate
from keras.models import Model
from keras.optimizers import Adam
import pandas as pd

ratings_df = pd.read_csv('dataset/rating.csv').head(10000)
num_users = ratings_df['userId'].nunique()

train, test = train_test_split(ratings_df, test_size=0.2)

embedding_size = 50

user_input = Input(shape=(1,))
movie_input = Input(shape=(1,))

user_embedding = Embedding(input_dim=num_users + 1, output_dim=embedding_size)(user_input)
movie_embedding = Embedding(input_dim=ratings_df['movieId'].max() + 1, output_dim=embedding_size)(movie_input)

user_vec = Flatten()(user_embedding)
movie_vec = Flatten()(movie_embedding)

concat = Concatenate()([user_vec, movie_vec])
dense = Dense(64, activation='relu')(concat)
output = Dense(1)(dense)

model = Model(inputs=[user_input, movie_input], outputs=output)
model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')

model.fit([train['userId'], train['movieId']], train['rating'], epochs=5, verbose=1)

model.save('./models/Model.h5')
