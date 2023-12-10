import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors

def simulate_allele_counts(p):
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

    variance_estimates = pd.DataFrame(columns=['method1', 'method2'], index=range(2000))

    for i in range(2000):
        genotype_df = genotypes()
        var1 = method1(genotype_df)
        var2 = method2(genotype_df)

        variance_estimates.loc[i, 'method1'] = var1
        variance_estimates.loc[i, 'method2'] = var2

    sns.scatterplot(data=variance_estimates, x='method1', y='method2')
    plt.title("Scatterplot of Method 1 vs Method 2")
    plt.show()

    actual_variance = 2 * p*(1-p)
    print(f"Actual Variance: {actual_variance}")
    variance_mean_method1 = variance_estimates['method1'].mean()
    variance_mean_method2 = variance_estimates['method2'].mean()

    print(f"Method 1 Variance: {variance_mean_method1}")
    print(f"Method 2 Variance: {variance_mean_method2}")

    # Color the histograms based on difference from actual variance
    def color_histogram(data, method, bins):
        hist, bin_edges = np.histogram(data[method], bins=bins)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        colors = [mcolors.to_hex(plt.cm.RdBu_r((center - actual_variance) / max(abs(bin_centers - actual_variance)))) for center in bin_centers]
        sns.histplot(data=data, x=method, bins=bins, palette=colors)
        plt.axvline(actual_variance, color='black', linestyle='--', label='Actual Variance')
        plt.legend()
        plt.title(f"{method} histogram (bins={bins})")
        plt.show()

    color_histogram(variance_estimates, 'method1', 15)
    color_histogram(variance_estimates, 'method2', 15)

# Testing the function with three different allele frequencies
simulate_allele_counts(0.12345)
simulate_allele_counts(0.5)
simulate_allele_counts(0.9)


