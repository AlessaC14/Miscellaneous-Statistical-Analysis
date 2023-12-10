import numpy as np
import pandas as pd

def generate_allele_counts(allele_frequency, strength_of_assortative_mating, n):
    return _generate_allele_counts(allele_frequency, strength_of_assortative_mating, n)


def _generate_allele_counts(allele_frequency, strength_of_assortative_mating, n):
    assert isinstance(allele_frequency, (int, float)) and 0 <= allele_frequency <= 1, "Allele frequency must be between 0 and 1 inclusive"
    assert isinstance(strength_of_assortative_mating, (int, float)) and 0 <= strength_of_assortative_mating <= 1, "Strength of assortative mating must be between 0 and 1 inclusive"

    extreme_assortative_mating = 2 * np.random.binomial(1, allele_frequency, n)
    no_assortative_mating = np.random.binomial(2, allele_frequency, n)

    return np.where(np.random.binomial(1, strength_of_assortative_mating, n),
                    extreme_assortative_mating,
                    no_assortative_mating)


# Functions from efficiency.py
p = 0.12345

def genotypes():
    genotypes = pd.DataFrame({'allele_count': np.random.binomial(2, p, 1000)})
    return genotypes

def method1(df):
    var_method1 = df['allele_count'].var()
    return var_method1

def method2(df):
    allele_mean = df['allele_count'].mean()
    variance = allele_mean * (2-allele_mean)/2
    return variance

# Dataframe for storing variance
variance_estimates = pd.DataFrame({'method1': np.zeros(2000), 'method2': np.zeros(2000)})

# For loop to repeat 2000 times
for i in range(2000):
    geno_df = genotypes()
    variance_estimates.at[i, 'method1'] = method1(geno_df)
    variance_estimates.at[i, 'method2'] = method2(geno_df)

def compute_variance(allele_frequency, strength_of_assortative_mating):
    # Check user input -- should be numbers from 0 to 1
    assert isinstance(allele_frequency, (int, float)) and 0 <= allele_frequency <= 1, "Allele frequency must be between 0 and 1 inclusive"
    assert isinstance(strength_of_assortative_mating, (int, float)) and 0 <= strength_of_assortative_mating <= 1, "Strength of assortative mating must be between 0 and 1 inclusive"

    variance_if_independent = 2 * allele_frequency * (1 - allele_frequency)
    variance_if_identical = 4 * allele_frequency * (1 - allele_frequency)

    return strength_of_assortative_mating * variance_if_identical + (1 - strength_of_assortative_mating) * variance_if_independent

# Check the math. These should all be roughly the same.
print(compute_variance(0.5, 0.5))
print(np.var(generate_allele_counts(0.5, 0.5, 100000)))
print(compute_variance(0.3, 0.3))
print(np.var(generate_allele_counts(0.3, 0.3, 100000)))
print(compute_variance(0.3, 0))
print(np.var(generate_allele_counts(0.3, 0, 100000)))
print(compute_variance(0.3, 1))
print(np.var(generate_allele_counts(0.3, 1, 100000)))


# How to read a CSV into Python as a dataframe

# If you want to pull it straight from the course website using a URL
allele_counts = pd.read_csv("https://raw.githubusercontent.com/ekernf01/HEART_choosing_stat_methods/main/course%20content/4_mistaken_assumptions/demo_data/demo1.csv")

# Simulate allele counts for 1 locus in 1000 people
allele_counts = generate_allele_counts(0.5, 0.9, 1000)
print(allele_counts)

#Methods from efficiency session
def method1(df):
    var_method1 = df['allele_count'].var()
    return var_method1

def method2(df):
    allele_mean = df['allele_count'].mean()
    variance = allele_mean * (2-allele_mean)/2
    return variance


# Convert allele_counts to DataFrame
allele_counts_df = pd.DataFrame({'allele_count': allele_counts})

# Estimate variance using method1 and method2
var_method1 = method1(allele_counts_df)
var_method2 = method2(allele_counts_df)

# Store results in a separate dataframe
variance_df = pd.DataFrame({
    'Method1': [var_method1],
    'Method2': [var_method2]
})

print(variance_df)

#Initializing DatFrame
results_df = pd.DataFrame(columns=['Method1', 'Method2'])

#Using loop to repeat process 2000 times
for i in range(2000):
    # Generate allele counts
    allele_counts = generate_allele_counts(0.5, 0.5, 1000)  
    allele_counts_df = pd.DataFrame({'allele_count': allele_counts})

    # Estimate variance using method1 and method2
    var_method1 = method1(allele_counts_df)
    var_method2 = method2(allele_counts_df)

#Storing results in DF
results_df.loc[i] = [var_method1, var_method2]

print(results_df)

#Determining which method is more accurate
# Compute the true variance for all simulations
true_variances = [compute_variance(0.5, 0.5) for i in range(2000)]  

# Compute the average absolute difference for method1
avg_diff_method1 = np.mean(np.abs(variance_estimates['method1'] - true_variances))

# For method2
avg_diff_method2 = np.mean(np.abs(variance_estimates['method2'] - true_variances))

print(f"Average absolute difference for Method 1: {avg_diff_method1}")
print(f"Average absolute difference for Method 2: {avg_diff_method2}")

if avg_diff_method1 < avg_diff_method2:
    print("Method 1 is closer to the truth on average.")
else:
    print("Method 2 is closer to the truth on average.")
