#Expected value and variance
from scipy.stats import binom

def binomial_stats(n, p):
 
    pmf = [binom.pmf(k, n, p) for k in range(n+1)]
    
   
    expect = sum([k * prob for k, prob in enumerate(pmf)])
    
    # Variance
    expect_squared = sum([k**2 * prob for k, prob in enumerate(pmf)])
    variance = expectation_squared - expectation**2
    
    return expect, variance


n, p = 2, 1/3
print(binomial_stats(n, p))

#Estimating mean and variance from sample
import numpy as np
import scipy.stats as stats


n, p = 25, 0.12345
samples = stats.binom(n, p).rvs(10000)


sample_mean = np.mean(samples)
sample_variance = np.var(samples)


expected_mean, expected_variance = binomial_stats(n, p)

print(f"Sample Mean: {sample_mean}, Expected Mean: {expected_mean}")
print(f"Sample Variance: {sample_variance}, Expected Variance: {expected_variance}")
