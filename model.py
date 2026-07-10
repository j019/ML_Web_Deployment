# Importing the libraries
import numpy as np
import pandas as pd
import pickle

dataset = pd.read_csv('house_price_prediction.csv')

top_6 = ['sqft_living15','sqft_above','grade',
'condition','bedrooms','floors']

X = dataset.loc[:, top_6]

y = dataset['price']

from sklearn.linear_model import Ridge
regressor = Ridge(random_state=7)

#Fitting model with trainig data
regressor.fit(X, y)

# Saving model to disk
pickle.dump(regressor, open('model.pkl','wb'))

# Loading model to compare the results
model = pickle.load(open('model.pkl','rb'))
print(model.predict([[1440,1730,7,3,3,2]]))

