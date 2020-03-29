from bs4 import BeautifulSoup
import os
import sys
import requests
import shutil
import re 
import csv
import itertools
# Created by Abrahan Nevarez
# Starts the setup
def setup(link):
    web_page = requests.get(link)
    soup_obj = BeautifulSoup(web_page.content, "html.parser")
    remove_stuff(link, soup_obj)

def csv_creator(original_file, name_of_file,name_of_business, phone_numbers, addresses):
    headers=['Name', 'Address']
    with open(name_of_file + ".csv", 'w', newline='') as output:
        writer = csv.writer(output)
        writer_obj = csv.writer(output)
        writer_obj.writerow(["Name", "Address", "Phone Number", "Zipcode", "District"])
        for i, j in zip(name_of_business, addresses):
            writer_obj.writerow([i, j])
        output.close()
        shutil.move(name_of_file + ".csv", "../dataset/" + original_file)

# Lets us parse out specific parts
def assign_values(content, name):
    kid_distribution_dump = content[65:74]
    print(content[60])
    senior_distribution_dump = content[108:129]
    senior_home_dump = content[133:141]
    kid_distribution_name_dump = [s for s in kid_distribution_dump if " X" in s]
    kid_distribution_streetaddresses_dump = [s for s in kid_distribution_dump if "10" in s]
    dump_parts(kid_distribution_dump, name, "kid-dump")
    dump_parts(senior_distribution_dump, name, "senior-dump")
    csv_creator(name, "completedump", kid_distribution_name_dump, "777", kid_distribution_streetaddresses_dump)
    
    
# Removes text we may not want
def remove_stuff(link, soup_obj):
    text_file_name = link.replace("https://www.nycfoodpolicy.org/coronavirus-nyc-food-resource-guide-", "")
    text_file_name = text_file_name.replace("/", "")
    if not os.path.isdir(text_file_name):
        try:
            os.mkdir("../dataset/" + text_file_name)
        except:
            print("Error, folder exists!")

    li_tag = [item.get_text() for item in soup_obj.select("li")]
    
    assign_values(li_tag, text_file_name)
    finish(li_tag, text_file_name)
def finish(content, name):
    name_of_file = name + ".txt"
    dump = open(name_of_file, "w")
    print(content, file = dump)
    dump.close()
    shutil.move(name_of_file, "../dataset/" + name)

# Dumps to a txt file
def dump_parts(content, name, specific_name):
    name_of_dump = name + "-" + specific_name + ".txt"
    dump = open(name_of_dump, "w")
    print(content, file = dump)
    dump.close()
    shutil.move(name_of_dump, "../dataset/" + name)
if __name__ == "__main__":
    link = sys.argv[1]
    setup(link)