import sys
from tabula import read_pdf, convert_into
import tabula as tabula
import pandas as pd
import shutil
# Fixes up the excel file
def fix(pdf_file):
    pdf_file_clean = pdf_file.replace(".csv", "")
    df = pd.read_csv(pdf_file, sep=",")

    # Notes:
    # - the `subset=None` means that every column is used 
    #    to determine if two rows are different; to change that specify
    #    the columns as an array
    # - the `inplace=True` means that the data structure is changed and
    #   the duplicate rows are gone  
    df.drop_duplicates(subset=None, inplace=True)
    df["ORG PHONE"] = df["ORG PHONE"].str.replace(r'\D+', '')
    # Write the results to a different file
    df.to_csv(pdf_file)
    text = open(pdf_file, "r")
    text = ''.join([i for i in text]) \
            .replace("BX", "The Bronx")
    #text_strip(text, "BX", "Bronx")
    text = ''.join([i for i in text]) \
            .replace("BK", "Brooklyn")
    text = ''.join([i for i in text]) \
            .replace("QN", "Queens")
    text = ''.join([i for i in text]) \
            .replace("NY", "New York")
    text = ''.join([i for i in text]) \
            .replace("SI", "Staten Island")
    text = ''.join([i for i in text]) \
            .replace("()", "")
    
    x = open(pdf_file,"w")
    x.writelines(text)
    x.close()

    

def pdf_scrape(link):
    link_name = link.replace("https://www1.nyc.gov/assets/hra/downloads/pdf/services/efap/", "")
    link_name_without_pdf = link_name.replace(".pdf", "")
    data = tabula.convert_into(link, link_name_without_pdf + ".csv", output_format="csv", pages='all')
    fix(link_name_without_pdf + ".csv")
    shutil.move(link_name_without_pdf + ".csv", "../dataset/")
    

if __name__ == "__main__":
    link = sys.argv[1]
    pdf_scrape(link)