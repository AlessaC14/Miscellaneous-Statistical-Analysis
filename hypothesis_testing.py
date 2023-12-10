rejects_beta2 = 0
rejects_beta3 = 0

for _ in range(1000):

       # Perform hypothesis testing
    p_values = mod.pvalues
    if p_values['x2'] < 0.10:  # If p-value for beta2 is less than 0.10
        rejects_beta2 += 1
    if p_values['x3'] < 0.10:  # If p-value for beta3 is less than 0.10
        rejects_beta3 += 1
# Calculate the percentage of rejections
percent_rejects_beta2 = (rejects_beta2 / 1000) * 100
percent_rejects_beta3 = (rejects_beta3 / 1000) * 100

#report the results in a table format
results_table = pd.DataFrame({
    'Method': ['Fitting error', 'LOOCV', 'Hypothesis tests'],
    'includes X2': [fitting_error_X2, loocv_error_X2, percent_rejects_beta2],
    'includes X3': [fitting_error_X3, loocv_error_X3, percent_rejects_beta3]
})

print(results_table)