
import streamlit as st
import pandas as pd
import json
import requests
from pathlib import Path
from io import StringIO
import plotly.express as px
import ssl
import pandas as pd
from urllib.request import urlopen

# Bypass SSL certificate verification
ssl._create_default_https_context = ssl._create_unverified_context


### Access the data set and read the file
### Displays the first 5 rows of the DataFrame.

url = 'https://raw.githubusercontent.com/almazafa/DataScience/main/Data%20Science%20Jobs%20Salaries.csv'
df = pd.read_csv(url)
print(df.head())

### I wanted to show other way how i can accesss the url and displays it as DataFrame using requests library

# URL of the CSV file on GitHub
url = 'https://raw.githubusercontent.com/almazafa/DataScience/main/Data%20Science%20Jobs%20Salaries.csv'

# Fetch the CSV data using requests
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Load the content of the response into a pandas DataFrame
    csv_data = StringIO(response.text)
    df = pd.read_csv(csv_data)

    # Display the first few rows of the DataFrame
    print(df.head())
else:
    print('Failed to fetch data. Status code:', response.status_code)

    # Provide a summary of statistics for numeric columns
df.describe()

# To use Json i need to convert csv to json
# Convert DataFrame to JSON
json_data = df.to_json(orient='records')

# Writing JSON data to a file
with open('data.json', 'w') as json_file:
    json.dump(json.loads(json_data), json_file, indent=4)

    # Get user inputs:
# experience level you are searching for
experience_level = str(input("Enter experience level( EN / MI/ SE): ")).lower() + '_experience_level'

# employment_type you are searching for
employment_type = str(input("Enter employment_type: FT or PT")).lower().replace(' ', '+')

# job you are searching for
job_title = str(input("Enter keywords: Data Scientist or Data Engineer ")).lower().replace(' ', '+')

# Will display pop up message please insert what you are looking for :

search_query = url + '?&q=' + job_title + '&l=' + employment_type + '&explvl=' + experience_level
response_search = requests.get(search_query)

df_searched = pd.read_csv(StringIO(response_search.text))

print(f'Your search is ready: {df_searched}')

# Streamlit app
# name of the app - title

st.title('Data Science Job Visualiztion')

# display the data set

st.write("Loaded Data:")
st.write(df)

# Use Plotly charts based on the data set
# salary chart using histogram


fig_salary_dist = px.histogram(df, x='salary', title='Salary Distribution')
st.plotly_chart(fig_salary_dist)

# experience_level job distribution using pie chart

fig_experience_dist = px.pie(df, names='experience_level', title='experience level job distribution')
st.plotly_chart(fig_experience_dist)

# job title frequencies using bar chart

fig_job_dist = px.bar(df['job_title'].value_counts(), x=df['job_title'].value_counts().index,
                      y=df['job_title'].value_counts().values, labels={'x': 'Job job_title', 'y': 'Frequency'},
                      title='Job Title Frequencies')
st.plotly_chart(fig_job_dist)

## write this in the terminal :
# streamlit run /home/codespace/.local/lib/pyhton3.10/site-packages/ipykernel_launcher.py



