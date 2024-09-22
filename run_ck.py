import pandas as pd
import subprocess

if __name__ == '__main__':
    data = pd.read_csv('./repo_data/github_repositories_data.csv')

    repos_to_clone = data['url'].tolist()

    for (idx, data) in enumerate(repos_to_clone):
        try:
            command = f'java -jar ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar \
                        ./repo_clones/{idx} \
                        true \
                        0 \
                        true \
                        ./resultados/{idx}-resultados.csv'
            
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            print(f'Output:\n{result.stdout}')
            if result.stderr:
                print(f'Error:\n{result.stderr}')
                
        except subprocess.CalledProcessError as e:
            print(f'Command failed with error:\n{e.stderr}')
