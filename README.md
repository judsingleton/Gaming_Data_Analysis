# Gaming_Data_Analysis
Analysis of consumer trends in video game data

The main question this analysis aims to answer is what correlation if any exists between a video game's sales and any negative impact on the mental or social well-being of its players.  Video games are an increasingly profitable sector of the entertainment industry, eclipsing both the music and movie industries.  However, concerns about their possible impact upon the psychosocial health of its players have been raised from multiple corners.  In this analysis several data sets will be examined, with visualizations provided on a Tableau dashboard.

## Project Objective 

The objective of this project is to see what correlations can be found between a video game's sales and several other factors.  These include several mental health screening evaluations as well as the genre.  Questions to answer include whether game genre shows any noticeable correlation to mental health scores, genre profitability, and any possible correlation between the gamer's mental and social health and overall game profits.

## Project Setup Instructions

As the data visualizations will be created in Tableau, the library requirements for this project are minimal.  They are included in the 'requirements.txt' file.

### Steps to run:

Python 3.13 and Jupyter notebooks will need to be installed on your machine.

1. Clone the repository either from the terminal or by downloading the zip file.
2. In the terminal, navigate to the folder containing the cloned repository and run the following code:
    pip install -r requirements.txt
3. Open the project in Jupyter Notebook from the command line or terminal.
4. If you are not in the correct location navigate to the directory containing the repository.
5. Open Gaming_Data_Analysis.ipynb.
6. Click Run All.

### To run in a virtual environment:

From the terminal, enter the following commands.

Gitbash:  

python -m venv env
source Scripts/activate

Windows:  

python -m venv env
Scripts\activate.bat

Mac:  

python -m venv env
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

For sales, a dataset with sales figures (with just shy of 64 thousand rows) for video games released between 1978 and 2024 is examined, as well as a dataset consisting of the top 50 games in each publisher category of AAA, AA, and independent or 'indie'.  A dataset of approximately 40 thousands rows consisting of data from users consisting of time spent playing games as well as engagement level is examined.  Finally, an in-depth study of ten representative video games consisting of over 13 thousand rows and their players' score on various mental health screening tools will be explored.  

I found that while there does appear to be some slight correlation between genre and mental health scores, there does not appear to be one between genre and revenue.  As such, this would seem to imply a weak correlation if any between game revenue and the mental health scores of the players.

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
 | Singleplayer | Whether the game has a single player mode. Calculated for top 50 dataset from Tags column.| bool |
 | Multiplayer | Whether the game has a multi player mode. Calculated for top 50 dataset from Tags column.| bool |
  | Tags | This column consists of lists of strings that describe each title.| Pandas series |


### Notes on data normalization:

Due to Other not being a single video game, and League of Legends and Hearthstone not appearing on the sales data due to being free to download, we must manually assign Platform and Genre.

Similary, for the top 50 dataset, Genre is not a pre-populated column.  Instead, a Tags column consisting of lists of strings is included, in which multiple genres could be present.  As genre is a somewhat subjective category, these titles had to be manually assigned genres based on the contents in their Tags summaries from Steam as well as Wikipedia.  These are included in the separate Genres.csv file.

## Project Summary

All visualizations can be accessed from the Tableau dashboard at https://public.tableau.com/app/profile/jud.singleton/viz/GamingDataAnalysisCapstone/GamingDataAnalysisCapstone?publish=yes

Information about the mental health screening data found in the Gaming Study dataset can be found at the links below.  Note that on the first two tests a higher number indicates a negative outcome (higher anxiety or social phobia) while on the SWL a higher score indicates a higher satisfaction with life.  No units are used for any of the tests.

Generalized Anxiety Disorder (GAD-7):  https://www.hiv.uw.edu/page/mental-health-screening/gad-7

Social Phobia Inventory (SPIN):  https://psychology-tools.com/test/spin

Satisfaction With Life Scale:  https://novopsych.com/assessments/well-being/satisfaction-with-life-scale-swls/

There is surprisingly little difference between genre and the amount of time a player devotes towards gaming on average.  This remains the case when separating data out by gender.  This would seem to indicate any correlation between these two factors and player mental health is low.

Role-playing games, which tend to have more emphasis on long-term player progression than other genres, do have higher average scores for the mental health screenings than do strategy games or shooters.  Surprisingly, MMOs which are a distinct sub-genre of role-playing games that tends to heavily emphasize player progression, scored only neglibly higher on the GAD lower on the SWL, but also lower SPIN evaluations.  Shooters scored the lowest in each category.

There does not appear to be a strong correlation at first glance between mental health and the profitability of a video game.  MMOs and shooters have roughly equivalent average global revenue, with strategy and non-MMO role-playing games being noticeably less profitable on average.  

One limitation of this analysis is simply a lack of available metnal health data for more titles.  While the listed titles on the Gaming Study dataset are popular titles and representative of their specific genres, not all genres are represented.  Additionally, the study is skewed towards established titles, with the most recent titles being released in 2014.  The other limitation is that the sales dataset captures revenue based on purchasing the game, but does not appear to include revenue for games that are free to download but include in-game purchases, as neither Hearthstone nor League of Legends require an initial purchase.

For further analysis, age and location data have been left in the datasets but not specifically explored here.  Additionally, if more granular data is desired, the scores for the individual questions on the mental health assessments have been retained on the Gaming Study CSV file in the Final_Data folder.
