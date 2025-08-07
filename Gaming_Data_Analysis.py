#Import libraries

import os
import pandas as pd
import sqlite3

sales_data = pd.read_csv("Video_Game_Sales_1978-2024.csv")
top_50_data = pd.read_csv("2024_Top_50_AAA_AA_Indie_Games.csv")
gaming_study_data = pd.read_csv("GamingStudy_data.csv", encoding='windows-1254')
online_behavior_data = pd.read_csv("online_gaming_behavior_dataset.csv")
genres = pd.read_csv('genres.csv')

#Add normalization of genre data to top_50_data
top_50_data = pd.merge(top_50_data, genres[['Name', 'Genre']], on='Name', how='left')

#Align column names and rename columns for clarity.

top_50_data.rename(columns={"ReleaseDate": "Year"}, inplace=True)
gaming_study_data.rename(columns={"Game": "Name", "Hours": "HoursPerWeek", "Residence_ISO3": "Location", "GAD_T": "GAD_Total", "SWL_T": "SWL_Total", "SPIN_T": "SPIN_Total"}, inplace=True)
online_behavior_data.rename(columns={"GameGenre": "Genre", "PlayTimeHours": "Hours per Week", "GameDifficulty": "Game Difficulty", "EngagementLevel": "Engagement Level", "InGamePurchases": "In Game Purchases", "SessionsPerWeek": "Sessions per Week", "AvgSessionDurationMinutes": "Average Session Duration"}, inplace=True)

#Drop unnecessary columns from dataframe.

sales_data = sales_data.drop(['Rank', 'Publisher', 'Developer', 'Critic_Score', 'All_Platforms', 'User_Score', 'All_Games', 'NA_Sales', 'PAL_Sales', 'JP_Sales', 'Other_Sales'], axis=1)
top_50_data = top_50_data.drop(['Publishers', 'Developers', 'Steam Id', 'Price', 'Review Count', 'Review Score', 'Steam Followers'], axis=1)
top_50_data = top_50_data.drop(top_50_data.columns[0], axis=1)
gaming_study_data = gaming_study_data.drop(['S. No.', 'Timestamp', 'GADE', 'earnings', 'whyplay', 'Degree', 'Playstyle', 'Work', 'League', 'highestleague', 'streams', 'Birthplace', 'Residence', 'Reference', 'accept', 'Birthplace_ISO3'], axis=1)
online_behavior_data = online_behavior_data.drop(['PlayerID', 'PlayerLevel', 'AchievementsUnlocked'], axis=1)

#Remove rows with NA for NAME
top_50_data = top_50_data.dropna(subset='Name')
sales_data = sales_data.dropna(subset='Name')
gaming_study_data = gaming_study_data.dropna(subset='Name')

#Convert any necessary columns to correct data type
sales_data['Name'] = sales_data['Name'].astype("string")
sales_data['Platform'] = sales_data['Platform'].astype("string")
sales_data['Genre'] = sales_data['Genre'].astype("string")

top_50_data['Name'] = top_50_data['Name'].astype("string")
top_50_data['Genre'] = top_50_data['Genre'].astype("string")
top_50_data['PublisherClass'] = top_50_data['PublisherClass'].astype("string")
top_50_data['Copies Sold'] = top_50_data['Copies Sold'].str.replace(',', '')
top_50_data['Copies Sold'] = top_50_data['Copies Sold'].astype('float64')
top_50_data['Copies Sold'] = top_50_data['Copies Sold'].astype(int)
top_50_data['Gross Revenue'] = top_50_data['Gross Revenue'].str.replace(',', '')
top_50_data['Gross Revenue'] = top_50_data['Gross Revenue'].str.replace('$', '')
top_50_data['Gross Revenue'] = top_50_data['Gross Revenue'].astype('float64')

gaming_study_data['Name'] = gaming_study_data['Name'].astype("string")
gaming_study_data['Gender'] = gaming_study_data['Gender'].astype("string")
gaming_study_data['Platform'] = gaming_study_data['Platform'].astype("string")
gaming_study_data['Location'] = gaming_study_data['Location'].astype("string")

online_behavior_data['Gender'] = online_behavior_data['Gender'].astype("string")
online_behavior_data['Location'] = online_behavior_data['Location'].astype("string")
online_behavior_data['Genre'] = online_behavior_data['Genre'].astype("string")
online_behavior_data['Game Difficulty'] = online_behavior_data['Game Difficulty'].astype("string")
online_behavior_data['Engagement Level'] = online_behavior_data['Engagement Level'].astype("string")

