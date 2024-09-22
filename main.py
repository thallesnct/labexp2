from dateutil import parser
from datetime import datetime, timezone
import requests
import pandas as pd
import time

GITHUB_TOKEN = "GH_TOKEN_HERE"
GITHUB_GRAPHQL_API_URL = "https://api.github.com/graphql"

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}"
}

query = """
query($cursor: String) {
  search(query: "language:Java sort:stars-desc", type: REPOSITORY, first: 40, after: $cursor) {
    pageInfo {
      endCursor
      hasNextPage
    }
    nodes {
      ... on Repository {
        name
        stargazerCount
        owner {
          login
        }
        createdAt
        releases {
          totalCount
        }
        url
      }
    }
  }
}
"""

def run_query(query, variables):
    response = requests.post(GITHUB_GRAPHQL_API_URL, json={'query': query, 'variables': variables}, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed to run and returned code: {response.status_code}. Text: {response.text}")

repositories_data = []
cursor = None  # Cursor para paginação
progress = 0
current_time = datetime.now(timezone.utc)

while progress < 1000:
    variables = {"cursor": cursor}
    result = run_query(query, variables)
    progress += 40
    print(f"({(progress/1000) * 100}% Progress) Running query with cursor: {cursor}")
    repositories = result["data"]["search"]["nodes"]
    
    # Processar os dados de cada repositório e adicionar à lista
    for repo in repositories:
        repo_data = {
            "name": repo["name"],
            "owner": repo["owner"]["login"],
            "stargazerCount": repo["stargazerCount"],
            "created_at": repo["createdAt"],
            "current_date": current_time,
            "time_since_created_at_in_seconds": (current_time - parser.parse(repo["createdAt"])).total_seconds(),
            "releases_count": repo["releases"]["totalCount"],
            "url": repo["url"],
        }
        repositories_data.append(repo_data)
    
    if result["data"]["search"]["pageInfo"]["hasNextPage"]:
        cursor = result["data"]["search"]["pageInfo"]["endCursor"]
        time.sleep(4)
    else:
        break

# Converter a lista de dados em um DataFrame do pandas
df = pd.DataFrame(repositories_data)

# Calcular o percentual de issues fechadas

# Salvar o DataFrame em um arquivo CSV
df.to_csv('./repo_data/github_repositories_data.csv', index=False)

print("Dados salvos em 'github_repositories_data.csv'.")
