import requests
import pandas as pd


def get_file_names(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Server returned status {response.status_code}: {response.text}")
    return response.json()

# Example usage
url = "http://localhost:3000/fragments"
try:
    filenames = get_file_names(url + "/list")

    # create a dataframe from the filenames
    df = pd.DataFrame(filenames, columns=["filename"])

    # import the arrow table into pandas
    print(df)
except Exception as e:
    print(f"Error: {e}")