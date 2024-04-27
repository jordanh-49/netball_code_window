import streamlit as st
import pandas as pd
import os
import plotly.express as px

def load_csv_files(directory):
    # Initialize an empty list to store DataFrames
    dataframes = []
    
    # Loop through all files in the specified directory
    for file in os.listdir(directory):
        # Check if the file matches the expected naming pattern
        if file.endswith(".csv"):
            # Construct the full path to the file
            file_path = os.path.join(directory, file)
            
            # Load the CSV file into a DataFrame
            df = pd.read_csv(file_path)
            
            # Optionally, add a column to identify the file if needed
            df['source_file'] = file
            
            # Append the DataFrame to the list
            dataframes.append(df)
    
    # Combine all DataFrames into a single DataFrame
    combined_df = pd.concat(dataframes, ignore_index=True)
    
    return combined_df

def preprocess_data(df):
    # Calculate counts of makes and misses for each combination of home/away, position, and score
    df_count = df.groupby(['Team', 'Position', 'Result']).size().reset_index(name='count')
    return df_count

# Usage example
directory = 'data'
all_data = load_csv_files(directory)


st.dataframe(all_data)

# Set up the Streamlit app
st.title('Shot Outcomes by Team and Position')

data_preprocessed = preprocess_data(all_data)

# Create the bar chart using Plotly
fig = px.bar(data_preprocessed, x='Team', y='count', color='Result', barmode='group',
             facet_col='Position',  # Split by position
             labels={'count':'Number of Shots', 'team_type': 'Team Type', 'position': 'Position', 'score': 'Shot Outcome'},
             title='Number of Makes and Misses by Team and Position')
st.plotly_chart(fig)
