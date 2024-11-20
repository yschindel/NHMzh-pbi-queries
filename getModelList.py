import requests
import pandas as pd

def get_model_list(project):
    url = "http://localhost:3000/data/models"
    params = {"project": project}
    
    response = requests.get(url, params=params)
    return response.json()

# Example usage
result = get_model_list("juch-areal")

print(result)
# convert to pandas dataframe
df = pd.DataFrame(result)

print(df)

