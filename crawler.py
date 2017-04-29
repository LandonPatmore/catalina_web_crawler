import requests
import json
from bs4 import BeautifulSoup

transient_data = {}
transient_array = []

#change this to wherever you would like the file to save to
path_name = "<File path>"

'''
crawls the website specified and finds the table on the website and returns
the rows
'''
def LSST_crawler():
    url = "http://nesssi.cacr.caltech.edu/MLS/CRTSII_Allns.html"
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")

    table = soup.findChildren("table")
    my_table = table[0]

    rows = my_table.findChildren(["th", "tr"])
    return rows

'''
takes in the rows from the LSST_crawler() function and goes through the rows
and gets the data in the cells and strips the whitespace from them and then
creates objects inside of the dictionary which then is created as a file
specified where the user wants
'''
def set_data(rows):
    for row in rows:
        cells = row.findChildren("td")
        for cell in cells[:8]:
            transient_data[cells[0].text.lstrip().rstrip()] = {
                'ra' : cells[1].text.lstrip().rstrip(),
                'dec' : cells[2].text.lstrip().rstrip(),
                'ut_date' : cells[3].text.lstrip().rstrip(),
                'mag' : cells[4].text.lstrip().rstrip(),
                'last_time' : cells[6].text.lstrip().rstrip(),
                'light_curve' : cells[7].text.lstrip().rstrip()
            }
            break
    j = json.dumps(transient_data)
    with open("%s" % path_name, "w") as f:
        f.write(j)
        print("JSON created")

set_data(LSST_crawler())
