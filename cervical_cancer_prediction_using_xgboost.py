# -*- coding: utf-8 -*-
"""Cervical_Cancer_Prediction_Using_XGBoost.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1NLrXaLNTOxbRY0cDgCvmp-XWL_qO6_LN

# Predeicting Cervical Cancer Using XGBoost

### IMPORTING LIBRARIES AND DATASETS
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import zipfile

!pip install plotly
!pip install jupyterthemes
import plotly.express as px

from jupyterthemes import jtplot

jtplot.style(theme = 'monokai', context = 'notebook', ticks = True, grid = False)

cancer_df = pd.read_csv('cervical_cancer.csv')

cancer_df.tail(5)

"""### EXPLORATORY DATA ANALYSIS"""

cancer_df.info()

cancer_df.describe()

# REPLACING '?' WITH NaN

cancer_df = cancer_df.replace('?', np.nan)
cancer_df

# PLOTTING HEATMAP TO VISUALIZE THE NUMBER OF NaN'S IN TH DATA

plt.figure(figsize=(20,20))
sns.heatmap(cancer_df.isnull(), yticklabels = False)
plt.show()

# WE OBSERVE THAT THERE ARE A LOT OF NAN VALUES IN "STD'S: TIME SINCE FIRST DIAGNOSIS" AND "STD'S: TIME SINCE LAST DIAGNOSIS"
# SO WE WILL DROP THESE COLUMNS

cancer_df = cancer_df.drop(['STDs: Time since first diagnosis', 'STDs: Time since last diagnosis'], axis=1)
cancer_df

# Converting the column data types, from object to numeric in order to perform Statistical Analysis of the Data

cancer_df = cancer_df.apply(pd.to_numeric)
cancer_df.info()

cancer_df.describe()

cancer_df.mean()

# REPLACING NULL/NaN values with the mean values:

cancer_df =  cancer_df.fillna(cancer_df.mean())
cancer_df

# PLOTTING HEATMAP AGAIN TO VISUALIZE AND CHECK OUR DATA CLEANSING

plt.figure(figsize=(8,20))
sns.heatmap(cancer_df.isnull(), yticklabels = False)
plt.xticks(rotation=90)
plt.tick_params(labelsize=8)
plt.show()

# THUS WE CAN SEE THAT WE HAVE NO NULL VALUES NOW

cancer_df.describe()

"""THIS THE AGE RANGE FOR PEOPLE INVOLVED IN THE STUDY ARE : (13, 84)

### PERFORMING DATA VISUALIZATION
"""

# WE'LL TRY TO OBSERVE THE CORELATION BETWEEN DIFFERENT FEATURES IN OUR DATASETS:

corr_matrix = cancer_df.corr()

corr_matrix

# PLOTTING THE HEATMAP FOR CORRELATION MATRIX

plt.figure(figsize = (30,30))
sns.heatmap(corr_matrix, annot=True)
plt.xticks(rotation=90)
plt.yticks(rotation=360)
plt.tick_params(labelsize=8)
plt.show()

# VISUALIZING THE WHOLE DATAFRAME BY PLOTTING HISTOGRAM
cancer_df.hist(bins = 10, figsize = (30,30), color='orange')
plt.show()

"""### PREPARING DATA BEFORE TRAINING"""

# WE SELECT BIOPSY DATA AS OUR TARGET VALUES:

target_df = cancer_df['Biopsy']
input_df = cancer_df.drop(['Biopsy'], axis=1)

X = np.array(input_df).astype('float32')
y = np.array(target_df).astype('float32')

y = y.reshape(-1,1)

from sklearn.preprocessing import StandardScaler, MinMaxScaler

scaler = StandardScaler()
X = scaler.fit_transform(X)

X

# SPLITTING DATA INTO TRAIN AND TEST DATASETS
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
X_test, X_val, y_test, y_val = train_test_split(X_test, y_test, test_size = 0.5)

"""### TRAINING AND EVALUATING XGBOOST CLASSIFIER"""

!pip install --upgrade pip
!pip install seaborn
!pip install xgboost

import xgboost as xgb

model = xgb.XGBClassifier(learning_rate = 0.1, max_depth = 50, n_estimators = 100)

model.fit(X_train, y_train)

"""#### TESTING OUT RESULTS OF OUR MODEL"""

result_train = model.score(X_train, y_train)

result_train

result_test = model.score(X_test, y_test)

result_test

y_predict = model.predict(X_test)

from sklearn.metrics import confusion_matrix, classification_report

print(classification_report(y_test, y_predict))

"""#### PLOTTING A CONFUSION MATRIX"""

cm = confusion_matrix(y_predict, y_test)

sns.heatmap(cm, annot = True)

plt.show()

"""# Export and Save the Model"""

import joblib
# Save the trained model to a file
model_filename = 'trained_model.joblib'
joblib.dump(model, model_filename)
print(f"Model saved to {model_filename}")

# Load the trained model from the file
loaded_model = joblib.load(model_filename)
print(f"Model loaded from {model_filename}")