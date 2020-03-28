from bs4 import BeautifulSoup
import os
import sys
import requests
import shutil
# Created by Abrahan Nevarez
# Starts the setup
def setup(link):
    web_page = requests.get(link)
    soup_obj = BeautifulSoup(web_page.content, "html.parser")
    remove_stuff(link, soup_obj)
# Lets us parse out specific parts
def assign_values(content, name):
    kid_distribution_dump = content[14:74]
    senior_distribution_dump = content[108:129]
    senior_home_dump = content[133:141]
    dump_parts(kid_distribution_dump, name, "kid-distribution-dump")
    dump_parts(senior_distribution_dump, name, "senior-distribution-dump")
    dump_parts(senior_home_dump, name, "senior-home-dump")

# Removes text we may not want
def remove_stuff(link, soup_obj):
    text_file_name = link.replace("https://www.nycfoodpolicy.org/coronavirus-nyc-food-resource-guide-", "")
    text_file_name = text_file_name.replace("/", "")
    if not os.path.isdir(text_file_name):
        try:
            os.mkdir("../dataset/" + text_file_name)
        except:
            print("Error, folder exists!")

    span = [item.get_text() for item in soup_obj.select("span")]
    span = [sub.replace("\xa0", "") for sub in span]
    span = [sub.replace(":", "") for sub in span]
    span = [sub.replace("Requires A Case Manager To Coordinate Services", "") for sub in span]
    assign_values(span, text_file_name)
    finish(span, text_file_name)
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