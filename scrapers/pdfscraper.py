import sys
from tabula import read_pdf, convert_into
import tabula as tabula
import pandas as pd
import shutil
# Lets us change the district column data
def changeData(df, original_word, new_word):
    df["DIS"] = df["DIS"].str.replace(original_word, new_word)
# Fixes up the excel file
def fix(pdf_file):
    pdf_file_clean = pdf_file.replace(".csv", "")
    df = pd.read_csv(pdf_file, sep=",")

    df.drop_duplicates(subset=None, inplace=True)
    df["ORG PHONE"] = df["ORG PHONE"].str.replace(r'\D+', '')

    # Replaces the district with the respective names
    changeData(df, "BX", "The Bronx")
    changeData(df, "BK", "Brooklyn")
    changeData(df, "QN", "Queens")
    changeData(df, "NY", "New York")
    changeData(df, "SI", "Staten Island")
    changeData(df, "NTY", "New York")
    # Write the results to a different file
    df.to_csv(pdf_file)
    

    

def pdf_scrape(link):
    link_name = link.replace("https://www1.nyc.gov/assets/hra/downloads/pdf/services/efap/", "")
    link_name_without_pdf = link_name.replace(".pdf", "")
    data = tabula.convert_into(link, link_name_without_pdf + ".csv", output_format="csv", pages='all')
    fix(link_name_without_pdf + ".csv")
    shutil.move(link_name_without_pdf + ".csv", "../dataset/")
    

if __name__ == "__main__":
    link = sys.argv[1]
    pdf_scrape(link)