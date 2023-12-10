import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import statsmodels.api as statsmodels

# Simulating data
regression_demo = pd.DataFrame({
    'constant': 1,
    'x1': np.random.choice(np.repeat(range(1, 11), 5), 550),
    'x2': np.random.choice(np.repeat(range(1, 11), 5), 550),
    'x3': np.random.choice(np.repeat(range(1, 11), 5), 550)
})

def make_noise(n):
    return np.random.binomial(n, 0.5, size=n)

regression_demo['y'] = regression_demo['x1']*11 + regression_demo['x2']*1 + make_noise(len(regression_demo))

# Plotting
plt.figure(figsize=(5, 5))
plt.scatter(regression_demo['x1'], regression_demo['y'])
plt.title("Y depends strongly on x1")
plt.xlabel("x1")
plt.ylabel("y")
plt.show()

plt.figure(figsize=(5, 5))
plt.scatter(regression_demo['x2'], regression_demo['y'] - regression_demo['x1']*10.1)
plt.title("Y depends weakly on x2")
plt.xlabel("x2")
plt.ylabel("y (adjusted for X1's effect)")
plt.show()

plt.figure(figsize=(5, 5))
plt.scatter(regression_demo['x3'], regression_demo['y'])
plt.title("Y is independent of x3")
plt.xlabel("x3")
plt.ylabel("y")
plt.show()

# Hypothesis testing
mod = statsmodels.OLS(regression_demo['y'], regression_demo.drop('y', axis = 1)).fit()
print("Model parameters:")
print(mod.params)
print("p-values:")
print(mod.pvalues)

plt.figure(figsize=(5, 5))
plt.scatter(regression_demo['y'], mod.predict())
plt.title("Model predictions versus actual y")
plt.xlabel("Actual y")
plt.ylabel("Predicted y")
plt.show()

# Leave-one-out cross validation
different_variable_subsets = {
    'simple': ['x1'],
    'medium': ['x1', 'x2'],
    'complex': ['x1', 'x2', 'x3']
}

leave_one_out_prediction_error = {'simple': 0, 'medium': 0, 'complex': 0}
for i in range(len(regression_demo)):
    for m in ['simple', 'medium', 'complex']:
        train_data = regression_demo.drop(i)
        my_model = LinearRegression()
        _ = my_model.fit(train_data[different_variable_subsets[m]], train_data['y'])
        predicted_y = my_model.predict(regression_demo.iloc[[i]][different_variable_subsets[m]])
        true_y = regression_demo.iloc[i]['y']
        leave_one_out_prediction_error[m] = leave_one_out_prediction_error[m] + (predicted_y - true_y)**2

leave_one_out_prediction_error = pd.Series(leave_one_out_prediction_error)
print("Leave-one-out prediction errors:", leave_one_out_prediction_error)


whole_dataset_prediction_error = {'simple': 0, 'medium': 0, 'complex': 0}
for m in ['simple', 'medium', 'complex']:
    my_model = LinearRegression()
    _ = my_model.fit(regression_demo[different_variable_subsets[m]], regression_demo['y'])
    whole_dataset_prediction_error[m] = np.sum((
        my_model.predict(regression_demo[different_variable_subsets[m]]) - 
        regression_demo['y']
    )**2)

