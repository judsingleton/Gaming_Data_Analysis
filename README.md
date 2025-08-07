# Gaming_Data_Analysis
Analysis of consumer trends in video game data

The main question this analysis aims to answer is what correlation if any exists between a video game's sales and any negative impact on the mental or social well-being of its players.  Video games are an increasingly profitable sector of the entertainment industry, eclipsing both the music and movie industries.  However, concerns about their possible impact upon the psychosocial health of its players have been raised from multiple corners.  In this analysis several data sets will be examined, with visualizations provided on a Tableau dashboard.

## Project Objective 

The objective of this project is to see what correlations can be found between a video game's sales and several other factors.  As these

## Project Setup Instructions

As the data visualizations will be created in Tableau, the library requirements for this project are minimal.  They are included in the 'requirements.txt' file.

### Steps to run:

1. Clone the repository either from the terminal or by downloading the zip file.
2. In the terminal, navigate to the folder containing the cloned repository and run the following code:
    pip install -r requirements
3. Open the project in Jupyter Notebook from the command line or terminal.
4. If you are not in the correct location navigate to the directory containing the repository.
5. Open Gaming_Data_Analysis.ipynb.
6. Click Run All.

### To run in a virtual environment:

From the terminal, enter the following commands.

Gitbash:  

python3 -m venv env
source Scripts/activate

Windows:  

python -m venv env
Scripts\activate.bat

Mac:  

python3 -m venv env
source env/bin/activate


## Technologies Used

  Pandas was used to clean and otherwise process the datasets.  SQLite3 was used to join two datasets into a new dataset.
  This project was developed in Jupyter Notebooks to allow for clean, narrative-driven presentation of the code and the results.
  Visualizations were created using Tableau Desktop Public.
  
## Data Sources

Video game sales data came from Kaggle by means of Gigasheet.

https://www.gigasheet.com/sample-data/video-game-sales-1978---2024 - Renamed to Video_Game_Sales_1978-2024.csv.
https://www.kaggle.com/datasets/jasonlreed/video-game-sales?resource=download

The online gaming behavior and gaming study datasets came from Kaggle.

https://www.kaggle.com/datasets/rabieelkharoua/predict-online-gaming-behavior-dataset
https://www.reddit.com/r/gamedev/comments/1hy9ljz/i_collected_data_from_the_top_50_aaa_aa_and_indie/ - Renamed to as 024_Top_50_AAA_AA_Indie_Games.csv

The top 50 AAA, AA, and indie games were sourced from Reddit.

https://www.reddit.com/r/gamedev/comments/1hy9ljz/i_collected_data_from_the_top_50_aaa_aa_and_indie/ 
/ https://docs.google.com/spreadsheets/d/1bgNeVZWW4ErxR_XhhO8PjkOi1tSqR-irBfxUyEraPiM/edit?gid=0#gid=0


## Data Summary

For sales, a dataset with sales figures for video games released between 1978 and 2024 is examined, as well as a dataset consisting of the top 50 games in each publisher category of AAA, AA, and independent or 'indie'.  A dataset consisting of data from users consisting of time spent playing games as well as engagement level is examined.  Finally, an in-depth study of ten representative video games and their players' score on various mental health screening tools will be explored.

### Data Dictionary 
 | Column Name | Description | Data Type |
 |-----------|-------------|------------|
 | Name | The name of the individual video game. | string |
 | Genre | The genre of the video game. | string |
 | HoursPerWeek | The estimaed hours per week an individual spends gaming. | int |
 | GAD_T, SPIN_T, SWL_T | The total scores for the three mental health screenings. | int |
 | GAD_#, SPIN_#, SWL_# | These columns contain the score for a given question number on the specified screening test.  While not directly used in the analysis, they are retained for ease of additional further analysis. | int |
 | Platform | The video game platform (PC, console, mobile, etc.) the individual is using for the games. | string |
 | Global_Sales | The global sales in millions of dollars for the title. | float64 |


### Notes on data normalization:

Due to Other not being a single video game, and League of Legends and Hearthstone not appearing on the sales data due to being free to download, we must manually assign Platform and Genre.

Similary, for the top 50 dataset, Genre is not a pre-populated column.  Instead, a Tags column consisting of lists of strings is included, in which multiple genres could be present.  As genre is a somewhat subjective category, these titles had to be manually assigned genres based on the contents in their Tags summaries from Steam as well as Wikipedia.  These are included in the separate Genres.csv file.

## Project Summary

All visualizations can be accessed from the Tableau dashboard at https://public.tableau.com/app/profile/jud.singleton/viz/GamingDataAnalysisCapstone/Dashboard1?publish=yes.


 
