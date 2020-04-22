import os
import sys
import json
from csv import DictReader
from src.hardcoded_resources import TSV_FILE_NAME

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")


##
# Checks if folder for data download exists,
# if not then creates one.
def create_data_directory():
    if not directory_exists(ROOT_DIR, "data"):
        create_directory(ROOT_DIR, "data")


##
# Checks if folder/file exists inside given path.
#
# @param: parent_dir - directory which should contain file to be checked
# @param: dir_name - folder/file to check
# @returns: True if folder/file exists, else False
def directory_exists(parent_dir, dir_name):
    return os.path.exists(os.path.join(parent_dir, dir_name))


##
# Creates folder inside given path.
#
# @param: parent_dir - directory which should contain new folder
# @param: dir_name - new folder name
def create_directory(parent_dir, dir_name):
    os.mkdir(os.path.join(parent_dir, dir_name))


##
# Checks if folder for data download exists inside project directory.
#
# @returns: True if data folder exists, else False
def data_dir_exists():
    return directory_exists(ROOT_DIR, "data")


##
# Creates folder for data download inside project directory.
def create_data_dir():
    create_directory(ROOT_DIR, "data")


##
# Downloads data from response of earlier invoked web request and saves in storage.
# Also, prints download progress to stdout.
#
# @param: dir_name - string stating name of folder, inside which downloaded data will be stored
# @param: sat_scan_completion_date - string containing datetime of satellite scan,
# serves as part of name, which will be given to downloaded file
# @param: download_response - response of earlier executed web request, containing stream of data to download
def download(dir_name, sat_scan_completion_date, download_response):
    if not directory_exists(DATA_DIR, dir_name):
        create_directory(DATA_DIR, dir_name)

    file_name = dir_name + '_' + sat_scan_completion_date + '.zip'

    with open(os.path.join(os.path.join(DATA_DIR, dir_name), file_name), 'wb') as data_file:
        print("\nDownloading %s" % file_name)
        total_data_length = download_response.headers.get('content-length')

        if total_data_length is None:
            data_file.write(download_response.content)
        else:
            data_length = 0
            total_data_length = int(total_data_length)
            for data in download_response.iter_content(chunk_size=4096):
                data_length += len(data)
                data_file.write(data)
                progress = int(50 * data_length / total_data_length)
                sys.stdout.write("\r[%s%s]" % ('=' * progress, ' ' * (50 - progress)))
                sys.stdout.flush()


##
# Saves given json string in storage.
#
# @param: dir_name - string stating name of folder, inside which downloaded data will be stored
# @param: json_name - string, serves as part of name, which will be given to downloaded file
# @json_string - string containing json to be stored
def store_json(dir_name, json_name, json_string):
    if not directory_exists(DATA_DIR, dir_name):
        create_directory(DATA_DIR, dir_name)

    file_name = dir_name + '_' + json_name + '.json'

    open(os.path.join(os.path.join(DATA_DIR, dir_name), file_name), 'w').write(json.dumps(json_string))


##
# Loads eruptions data from *.tsv file located at project directory and puts them inside list in form of tuples.
# Eruption tuple has following structure:
#   (<volcano_name>, <year_of_eruption>, <month>, <day>, <latitude>, <longitude>)
def load_tsv():
    eruption_list = list()
    with open(os.path.join(ROOT_DIR, TSV_FILE_NAME), 'r') as csv_file:
        csv_reader = DictReader(csv_file, dialect='excel-tab')
        header = next(csv_reader)
        for row in csv_reader:
            if row['Year'] != '' and row['Mo'] != '' and row['Dy'] != '' and row['Name'] != '' and row['Latitude'] != '' and row['Longitude'] != '':
                eruption_list.append((row['Name'], row['Year'], row['Mo'], row['Dy'], row['Latitude'], row['Longitude']))
        print("Loaded %s csv rows" % len(eruption_list))
        # in order to have newest eruptions first, list is reversed
        eruption_list.reverse()
        return eruption_list

