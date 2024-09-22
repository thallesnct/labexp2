import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == '__main__':
    data = pd.read_csv('./summarized_repo_data.csv')
    
    labels_compare_to = ['Popularidade', 'Maturidade', 'Atividade', 'Tamanho']
    compare_to = ['stargazer_count', 'age_in_years', 'releases_count', 'loc']
    labels_columns = ['CBO', 'CBO (Média)', 'CBO (Desvio Padrão)', 'CBO (Mediana)', 'DIT', 'DIT (Média)', 'DIT (Desvio Padrão)', 'DIT (Mediana)', 'LCOM', 'LCOM (Média)', 'LCOM (Desvio Padrão)', 'LCOM (Mediana)']
    columns = ['cbo', 'cbo_avg', 'cbo_std', 'cbo_mdn', 'dit', 'dit_avg', 'dit_std', 'dit_mdn', 'lcom', 'lcom_avg', 'lcom_std', 'lcom_mdn']
    
    for (idx_metric, metric) in enumerate(compare_to):
        for (idx_column, column) in enumerate(columns):
            fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(8, 10))
            
            sns.barplot(data=data, x='repo_idx', y=metric, ax=axes[0], color='lightblue')
            axes[0].set_title(f'{labels_compare_to[idx_metric]} por repositório')
            axes[0].set_xlabel('Item')
            axes[0].set_ylabel(f'{labels_compare_to[idx_metric]}')

            sns.barplot(data=data, x='repo_idx', y=column, ax=axes[1], color='black')
            axes[1].set_title(f'{labels_columns[idx_column]} por repositório')
            axes[1].set_xlabel('Item')
            axes[1].set_ylabel(f'{labels_columns[idx_column]}')

            plt.tight_layout()

            plt.savefig(f'./charts/{metric}-vs-{column}.png', format='png')