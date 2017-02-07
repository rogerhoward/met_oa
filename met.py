#!/usr/bin/env python
import os, sys, csv
import requests
import json

data_url = 'https://media.githubusercontent.com/media/metmuseum/openaccess/master/MetObjects.csv'
local_data_path = 'data.csv'
padding = 10

def get_subdirectory(accession_number):
    """
    Takes the accession number and returns a path to a subdirectory, creating it if needed.
    Subdirectories calculated to contain up to 100 files.
    For example, given the accession number name 3168449, returns a path like:
    ./_data/03/16/84/
    """
    components = accession_number.zfill(padding)
    sub_dir = os.path.join(data_path, components[0:2], components[2:4], components[4:6], components[6:8])
    os.makedirs(sub_dir, exist_ok=True)
    return sub_dir


def get_met_records():
    """
    Return Met open access data as a list of dictionaries, suitable for encoding as JSON.
    """
    print('Getting Met open access data...')

    # Download CSV if not exists
    if not os.path.exists(local_data_path):
        print('Data file missing, downloading current version from Github...')
        r = requests.get(data_url, stream=True)
        with open(local_data_path, 'w') as f:
            for chunk in r.iter_content(chunk_size=10240): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
    else:
        print('Data already downloaded, will use it...')


    # Parse CSV, and convert to a list of dictionaries,
    # using first row as dictionary keys
    records = []
    with open(local_data_path, 'r') as f:
        csv_reader = csv.reader(f, delimiter=',', quotechar='"')
        header = None
        for row in csv_reader:
            if header:
                row = dict(zip(header, row))
                records.append(row)
            else:
                header = [x.strip('\ufeff') for x in row]

    return records


def save_met_data(records):
    """
    Save records into subdirectories, using padded Object ID as basis for
    subdirectory structure and filenames.
    """
    print('Saving Met open access data...')
    for record in records:
        accession_number = record['Object ID']
        file_name = '{}.json'.format(accession_number.zfill(padding))
        directory = get_subdirectory(accession_number)

        path = os.path.join(directory, file_name)
        with open(path, 'w') as f:
            json.dump(record, f, indent=4, ensure_ascii=False, sort_keys=True)


if __name__ == "__main__":
    repo_path = os.path.dirname(os.path.realpath(sys.argv[0]))    # Path to current directory
    data_path = os.path.join(repo_path, '_data')                  # Root path for record data
    os.makedirs(data_path, exist_ok=True)                         # Create _data directory

    records = get_met_records()                                   # Fetch Met open access data, convert to dictionaries
    save_met_data(records)                                        # Save it into _data
