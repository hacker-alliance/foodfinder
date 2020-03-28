import pandas as pd 
import shutil
def text_strip(text, original_word, new_word):
    text = ''.join([i for i in text]) \
    .replace(original_word, new_word)

pdf_link = "dataset\EFAP_ACTIVE.csv"
pdf_link_name = "EFAP_ACTIVE_CLEAN"
text = open(pdf_link, "r")

text = ''.join([i for i in text]) \
        .replace("BX", "Bronx")
#text_strip(text, "BX", "Bronx")
text = ''.join([i for i in text]) \
        .replace("BK", "Brooklyn")
text = ''.join([i for i in text]) \
        .replace("QN", "Queens")
text = ''.join([i for i in text]) \
        .replace("NY", "New York")
text = ''.join([i for i in text]) \
        .replace("SI", "Staten Island")
x = open(pdf_link_name +".csv","w")

x.writelines(text)
x.close()
shutil.move(pdf_link_name + ".csv", "dataset/" + pdf_link_name + ".csv")

    