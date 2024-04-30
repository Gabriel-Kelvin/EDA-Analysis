# -*- coding: utf-8 -*-
"""Intern Assignment.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1G2bAlSU5So5qXXL0cEI04xVWDLgB9_Yj
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
import warnings
warnings.filterwarnings("ignore")

msl_test = pd.read_csv("msl_test.csv")
msl_test_label = pd.read_csv("msl_test_label.csv")
psm_test = pd.read_csv("psm_test.csv")
psm_test_label = pd.read_csv("psm_test_label.csv")
smap_test = pd.read_csv("smap_test.csv")
smap_test_label = pd.read_csv("smap_test_label.csv")
test = pd.read_csv("test.csv")
test_label = pd.read_csv("test_label.csv")

"""MSL Test Dataset"""

print("MSL Test Dataset:")
print("Column Names:")
print(msl_test.columns.tolist())
print("\nInfo:")
print(msl_test.info())
print("\nDescribe:")
print(msl_test.describe())

"""MSL Test Label Dataset"""

print("\nMSL Test Label Dataset:")
print("Column Names:")
print(msl_test_label.head())
print("\nInfo:")
print(msl_test_label.info())
print("\nDescribe:")
print(msl_test_label.describe())

"""PSM Test Dataset"""

print("\nPSM Test Dataset:")
print("Column Names:")
print(psm_test.head())
print("\nInfo:")
print(psm_test.info())
print("\nDescribe:")
print(psm_test.describe())

"""PSM Test Label Dataset"""

print("\nPSM Test Label Dataset:")
print("Column Names:")
print(psm_test_label.columns.tolist())
print("\nInfo:")
print(psm_test_label.info())
print("\nDescribe:")
print(psm_test_label.describe())

"""SMAP Test Dataset"""

print("\nSMAP Test Dataset:")
print("Column Names:")
print(smap_test.columns.tolist())
print("\nInfo:")
print(smap_test.info())
print("\nDescribe:")
print(smap_test.describe())

"""SMAP Test Label Dataset"""

print("\nSMAP Test Label Dataset:")
print("Column Names:")
print(smap_test_label.columns.tolist())
print("\nInfo:")
print(smap_test_label.info())
print("\nDescribe:")
print(smap_test_label.describe())

"""Test Dataset"""

print("\nTest Dataset:")
print("Column Names:")
print(test.columns.tolist())
print("\nInfo:")
print(test.info())
print("\nDescribe:")
print(test.describe())

"""Test Label Dataset"""

print("\nTest Label Dataset:")
print("Column Names:")
print(test_label.columns.tolist())
print("\nInfo:")
print(test_label.info())
print("\nDescribe:")
print(test_label.describe())

# Draw time series plots with anomaly regions
plt.figure(figsize=(12, 6))
plt.plot(psm_test['timestamp_(min)'], psm_test['feature_0'])
plt.xlabel('Timestamp')
plt.ylabel('Feature Value')
plt.title('Time Series Plot for PSM Test Dataset')

# Identify anomaly regions
common_index = psm_test.index.intersection(psm_test_label.index)
anomaly_regions = psm_test_label.loc[common_index][psm_test_label.loc[common_index]['label'] == 1]
plt.scatter(psm_test.loc[anomaly_regions.index, 'timestamp_(min)'], psm_test.loc[anomaly_regions.index, 'feature_0'], color='r', label='Anomalies')
plt.legend()
plt.show()

# Perform EDA and find root cause
print('MSL Test Dataset')
print(msl_test.describe())
print('Correlation Matrix:')
print(msl_test.corr())

print('\nPSM Test Dataset')
print(psm_test.describe())
print('Correlation Matrix:')
print(psm_test.corr())

print('\nSMAP Test Dataset')
print(smap_test.describe())
print('Correlation Matrix:')
print(smap_test.corr())

print('\nTest Dataset')
print(test.describe())
print('Correlation Matrix:')
print(test.corr())

# Supervised Learning (MSL Test Dataset, PSM Test Dataset)
scaler = StandardScaler()
msl_test_scaled = scaler.fit_transform(msl_test)
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(msl_test_scaled, msl_test_label['0'])
feature_importances = pd.Series(model.coef_[0], index=msl_test.columns)
print('\nMSL Test Dataset: Important Features')
print(feature_importances.sort_values(ascending=False))

# Unsupervised Learning (SMAP Test Dataset)
smap_test = pd.read_csv('smap_test.csv')
smap_test_label = pd.read_csv('smap_test_label.csv')

# Handle missing values
smap_test = smap_test.dropna()  # Drop rows with any missing values

# Standardize the data
scaler = StandardScaler()
smap_test_scaled = scaler.fit_transform(smap_test)

# Perform PCA
pca = PCA(n_components=2)
pca_result = pca.fit_transform(smap_test_scaled)

# Perform anomaly detection
model = IsolationForest(contamination=0.1)
model.fit(pca_result)
anomaly_scores = model.decision_function(pca_result)

# Plot the results
plt.figure(figsize=(12, 6))
plt.scatter(pca_result[:, 0], pca_result[:, 1], c=anomaly_scores, cmap='viridis')
plt.colorbar()
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('SMAP Test Dataset Anomaly Detection')
plt.show()