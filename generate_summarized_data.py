import pandas as pd
import subprocess

if __name__ == '__main__':
    data = pd.read_csv('./repo_data/github_repositories_data.csv')
    summarized_class_data = pd.DataFrame(columns=[
        'repo_idx', 
        'dit', 
        'dit_avg', 
        'dit_std', 
        'dit_mdn', 
        'loc', 
        'cbo', 
        'cbo_avg', 
        'cbo_std', 
        'cbo_mdn', 
        'lcom', 
        'lcom_avg', 
        'lcom_std', 
        'lcom_mdn', 
        'stargazer_count', 
        'releases_count', 
        'age_in_years'
    ])
    empty_repos = list()

    repos_to_clone = data['url'].tolist()

    for (idx, _) in enumerate(repos_to_clone):
        dataframe_lint = pd.read_csv(f'./ck-results/{idx}-resultados.csvclass.csv')
        summarized_class_values = dataframe_lint[['dit', 'loc', 'cbo', 'lcom']].sum()
        average = dataframe_lint[['dit', 'cbo', 'lcom']].mean()
        standard_deviation = dataframe_lint[['dit', 'cbo', 'lcom']].std()
        median = dataframe_lint[['dit', 'cbo', 'lcom']].median()
        
        if (summarized_class_values['dit'] == 0 and
            summarized_class_values['loc'] == 0 and
            summarized_class_values['cbo'] == 0 and 
            summarized_class_values['lcom'] == 0):
            empty_repos.append(f'{idx}')
            continue
            
        summarized_class_data.loc[idx] = [
            idx,
            summarized_class_values['dit'], 
            average['dit'],
            standard_deviation['dit'],
            median['dit'],
            summarized_class_values['loc'], 
            summarized_class_values['cbo'], 
            average['cbo'],
            standard_deviation['cbo'],
            median['cbo'],
            summarized_class_values['lcom'], 
            average['lcom'],
            standard_deviation['lcom'],
            median['lcom'],
            data.at[idx, 'stargazerCount'], 
            data.at[idx, 'releases_count'], 
            (data.at[idx, 'time_since_created_at_in_seconds'] / (365.25 * 24 * 60 * 60)) 
        ]
            
    summarized_class_data.to_csv('./repo_data/summarized_repo_data.csv')
    print("Dados sumarizados salvos em 'summarized_repo_data.csv'.")
    with open("./repo_data/empty_repos.txt", "w") as outfile:
        outfile.write("\n".join(empty_repos))
    print("Lista de repositórios com métricas vazias salva em 'empty_repos.txt'.")