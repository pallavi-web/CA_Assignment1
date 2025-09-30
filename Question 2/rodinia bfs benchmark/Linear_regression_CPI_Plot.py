import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import nnls
from sklearn.metrics import mean_squared_error, r2_score

# Load data
df = pd.read_csv('data2.csv')
df['CPI'] = df['cpu-cycles'] / df['instructions']

# Select features for CPI stack
features = ['l1i-misses', 'l1d-misses', 'l2-misses', 'l3-misses',
            'itlb-misses', 'dtlb-misses', 'branch-misses']
X = df[features].values
y = df['CPI'].values

# NNLS (non-negative least squares)
coef_nnls, _ = nnls(X, y)
y_pred = np.dot(X, coef_nnls)
residuals = y - y_pred

# Statistical measures
rmse = np.sqrt(mean_squared_error(y, y_pred))
r2 = r2_score(y, y_pred)
n = len(y)
p = len(features)
adj_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)

print("CPI Stack coefficients:", coef_nnls)
print("RMSE:", rmse)
print("R2:", r2)
print("Adjusted R2:", adj_r2)
print("Residuals:", residuals)

# Plot CPI stack\
plt.figure(figsize=(8,6))
plt.bar(features, coef_nnls)
plt.ylabel("CPI Contribution per Event")
plt.title("CPI Stack")
plt.tight_layout()
plt.show()

import statsmodels.api as sm
model = sm.OLS(y, X).fit()
f_statistic = model.fvalue
p_value = model.f_pvalue
print("F-statistic:", f_statistic)
print("p-value:", p_value)