#Remove rows with NA for SPIN
gaming_study_data = gaming_study_data.dropna(subset='SPIN_Total')

#Clean up the Platform data - only PC and console are differentiated so no need for the special characters. Similarly Smartphone / Tablet can be consolidated as Mobile.
gaming_study_data['Platform'] = gaming_study_data['Platform'].replace('Console (PS, Xbox, ...)', 'Console')
gaming_study_data['Platform'] = gaming_study_data['Platform'].replace('Smartphone / Tablet', 'Mobile')

#The names of the games on the gaming study data should match those on the sales data sheet as well.

gaming_study_data['Name'] = gaming_study_data['Name'].replace('Skyrim', 'The Elder Scrolls V: Skyrim')
gaming_study_data['Name'] = gaming_study_data['Name'].replace('Counter Strike', 'Counter-Strike')
gaming_study_data['Name'] = gaming_study_data['Name'].replace('Diablo 3', 'Diablo III')

#Clean up the Platform data - only PC and console are differentiated so no need for the special characters. Similarly Smartphone / Tablet can be consolidated as Mobile.
gaming_study_data['Platform'] = gaming_study_data['Platform'].replace('Console (PS, Xbox, ...)', 'Console')
gaming_study_data['Platform'] = gaming_study_data['Platform'].replace('Smartphone / Tablet', 'Mobile')

#The names of the games on the gaming study data should match those on the sales data sheet as well.

gaming_study_data['Name'] = gaming_study_data['Name'].replace('Skyrim', 'The Elder Scrolls V: Skyrim')
gaming_study_data['Name'] = gaming_study_data['Name'].replace('Counter Strike', 'Counter-Strike')
gaming_study_data['Name'] = gaming_study_data['Name'].replace('Diablo 3', 'Diablo III')

#Remove all game series from sales data as well as cross-platform entries as these have no sales

sales_data = sales_data.drop(sales_data[(sales_data['Platform'] == ('Series'))].index)
sales_data = sales_data.dropna(subset="Global_Sales")

#Update PokÃ©mon to Pokemon in the sales data. As there are various versions of 'Starcraft II' on the sales data sheet this is updated to 'Starcraft' to match the gaming study data.

sales_data['Name'] = sales_data['Name'].str.replace('PokÃ©mon', 'Pokemon')
sales_data.loc[sales_data['Name'].str.contains('StarCraft II'), 'Name'] = 'Starcraft 2'

online_behavior_data['Genre'] = online_behavior_data['Genre'].replace('RPG', 'Role-Playing')

#Utility function to get average value of one specified column based on given value in another column (defaults to Name).

def get_average(temp_df, tlist: list[str], cname: str, kname: str='Name'):
    """Calculates average value of specified column based on given value in another column (defaults to Name).
    Inputs:  Pandas dataframe, list of unique values for key column, name of column to calculate, optional key column specification.
    Outputs:  No return value; appends "cname_avg" column to temp_df."""
    for i in range(len(tlist)):
        mask = temp_df[kname] == tlist[i]
        average_val = temp_df[temp_df[kname] == tlist[i]][cname].mean()
        temp_df.loc[temp_df[kname] == tlist[i], [cname+'_avg']]= average_val

def duplist(temp_df):
    """Provides a list of values in the Name field  of the sales_data that appear more than once.  Only exact matches are returned.
    For example, 'Tetris', 'Tetris DS', and 'Tetris Plus' are all considered unique values."""
    multi_series = temp_df['Name'].value_counts()
    multi_list = multi_series[multi_series > 1].index.to_list()
    multi_list = list(set(multi_list))
    return multi_list

#If there is a title with multiple rows but no row where the Platform value is All, create a new row for the title.
#Genre and Year values will be based taken from the earliest release year.

mask = sales_data['Name'].isin(duplist(sales_data))
placeholder = sales_data[mask] #dataframe with only titles with more than one entry
placeholder = placeholder[placeholder['Global_Sales'] != 0.0]
plist = placeholder['Name'].to_list()

title_list = [] #A list of dataframes, with each list element being for one game title

for i in range(len(plist)):
    temp_df = placeholder[placeholder['Name'] == plist[i]]
    title_list.append(temp_df)

