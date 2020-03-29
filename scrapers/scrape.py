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

        
def csv_creator(original_file, name_of_file,name_of_business, phone_numbers, addresses, zipcode, District):
    #print(addresses)
    with open(name_of_file + ".csv", 'w', newline='') as output:
        writer = csv.writer(output)
        writer_obj = csv.writer(output)
        writer_obj.writerow(["Name", "Phone Number", "Address", "Zipcode", "District"])
        #writer_obj.writerow([name_of_business, addresses, phone_numbers, zipcode, District])
        for i, j, k, l in zip(name_of_business, phone_numbers, addresses, zipcode):
            writer_obj.writerow([i, j, k, l, "The Bronx"])
        output.close()
        shutil.move(name_of_file + ".csv", "../dataset/" + original_file)

# Lets us parse out specific parts
def assign_values(content, name):
    kid_distribution_dump = content[60:160]
    senior_distribution_dump = content[208:230]
    senior_home_dump = content[133:141]

    storage_for_districts = ["Bronx", "Queens", "Staten Island", "New York"]
    storage_for_directions = ["East", "West", "North", "South"]
    storage_for_common_streets = ["Street", "Avenue", "Road", "Bridge", "Park", "River", "Blvd"]
    storage_for_street_names = ["Tremont", "Fordham", "Jerome", "Briggs", "Marion", "Martin Luther King", "Harlem", "Grand Concourse"]
    storage_for_time_settings = ["am", "pm"]
    storage_for_time = ["130", "230", "730"]
    zipcode_of_nyc = ["10453", "10457", "10458", "10468"]
    x_number = ["363120", "447125", "382125", "228400", "0332424", "0852400", "209313", "229275", "386125", "2321700", "0912200", "3031700", "3901930", "2041780", "2261950", "33140", "274275", "2261950", "9294590", "9294590", "30640", "0083010", "0462760", "2462641", "0542703", "5352512", "3961930", "1091771", "183"]
    random_storage = ["I.S.", "M.S.", "P.S.", "ampm", "PSI", "IS", "PST", "/", ", ,"]
    # Street name code, so much to parse out...
    kid_distribution_name_dump = [s for s in kid_distribution_dump if " X" in s]
    kid_distribution_name_dump = [re.sub(r'[^a-zA-Z \n.]', '', file) for file in kid_distribution_name_dump]
    for i in range(len(storage_for_directions)):
        kid_distribution_name_dump = [w.replace(storage_for_directions[i], '') for w in kid_distribution_name_dump]
    for i in range(len(storage_for_common_streets)):
        kid_distribution_name_dump = [w.replace(storage_for_common_streets[i], '') for w in kid_distribution_name_dump]
    kid_distribution_name_dump = [re.sub(r'\b\w{1,2}\b', '', file) for file in kid_distribution_name_dump]
    for i in range(len(storage_for_street_names)):
        kid_distribution_name_dump = [w.replace(storage_for_street_names[i], '') for w in kid_distribution_name_dump]
    for i in range(len(storage_for_districts)):
        kid_distribution_name_dump = [w.replace(storage_for_districts[i], '') for w in kid_distribution_name_dump]
    kid_distribution_name_dump = [w.replace("..", '') for w in kid_distribution_name_dump]
    kid_distribution_name_dump = [w.replace(".", '') for w in kid_distribution_name_dump]
    kid_distribution_name_dump = [w.replace("X", ' ') for w in kid_distribution_name_dump]
    for i in range(len(random_storage)):
        kid_distribution_name_dump = [w.replace(random_storage[i], '') for w in kid_distribution_name_dump]
    print(kid_distribution_name_dump)
    kid_distribution_zipcode =  [i for i in kid_distribution_dump if re.findall(r'.*(\d{5}(\-\d{4})?)$', i)]
    kid_distribution_zipcode = [re.sub(r'[^0-9 \n\.]', '', file) for file in kid_distribution_zipcode]
    kid_distribution_zipcode = [re.sub(r'\b\d{1,4}\b', '', file) for file in kid_distribution_zipcode]
    kid_distribution_zipcode = [w.replace(" .    . ", '') for w in kid_distribution_zipcode]
    
    kid_distribution_phone =  [i for i in kid_distribution_dump if re.findall(r'.*(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', i)]
    kid_distribution_phone = [w.replace("am", '') for w in kid_distribution_phone ]
    kid_distribution_phone = [w.replace("pm", '') for w in kid_distribution_phone ]
    kid_distribution_phone = [w.replace("X", '') for w in kid_distribution_phone ]
    kid_distribution_phone = [w.replace(":", '') for w in kid_distribution_phone]
    kid_distribution_phone = [w.replace("-", '') for w in kid_distribution_phone]
    kid_distribution_phone = [w.replace("–", '') for w in kid_distribution_phone]
    for i in range(len(storage_for_districts)):
        kid_distribution_phone = [w.replace(storage_for_districts[i], '') for w in kid_distribution_phone]
    for i in range(len(storage_for_common_streets)):
        kid_distribution_phone = [w.replace(storage_for_common_streets[i], '') for w in kid_distribution_phone]
    for i in range(len(storage_for_directions)):
        kid_distribution_phone = [w.replace(storage_for_directions[i], '') for w in kid_distribution_phone]
    for i in range(len(storage_for_street_names)):
        kid_distribution_phone = [w.replace(storage_for_street_names[i], '') for w in kid_distribution_phone]
    for i in range(len(storage_for_time)):
        kid_distribution_phone = [w.replace(storage_for_time[i], '') for w in kid_distribution_phone]
    for i in range(len(zipcode_of_nyc)):
        kid_distribution_phone = [w.replace(zipcode_of_nyc[i], '') for w in kid_distribution_phone]
    
    kid_distribution_phone = [re.sub(r'\b\d{0,4}\b', '', file) for file in kid_distribution_phone]
    for i in range(len(x_number)):
        kid_distribution_phone = [w.replace(x_number[i], '') for w in kid_distribution_phone]
    kid_distribution_phone = [re.sub(r'[^0-9\n\.]', '', file) for file in kid_distribution_phone]
    kid_distribution_phone = [w.replace("..", '') for w in kid_distribution_phone]
    
    kid_distribution_street_address = [s for s in kid_distribution_dump if " X" in s]
    kid_distribution_street_address = [w.replace("X", '') for w in kid_distribution_street_address]
    kid_distribution_street_address = [w.replace("–", '') for w in kid_distribution_street_address]
    kid_distribution_street_address = [w.replace("-", '') for w in kid_distribution_street_address]
    kid_distribution_street_address = [w.replace(":", '') for w in kid_distribution_street_address]
    for i in range(len(storage_for_time_settings)):
        kid_distribution_street_address = [w.replace(storage_for_time_settings[i], '') for w in kid_distribution_street_address]
    for i in range(len(storage_for_districts)):
        kid_distribution_street_address = [w.replace(storage_for_districts[i], '') for w in kid_distribution_street_address]
    kid_distribution_street_address = [re.sub(r'\b\d{5,18}\b', '', file) for file in kid_distribution_street_address]
    for i in range(len(storage_for_time)):
        kid_distribution_street_address = [w.replace(storage_for_time[i], '') for w in kid_distribution_street_address]
    for i in range(len(random_storage)):
        kid_distribution_street_address = [w.replace(random_storage[i], '') for w in kid_distribution_street_address]
        
    kid_distribution_district = [s for s in kid_distribution_dump if "X" in s]
    kid_distribution_district = [re.sub(r'[^a-zA-Z \n\.]', '', file) for file in kid_distribution_district]   #kid_distribution_district = [s for s in kid_distribution_dump if " " + storage_for_districts[i] in s]
    for i in range(len(storage_for_time_settings)):
        kid_distribution_district = [w.replace(storage_for_time_settings[i], '') for w in kid_distribution_district]
    for i in range(len(storage_for_directions)):
        kid_distribution_district = [w.replace(storage_for_directions[i], '') for w in kid_distribution_district]
    for i in range(len(storage_for_street_names)):
        kid_distribution_district = [w.replace(storage_for_street_names[i], '') for w in kid_distribution_district]
    for i in range(len(storage_for_common_streets)):
        kid_distribution_district = [w.replace(storage_for_common_streets[i], '') for w in kid_distribution_district]
    for i in range(len(random_storage)):
        kid_distribution_district = [w.replace(random_storage[i], '') for w in kid_distribution_district]
    kid_distribution_district = [w.replace("X", '') for w in kid_distribution_district]
    kid_distribution_district = [w.replace("X", '') for w in kid_distribution_district]
    
    print(kid_distribution_district)
    dump_parts(kid_distribution_dump, name, "kid-dump")
    dump_parts(senior_distribution_dump, name, "senior-dump")
    csv_creator(name, "completedump", kid_distribution_name_dump, kid_distribution_phone, kid_distribution_street_address, kid_distribution_zipcode, "The Bronx")
    
    
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