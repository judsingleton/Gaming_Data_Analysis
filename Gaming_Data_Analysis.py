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

sales_data = sales_data.drop(['Publisher', 'Developer', 'Critic_Score', 'All_Platforms', 'User_Score', 'All_Games', 'NA_Sales', 'PAL_Sales', 'JP_Sales', 'Other_Sales'], axis=1)
top_50_data = top_50_data.drop(['Publishers', 'Developers', 'Steam Id'], axis=1)
top_50_data = top_50_data.drop(top_50_data.columns[0], axis=1)
gaming_study_data = gaming_study_data.drop(['S. No.', 'Timestamp', 'GADE', 'earnings', 'whyplay', 'League', 'highestleague', 'streams', 'Birthplace', 'Residence', 'Reference', 'accept', 'Birthplace_ISO3'], axis=1)
online_behavior_data = online_behavior_data.drop('PlayerID', axis=1)

#Convert any necessary columns to correct data type
print(sales_data.info())
sales_data['Name'] = sales_data['Name', 'Platform', 'Genre'].astype(str)


#Remove all game series from sales data as well as cross-platform entries as these have no sales figures and/or are also broken out by entry and platform

sales_data = sales_data.drop(sales_data[(sales_data['Platform'] == ('Series'))].index)
sales_data = sales_data.dropna(subset="Global_Sales")

#Utility function to get average value of one specified column based on given value in another column (defaults to Name).

def get_average(temp_df, tlist, cname, kname='Name'):
    for i in range(len(tlist)):
        mask = temp_df[kname] == tlist[i]
        average_val = temp_df[temp_df[kname] == tlist[i]][cname].mean()
        temp_df.loc[temp_df[kname] == tlist[i], [cname+'_avg']]= average_val

#For games with multiple entries that have sales data, add the sum of Global_Sales to the title (not series) from all platforms for the title

sales_data['Multiplatform'] = sales_data.duplicated(subset='Name', keep=False)


def duplist(temp_df):
    """Provides a list of values in the Name field  of the sales_data that appear more than once.  Only exact matches are returned."""
    multi_series = sales_data['Name'].value_counts()
    multi_list = multi_series[multi_series > 1].index.to_list()
    multi_list = list(set(multi_list))
    return multi_list

#If there is a title with multiple rows but no row where the Platform value is All, create a new row for the title.
#Genre and Year values will be based taken from the earliest release year.

mask = sales_data['Name'].isin(duplist(sales_data))
placeholder = sales_data[mask] #dataframe with only titles with more than one entry
#might need to drop some or all NaN or zero entries for Global Sales

placeholder = placeholder[placeholder['Global_Sales'] != 0.0]
plist = placeholder['Name'].to_list()

title_list = [] #A list of dataframes, with each list element being for one game title

for i in range(len(plist)):
    temp_df = placeholder[placeholder['Name'] == plist[i]]
    title_list.append(temp_df)

def title_gs_calc(title_df):
    """Takes a dataframe with multiple rows for a title and returns a datframe with a single row with the Global_Sales calculated."""
    return_df = title_df.head(1).reset_index()
    return_df['Platform'] = 'All'
    return_df['Global_Sales'] = title_df['Global_Sales'].sum()    
    return return_df

def title_add(tlist):
    """Takes a list of dataframe consisting of the same title and returns a dataframe that with All for the Platform value and the sum of the columns for Global_Sales."""
    added_titles = pd.DataFrame()
    for i in range(len(tlist)):
        temp_df = title_gs_calc(tlist[i])
        added_titles = pd.concat([added_titles, temp_df], ignore_index=True)
        added_titles = added_titles.drop_duplicates()
    return added_titles

sales_data = pd.concat([sales_data, title_add(title_list)], ignore_index=True)
sales_data = sales_data.reset_index(drop=True)

remove_title_list = duplist(sales_data)
rows_to_remove = sales_data[sales_data['Name'].isin(remove_title_list)].index.to_list()
rows_to_save = sales_data[sales_data['Platform'] == 'All']

sales_data = sales_data.drop(rows_to_remove)
sales_data = pd.concat([sales_data, rows_to_save], ignore_index=True)
sales_data = sales_data.drop_duplicates()

#Create list from Name column of top_50_data to use for column name for new dataframe created from Tags column
top_50_names = top_50_data['Name'].tolist()
top_50_data.index = top_50_names
top_50_data['Singleplayer'] = False
top_50_data['Multiplayer'] = False

#Utility function to check whether an element exists in a list of strings.

def list_check(selement: str, lelement: list[str]):
    """For a dataframe column consisting of lists of strings, return True if the tag exists in the list and False if it does not."""
    return selement in lelement

#Find Singleplayer and Multiplayer tags and set value of corresponding column to True if found

for name in top_50_names:
    taglist = top_50_data.loc[name, 'Tags']
    if list_check('Singleplayer', taglist):
        top_50_data.loc[name, 'Singleplayer'] = True
    else:
        top_50_data.loc[name, 'Singleplayer'] = False    
    if list_check('Multiplayer', taglist):
        top_50_data.loc[name, 'Multiplayer'] = True
    else:
        top_50_data.loc[name, 'Multiplayer'] = False


#Remove rows with NA for SPIN
gaming_study_data = gaming_study_data.dropna(subset='SPIN_Total')

print(gaming_study_data.head())

gmask = gaming_study_data['Name'].unique().tolist()

get_average(gaming_study_data, gmask, 'GAD_Total')
get_average(gaming_study_data, gmask, 'SWL_Total')
get_average(gaming_study_data, gmask, 'SPIN_Total')
get_average(gaming_study_data, gmask, 'HoursPerWeek')

print(gaming_study_data.head()) #REMOVE ME
print(gaming_study_data.info()) #REMVOE ME

gaming_study_avg = gaming_study_data.filter(['Name', 'HoursPerWeek_avg', 'GAD_Total_avg', 'SWL_Total_avg', 'SPIN_Total_avg'], axis=1)
gaming_study_avg = gaming_study_avg.drop_duplicates()
gaming_study_avg.to_csv("gaming_study_avg.csv")

print(gaming_study_avg.head()) #REMOVE ME



#Open the SQL connection and create a cursor

conn = sqlite3.connect(':memory:') 
cursor = conn.cursor()

def sql(query):
    """Input a SQL query and return a pandas dataframe object."""
    return pd.read_sql_query(query, conn)

#Load our data into SQL tables

sales_data.to_sql('Sales', conn, if_exists='replace', index=False)
gaming_study_avg.to_sql('Gaming_Study_Avg', conn, if_exists='replace', index=False)

sales_and_study = sql("""
    SELECT *
    FROM Gaming_Study_Avg
    LEFT JOIN Sales ON Sales.Name = Gaming_Study_Avg.Name;
    """)

sales_and_study.to_csv('sales_and_study.csv') 

conn.close()
