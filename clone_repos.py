import pandas as pd
import subprocess

if __name__ == '__main__':
    data = pd.read_csv('./repo_data/github_repositories_data.csv')

    repos_to_clone = data['url'].tolist()

    for (idx, repo) in enumerate(repos_to_clone):
        try:
            command = f'git clone {repo} ./repo_clones/{idx}'
            print(f'Executing: {command}')
            
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            print(f'Output:\n{result.stdout}')
            if result.stderr:
                print(f'Error:\n{result.stderr}')
                
            command = f'cd ./repo_clones/{idx} && rm -rf .git && cd ..'
            print(f'Executing: {command}')
            
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                
        except subprocess.CalledProcessError as e:
            print(f'Command failed with error:\n{e.stderr}')
