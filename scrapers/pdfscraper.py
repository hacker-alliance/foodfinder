import sys
from tabula import read_pdf, convert_into
import tabula as tabula
import pandas as pd
import shutil

def pdf_scrape(link):
    link_name = link.replace("https://www1.nyc.gov/assets/hra/downloads/pdf/services/efap/", "")
    link_name_without_pdf = link_name.replace(".pdf", "")
    data = tabula.convert_into(link, link_name_without_pdf + ".csv", output_format="csv", pages='all')
    shutil.move(link_name_without_pdf + ".csv", "../dataset/")
    

if __name__ == "__main__":
    link = sys.argv[1]
    pdf_scrape(link)