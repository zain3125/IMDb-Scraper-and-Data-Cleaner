# IMDb Movie Scraper and Data Cleaner

## 📌 Overview
This script performs the following tasks:
1. **Scrapes movie data** from IMDb using `BeautifulSoup` and `requests`.
2. **Cleans and processes the scraped data** by merging it with additional data from an external CSV file.
3. **Removes duplicates and fills missing values**.
4. **Saves the cleaned dataset** as a CSV file.

## 📂 Project Structure
- `final.py` → The main script for scraping and cleaning IMDb data.
- `imdb_movies.csv` → Stores the scraped movie data.
- `big_data.csv` → Additional dataset for merging.
- `cleaned_file.csv` → The final cleaned and processed dataset.

## 🔧 Dependencies
Make sure you have the following Python libraries installed:
```sh
pip install beautifulsoup4 requests pandas numpy
```

## 📡 IMDb Scraper
### **How It Works:**
- The script loops through IMDb movie IDs (`tt0000001` to `tt0005000`) and requests movie pages.
- Extracts details like `Title`, `Year`, `Rating`, `Votes`, `Genre`, `Description`, `Country`, `Director`, and `Writers`.
- Saves the extracted data to `imdb_movies.csv`.

### **Key IMDb Scraping Code:**
```python
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

title_tag = soup.find("span", class_="hero__primary-text")
title = title_tag.text.strip() if title_tag else "N/A"
```

## 🛠 Data Cleaning Process
### **Steps Taken:**
1. **Merge scraped data with `big_data.csv`** based on `IMDb ID`.
2. **Remove unnecessary columns:**
   ```python
   df.drop(columns=["primaryTitle", "originalTitle", "isAdult", "endYear"], inplace=True)
   ```
3. **Remove duplicate entries:**
   ```python
   df.drop_duplicates(subset=["IMDb ID"], keep="first", inplace=True)
   ```
4. **Replace missing values (`\N` to `NULL`)**
   ```python
   df.replace("\\N", "", inplace=True)
   ```
5. **Fill missing `Genre` values from `genres` column**
   ```python
   df["Genre"] = df["genres"]
   df.drop(columns=["genres"], inplace=True)
   ```
6. **Save the cleaned dataset:**
   ```python
   df.to_csv("cleaned_file.csv", index=False, encoding='utf-8')
   ```

## ✅ Final Output
- A cleaned dataset stored in `cleaned_file.csv` ready for further analysis.

## 🚀 How to Run the Script
Simply execute the script:
```sh
python final.py
```
This will scrape IMDb, clean the data, and save it to `cleaned_file.csv`.

---
**🔹 Author:** IMDb Data Engineering Project
**🔹 Last Updated:** March 2025

