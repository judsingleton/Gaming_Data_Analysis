#Import libraries

import os
import pandas as pd
import sqlite3

#Read each csv and create a corresponding pandas dataframe
print(os.getcwd())

sales_data = pd.read_csv("Video_Game_Sales_1978-2024.csv")
top_50_data = pd.read_csv("2024_Top_50_AAA_AA_Indie_Games.csv")
gaming_study_data = pd.read_csv("GamingStudy_data.csv", encoding='windows-1254')
online_behavior_data = pd.read_csv("online_gaming_behavior_dataset.csv")

#Align column names and rename columns for clarity

top_50_data.rename(columns={"ReleaseDate": "Year"}, inplace=True)
gaming_study_data.rename(columns={"Game": "Name", "Hours": "HoursPerWeek", "Residence_ISO3": "Location", "GAD_T": "GAD_Total", "SWL_T": "SWL_Total", "SPIN_T": "SPIN_Total"}, inplace=True)
online_behavior_data.rename(columns={"GameGenre": "Genre", "PlayTimeHours": "HoursPerWeek"}, inplace=True)

#Drop unnecessary columns from dataframe

sales_data = sales_data.drop(['Publisher', 'Developer', 'Critic_Score'], axis=1)
top_50_data = top_50_data.drop(['Publishers', 'Developers', 'Steam Id'], axis=1)
gaming_study_data = gaming_study_data.drop(['S. No.', 'Timestamp', 'GADE', 'earnings', 'whyplay', 'League', 'highestleague', 'streams', 'Birthplace', 'Residence', 'Reference', 'accept', 'Birthplace_ISO3'], axis=1)
online_behavior_data = online_behavior_data.drop('PlayerID', axis=1)

#Remove all game series from sales data as well as cross-platform entries as these have no sales

sales_data = sales_data.drop(sales_data[(sales_data['Platform'] == ('Series')) |(sales_data['Platform'] == ('All'))].index)


#Remove rows with NA for SPIN
gaming_study_data = gaming_study_data.dropna(subset='SPIN_Total')

#Create list from Name column of top_50_data to use for column name for new dataframe created from Tags column
top_50_names = top_50_data['Name'].tolist()
top_50_tags = top_50_data[['Tags']]
top_50_tags.index = top_50_names
top_50_tags['Singleplayer'] = False
top_50_tags['Multiplayer'] = False

#Find Singleplayer and Multiplayer tags and set value of corresponding column to True if found

#def list_extract():

for name in top_50_names:
    taglist = top_50_tags.loc[name, 'Tags']
    if "Singleplayer" in taglist:
        top_50_tags.loc[name, 'Singleplayer'] = True
    else:
        top_50_tags.loc[name, 'Singleplayer'] = False    
    if "Multiplayer" in taglist:
        top_50_tags.loc[name, 'Multiplayer'] = True
    else:
        top_50_tags.loc[name, 'Multiplayer'] = False





#print(top_50_tags.iloc[:,:5].head())

#Open the SQL connection and create a cursor

conn = sqlite3.connect(':memory:') 
cursor = conn.cursor()

def sql(query):
    """Input a SQL query and return a pandas dataframe object."""
    return pd.read_sql_query(query, conn)

#Load our data into SQL tables

sales_data.to_sql('Sales', conn, if_exists='replace', index=False)
top_50_data.to_sql('Top_50', conn, if_exists='replace', index=False)
gaming_study_data.to_sql('Gaming_Study', conn, if_exists='replace', index=False)
online_behavior_data.to_sql('Online_Behavior', conn, if_exists='replace', index=False)



conn.close()
