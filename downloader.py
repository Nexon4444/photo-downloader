import argparse
import json
import os
import re
import shutil
from os import path

import requests

parser = argparse.ArgumentParser()

main_grp = parser.add_argument_group('Main parameters')
main_grp.add_argument('-i', '--input-file', help = '<INPUT_FILE> text file containing the json list. Ex: list.json')
main_grp.add_argument('-o', '--output-directory', help = '<OUTPUT_DIRECTORY> (optional): output directory (default \'./downloaded_pictures/\')')
options = parser.parse_args()
output_format = 'png'

def filter_bad_filename_chars(filename):
    """
        Filter bad chars for any filename
    """
    # Before, just avoid triple underscore escape for the classic '://' pattern
    filename = filename.replace('://', '_')

    return re.sub('[^\w\-_\. ]', '_', filename)

def main():
    with open(path.join(options.input_file), "r") as f:
        datastore: dict = json.load(f)
        for key, val in reversed(sorted(datastore.items())):
            print(val["picture_link"])
            image_url = val["picture_link"]
            if image_url is None:
                continue
            output_filename = os.path.join(options.output_directory,
                                           ('%s.%s' % (filter_bad_filename_chars(key), output_format)))
            if os.path.exists(output_filename):
                print("omitting: " + str(output_filename))
                continue
            # Open the url image, set stream to True, this will return the stream content.
            resp = requests.get(image_url, stream=True)
            # Open a local file with wb ( write binary ) permission.
            local_file = open(output_filename, 'wb')
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            resp.raw.decode_content = True
            # Copy the response stream raw data to local image file.
            shutil.copyfileobj(resp.raw, local_file)

        print(datastore.keys())

        MYDIR = ("test")
        CHECK_FOLDER = os.path.isdir(MYDIR)

        # If folder doesn't exist, then create it.
        if not os.path.isdir(MYDIR):
            os.makedirs(MYDIR)
            print("created folder : ", MYDIR)

        else:
            print(MYDIR, "folder already exists.")
        # with open(path.join('data', name + '.txt'), 'w+') as w:
        #     for key in datastore.keys():
        #         w.write(key + "\n")

if __name__ == '__main__':
    main()