def title_gs_calc(title_df):
    """Takes a dataframe with multiple rows for a title and returns a dataframe with a single row with the Global_Sales calculated."""
    return_df = title_df.head(1).reset_index()
    return_df['Platform'] = 'All'
    return_df['Global_Sales'] = title_df['Global_Sales'].sum()    
    return return_df

def title_add(tlist):
    """Takes a list of dataframes consisting of the same title and returns a dataframe with All for the Platform value and the sum of the columns for Global_Sales."""
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
sales_data = sales_data.drop(columns=sales_data.columns[5], axis=1)

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

#Now that we have the Singleplayer and Multiplayer tags extracted we can drop the Tags column
top_50_data = top_50_data.drop(columns='Tags')

#Get column averages for specified and append to new columns at end

gmask = gaming_study_data['Name'].unique().tolist()

get_average(gaming_study_data, gmask, 'GAD_Total')
get_average(gaming_study_data, gmask, 'SWL_Total')
get_average(gaming_study_data, gmask, 'SPIN_Total')
get_average(gaming_study_data, gmask, 'HoursPerWeek')

#Create new dataframe with one entry per game.  The individual item averages for each screening test are not included in the dataframe
# as it is intended to be a high-level overview.

gaming_study_avg = gaming_study_data.filter(['Name', 'HoursPerWeek_avg', 'GAD_Total_avg', 'SWL_Total_avg', 'SPIN_Total_avg'], axis=1)
gaming_study_avg = gaming_study_avg.drop_duplicates()

#Open the SQL connection and create a cursor

conn = sqlite3.connect(':memory:') 
cursor = conn.cursor()

def sql(query):
    """Input a SQL query and return a pandas dataframe object."""
    return pd.read_sql_query(query, conn)

#Load our data into SQL tables

sales_data.to_sql('Sales', conn, if_exists='replace', index=False)
gaming_study_avg.to_sql('Gaming_Study_Avg', conn, if_exists='replace', index=False)

conn.execute("""
    CREATE TABLE SalesT
    (
    Name TEXT PRIMARY KEY,
    Platform TEXT,
    Global_Sales REAL,
    Genre TEXT,
    Year INTEGER);
    """)
    
conn.execute("""
    INSERT OR REPLACE INTO SalesT (Name, Platform, Global_Sales, Genre, Year)
    SELECT Name, Platform, Global_Sales, Genre, Year FROM Sales;
    """)

conn.execute("""
    CREATE TABLE GST
    (
    Name TEXT PRIMARY KEY,
    HoursPerWeek_avg REAL,
    GAD_Total_avg REAL,
    SWL_Total_avg REAL,
    SPIN_Total_avg REAL);
    """)

conn.execute("""
    INSERT OR REPLACE INTO GST (Name, HoursPerWeek_avg, GAD_Total_avg, SWL_Total_avg, SPIN_Total_avg)
    SELECT Name, HoursPerWeek_avg, GAD_Total_avg, SWL_Total_avg, SPIN_Total_avg FROM Gaming_Study_Avg;
    """)

sales_and_study = sql("""
    SELECT *
    FROM GST
    LEFT JOIN SalesT ON SalesT.Name = GST.Name;
    """)
sales_and_study = sales_and_study.loc[:,~sales_and_study.columns.duplicated()]

conn.close()

sales_and_study.iat[1,5] = 'All'
sales_and_study.iat[3,5] = 'PC'
sales_and_study.iat[9,5] = 'All'

sales_and_study.iat[3,7] = 'Strategy'
sales_and_study.iat[9,7] = 'Strategy'

sales_and_study.iat[3,8] = 2009
sales_and_study.iat[9,8] = 2014

#Missed updating these column names earlier.

sales_data.rename(columns={"Global_Sales": "Global Sales"}, inplace=True)
top_50_data.rename(columns={"Gross Revenue": "Global Sales"}, inplace=True)

#Export our updated and new dataframes to CSV to be loaded into Tableau!

sales_data.to_csv('Final_Data/Sales.csv', index=False)
top_50_data.to_csv('Final_Data/Top_50.csv', index=False)
gaming_study_data.to_csv('Final_Data/Gaming_Study.csv', index=False)
online_behavior_data.to_csv('Final_Data/Behavior.csv', index=False)
sales_and_study.to_csv('Final_Data/Sales_and_Study.csv', index=False)