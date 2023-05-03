# ML_Movie_Recommendation
#### Authors: Grant Doan, Prayash Joshi, Reagan Orth, Ved Patel

### Contributions:
- Grant Doan: Webscraping, Sentiment Analysis
- Prayash Joshi: Full-Stack, Cloud Hosting & Database, Dynamic web app
- Reagan Orth: Movie data cleaning, GNN, Recommendation Algorithm
- Ved Patel: Webscraping, Frontend, Poster

### Instructions:
1. ./webscraper (done by Ved and Grant):  
the driver is invoked as python ./driver.py [file with urls]
ex.  python.exe .\driver.py urls_pos_2.txt

The second dataset is located in the ./movie_data directory. Simply run the python script that is in the directory. The result will be 
a 1000 movie dataset with the associated links to the movies. 

2. ./app  (done by Prayash, Reagan's recommendation function):  
Our website can be accessed at https://filmgeniev2-5reqkkiosq-uc.a.run.app/  
Note that the website may take a while to load.

3. Our sentiment analysis notebooks (done by Grant) can be found in a google colab folder here:  
https://drive.google.com/drive/folders/1ppQgTfgZnkrcsiRvUjgFOcodiud7tZT4?usp=share_link

4. Our GNN notebook (done by Reagan) is found in ML notebooks/InitialModel.ipynb.  
Note that the GNN is very large and takes a long time to run(4 epochs took 6 hours on a laptop), which is why we have exported the similarity weights to a CSV file for easier use/access.



### Our Pipeline
1. Scrape the data from IMDb into two data files: a Reviews Dataset and a Movie Information Dataset using the webscraping tools we wrote.
2. Create the similarity matrix using the Movie Information Dataset and our code in ML notebooks/InitialModel.ipynb, export matrix to CSV.
3. Use Reviews Dataset to analyze sentiment of reviews and pull out critical features, such as actor names, genres, and other film titles.
4. Take user input from the website in JSON format, including movie names, ratings, and reviews.
5. Use custom recommendation algorithms with sentiment analysis input to determine which movies to recommend, seen in app/app.py
6. Display the recommended movies on the website, with some film information and clickable movie posters to link to the IMDb pages.
