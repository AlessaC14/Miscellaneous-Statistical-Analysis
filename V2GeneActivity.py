import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf

def plot_gene_activity(gene_num, regression_type):
    data_url = "https://raw.githubusercontent.com/ekernf01/HEART_choosing_stat_methods/main/course%20content/5_outlier_robustness/SyntheticGeneActivityData.csv"
    GeneActivity = pd.read_csv(data_url, index_col=0).T

    gene_col = f"x_g{gene_num}"
    velocity_col = f"velocity_x_g{gene_num}"

    plt.figure(figsize=(5, 5))
    plt.plot(GeneActivity[gene_col], GeneActivity[velocity_col], 'o')
    plt.xlabel("RNA concentration")
    plt.ylabel("RNA velocity")
    plt.title(f"RNA decay dynamics for Gene {gene_num}")

    if regression_type == "least-squares":
        model = smf.ols(f"{velocity_col} ~ {gene_col}", data=GeneActivity).fit()
        plt.plot(GeneActivity[gene_col], model.predict(GeneActivity[gene_col]), color="red", label="Least-Squares Line of Best Fit")
        
    elif regression_type == "quantile":
        model = smf.quantreg(f"{velocity_col} ~ {gene_col}", data=GeneActivity).fit(q=0.5)
        plt.plot(GeneActivity[gene_col], model.predict(GeneActivity[gene_col]), color="blue", label="Quantile Regression")

    plt.legend()
    plt.savefig(f"gene{gene_num}_rna_vs_rna_velocity_{regression_type}.png")
    plt.show()

# Test the function
genes_to_test = [1, 5, 16, 18]
for gene in genes_to_test:
    plot_gene_activity(gene, "least-squares")
    plot_gene_activity(gene, "quantile")
