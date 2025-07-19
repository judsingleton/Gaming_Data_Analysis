#Import libraries

import pandas as pd
import sqlite3

#Read each csv and create a corresponding pandas dataframe

sales_data = pd.read_csv("Gaming_Data_Analysis/Video_Game_Sales_1978-2024.csv")
top_50_data = pd.read_csv("Gaming_Data_Analysis/2024_Top_50_AAA_AA_Indie_Games.csv")
gaming_study_data = pd.read_csv("Gaming_Data_Analysis/GamingStudy_data.csv", encoding='windows-1254')
online_behavior_data = pd.read_csv("Gaming_Data_Analysis/online_gaming_behavior_dataset.csv")

#Drop unnecessary columns from dataframe

sales_data = sales_data.drop(['Publisher', 'Developer', 'Critic_Score'], axis=1)
top_50_data = top_50_data.drop(['Publishers', 'Developers'], axis=1)
gaming_study_data = gaming_study_data.drop(['S. No.', 'Timestamp', 'GADE', 'earnings', 'whyplay', 'League', 'highestleague', 'streams', 'Birthplace', 'Residence', 'Reference', 'accept', 'Birthplace_ISO3'], axis=1)
online_behavior_data = online_behavior_data.drop('PlayerID', axis=1)

#Remove all game series from sales data as well as cross-platform entries as these have no sales

sales_data = sales_data.drop(sales_data[sales_data['Platform'] == ('Series' or 'All')].index)

#Remove rows with NA for SPIN
gaming_study_data = gaming_study_data.dropna(subset='SPIN_T')

