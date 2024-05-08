import streamlit as st
import requests
from pathlib import Path 
import pandas as pd

def read_mdfile(filepath:str):
    """Reads a markdown file

    Args:
        file (str): The path to the markdown file to be read
    """
    md_text = Path(filepath).read_text(encoding="utf-8")
    st.markdown(md_text, unsafe_allow_html=True)


def load_html(url:str):
    """Extracts the HTML from the given url

    Args:
        url (str): The URL from which to extract the HTML

    Raises:
        Exception: The case when the URL provided is not valid

    Returns:
        html: The extracted html content
    """
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("찾을 수 없는 페이지입니다.")
    else:
        html = response.text

    return html

def json2csv(jsondict:dict):
    """Converts a dictionary to a DataFrame and saves it as a CSV file

    Args:
        jsondict (dict): The dictionary to be converted to a DataFrame
    """
    table_dict = {}
    data = jsondict['articles']
    for dictionary in data:
        for key, value in dictionary.items():
            if key in table_dict:
                table_dict[key].append(value)
            else:
                table_dict[key] = [value]

    table = pd.DataFrame(table_dict)
    
    return table.to_csv().encode('euc-kr')





