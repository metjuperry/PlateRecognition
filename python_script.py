import sys
import urllib2
from bs4 import BeautifulSoup
from openalpr import Alpr
import mysql.connector

webpage = "https://spz.penize.cz/"

config = {
    'user': 'root',
    'password': 'root',
    'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock',
    'database': 'ScannedRegistration',
    'raise_on_warnings': True,
}


def sanitize(string_input):
    for letter in range(0, len(string_input)):
        if string_input[letter] == ":":
            return string_input[letter + 2:]
    return string_input


def make_information_list(information_table):
    return [information_table[0].findAll("a")[0].string, information_table[0].findAll("a")[2].string,
            sanitize(information_table[0].findAll("p")[4].string),
            sanitize(information_table[0].findAll("p")[5].string),
            sanitize(information_table[0].findAll("p")[6].string)]


def main(webpage_to_scrape, database_config):
    alpr = Alpr("eu", "/config/alprd.conf.defaults", "/Users/matejsamler/Downloads/openalpr-master/runtime_data")
    if not alpr.is_loaded():
        print "Error loading OpenALPR"
        return -1

    con = mysql.connector.connect(**database_config)
    cursor = con.cursor()

    alpr.set_top_n(20)
    alpr.set_default_region("md")

    results = alpr.recognize_file(sys.argv[1])
    most_likely_plate = ""

    for plate in results['results']:
        for candidate in plate['candidates']:
            if candidate['confidence'] == plate['confidence']:
                most_likely_plate = candidate['plate']

    webpage_to_scrape = webpage_to_scrape + most_likely_plate
    try:
        soup = BeautifulSoup(urllib2.urlopen(webpage_to_scrape), "html.parser")
    except urllib2.HTTPError:
        con.commit()
        cursor.close()
        con.close()
        alpr.unload()
        return -1
    else:
        information_table = soup.findAll("div", class_="col1")

    indatabasequerry = "SELECT * FROM cars WHERE Plate = '" + most_likely_plate + "'"
    querry = "INSERT INTO `cars` (`Plate`, `Region`, `Insurance`, `Duration`, `Type`, `Brand`) VALUES ('" + most_likely_plate + "'"

    cursor.execute(indatabasequerry)
    rows = cursor.fetchall()
    if len(rows) > 0:
        return rows[0][0]
    else:
        for information in make_information_list(information_table):
            querry = querry + " ,'" + information + "'"
        querry = querry + ");"

        cursor.execute(querry)
        con.commit()

        cursor.execute(indatabasequerry)
        rows = cursor.fetchall()
        if len(rows) > 0:
            return rows[0][0]

    # Call when completely done to release memory
    cursor.close()
    con.close()
    alpr.unload()


print main(webpage, config)
