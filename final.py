from bs4 import BeautifulSoup
import csv
import numpy as np
import pandas as pd
import requests
import time


# إعدادات الطلبات
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
base_url = "https://www.imdb.com/title/tt{:07d}/"

# create csv file
with open("E:\python projects\Data Engineering\IMDb/imdb_movies.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["IMDb ID", "Title", "Year", "Rating", "Votes", "Genre", "Description", "Country", "Director", "Writers", "URL"])

    for i in range(1, 5001):
        imdb_id = f"tt{i:07d}"
        url = base_url.format(i)

        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"{imdb_id}: Not found")
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            title_tag = soup.find("span", class_="hero__primary-text")
            title = title_tag.text.strip() if title_tag else "N/A"

            year_tag = soup.select_one('a[href*="releaseinfo"]')
            year = year_tag.text.strip() if year_tag else "N/A"

            rating_tag = soup.find("span", class_="sc-d541859f-1 imUuxf")
            rating = rating_tag.text.strip() if rating_tag else "N/A"

            votes_tag = soup.find("div", class_="sc-d541859f-3 dwhNqC")
            votes = votes_tag.text.strip() if votes_tag else "N/A"

            genre_tag = soup.find("span", class_="ipc-chip__text")
            genre = genre_tag.text.strip() if genre_tag else "N/A"

            description_tag = soup.find("div", class_="ipc-html-content-inner-div")
            description = description_tag.text.strip() if description_tag else "N/A"

            country_tag = soup.select_one('li:has(a[href*="country_of_origin"]) a')
            country = country_tag.text.strip() if country_tag else "N/A"

            director_tag = soup.select_one('li:has(span:contains("Director")) a')
            director = director_tag.text.strip() if director_tag else "N/A"

            writers_tag = soup.select_one('li:has(span:contains("Writer")) a')
            writers = writers_tag.text.strip() if writers_tag else "N/A"


            writer.writerow([imdb_id, title, year, rating, votes, genre, description, country, director, writers, url])

            print(f"{imdb_id} | {title} | ({year}) | {rating} | {votes} | {genre} | {country} | {director} | {writers}")
            print("-"* 80)
            #yah 3aleek da enta bny adam awyyyy
            time.sleep(1)

        except Exception :
            print("Error processing")
            continue

print("success!")


# cleaning data


big = pd.read_csv(r"E:\python projects\Data Engineering\IMDb/big_data.csv", low_memory=False) #import additional data
movies = pd.read_csv(r"E:\python projects\Data Engineering\IMDb/imdb_movies.csv")
# print (movies.info)
# print (big.info)

df = pd.merge(movies, big, left_on='IMDb ID', right_on='tconst', how='inner')
df.drop(columns=["tconst"], inplace = True) 
# print (merged_df)

# remove duplicated columns
df.drop(columns=["primaryTitle", "originalTitle", "isAdult", "endYear"], inplace=True)

# remove duplicated rows
df["is_duplicate"] = np.where(df.duplicated(subset=["IMDb ID"]), "Duplicate", "Unique")
duplicates = df[df["is_duplicate"] == "Duplicate"]
df = df.drop_duplicates(subset=["IMDb ID"], keep="first")
df.drop (columns= (["is_duplicate"]), inplace = True )

# set null vaules
df.replace("\\N", "", inplace=True)


# fill missing genre values
df["Genre"] = df["genres"]
df.drop(columns=["genres"], inplace=True)

df.to_csv("E:/python projects/Data Engineering/IMDb/cleaned_file.csv", index=False, encoding='utf-8')
