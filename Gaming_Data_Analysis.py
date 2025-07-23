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

sales_data = sales_data.drop(sales_data[sales_data['Platform'] == ('Series' or 'All')].index)


#Remove rows with NA for SPIN
gaming_study_data = gaming_study_data.dropna(subset='SPIN_Total')

#Create list from Name column of top_50_data to use for column name for new dataframe created from Tags column
top_50_names = top_50_data['Name'].tolist()
top_50_tag_list = top_50_data['Tags'].tolist()
#top_50_tags = pd.DataFrame(top_50_tag_list, columns= top_50_names)

for name in top_50_names:
    top_50_tags[name] = top_50_tag_list


print(top_50_names)

"""
print(sales_data.head())
print(top_50_data.head())
print(gaming_study_data.head())
print(online_behavior_data.head())

print(top_50_tags.iloc[:,:5].head())
"""
