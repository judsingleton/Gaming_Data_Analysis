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
top_50_data = top_50_data.drop(top_50_data.columns[0], axis=1)
gaming_study_data = gaming_study_data.drop(['S. No.', 'Timestamp', 'GADE', 'earnings', 'whyplay', 'League', 'highestleague', 'streams', 'Birthplace', 'Residence', 'Reference', 'accept', 'Birthplace_ISO3'], axis=1)
online_behavior_data = online_behavior_data.drop('PlayerID', axis=1)

#Convert any necessary columns to correct data type
sales_data['Name'] = sales_data['Name'].astype(str)


#Remove all game series from sales data as well as cross-platform entries as these have no sales figures and/or are also broken out by entry and platform

sales_data = sales_data.drop(sales_data[(sales_data['Platform'] == ('Series'))].index)
sales_data = sales_data.dropna(subset="Global_Sales")


#For games with multiple entries that have sales data, add the sum of Global_Sales to the title (not series) from all platforms for the title

sales_data['Multiplatform'] = sales_data.duplicated(subset='Name', keep=False)
multi_series = sales_data['Name'].value_counts()
multi_list = multi_series[multi_series > 1].index.to_list()

#If there is a title with multiple rows but no row where the Platform value is All, create a new row for the title.
#Genre and Year values will be based taken from the earliest release year.

mask = sales_data['Name'].isin(multi_list)
placeholder = sales_data[mask] #dataframe with only titles with more than one entry
#might need to drop some or all NaN or zero entries for Global Sales

for name in multi_list:
    sub_mask = placeholder['Name'] == name
    sub_placeholder = placeholder[sub_mask] #dataframe with all rows for a single title
    for row in range(len(sub_placeholder.index)):
        if 'All' in sub_placeholder['Platform'].unique():
            break
        else:
         #dataframe with only one row to be appended to sales_data
            temp_df = sub_placeholder.loc[sub_placeholder['Year'] == sub_placeholder['Year'].min()].reset_index(drop=False)
            temp_df[0, 3] = 'All'
            temp_df[0, 10] = sub_placeholder['Global_Sales'].sum()
            pd.concat([sales_data, temp_df])
            


def sales_total(title: str):
    """Calculates total sales across all platforms for titles in the sales_data dataframe with multiple rows.  
    Only rows with values in the Global_Sales column are included in the calculation."""
    title_data = sales_data.loc[sales_data['Name'] == title].reset_index()
    return title_data["Global_Sales"].sum()

print(sales_total("Tetris"))

def calc_sales(m_list):
    """Pass in the sales dataframe and calculate total sales for each title with a Platform value of 'All'."""
    s_data = sales_data.reset_index(drop=True)
    print(s_data.head())
    gstotal = 0.0
    for i in range(len(m_list)):
        gstotal = sales_total(m_list[i])
        sales_data.iloc[i, 10] = gstotal
    print("Total global sales figures have been calculated.")

calc_sales(multi_list)


        

#Now that we have the totals
#sales_data = sales_data.drop(sales_data[(sales_data['Platform'] == ('Series')) |(sales_data['Platform'] == ('All'))].index)

#Remove rows with NA for SPIN
gaming_study_data = gaming_study_data.dropna(subset='SPIN_Total')

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





#print(top_50_data.iloc[:,:5].head())

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



test = sql("""
    SELECT Price, Singleplayer, Multiplayer
    FROM Top_50
    INNER JOIN Gaming_Study ON Gaming_Study.Name = Top_50.Name;
    """)

test.to_csv("test.csv", index=False)

print(sales_data.head())

conn.close()
