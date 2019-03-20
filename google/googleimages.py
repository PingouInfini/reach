import configparser
import json
import re
import os
import urllib.request
from google_images_download import google_images_download


def treatment(user):
    config = configparser.RawConfigParser()
    config.read('properties.config')

    get_metadata_from_username(user, config)
    download_img_from_metadata(user, config)

    #check_fileinfo(config.get('GoogleImages', 'googleimages.outputdirectory') + "/" + user)


def get_metadata_from_username(user, config):
    limit = config.get('GoogleImages', 'googleimages.limit')

    # class instantiation
    response = google_images_download.googleimagesdownload()

    # creating list of arguments
    arguments = {"keywords": user, "limit": limit,
                 "extract_metadata": True, "no_download": True,
                 "output_directory": "logs", "no_directory": True,
                 "type":"face"}
    # passing the arguments to the function and get metadata
    response.download(arguments)


def download_img_from_metadata(user, config):
    fname = "logs/" + user + ".json"
    output_directory = "google/"+config.get('GoogleImages', 'googleimages.outputdirectory') + "/" + user

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    with open(fname) as json_file:
        data = json.load(json_file)
        index = 0
        for img_data in data:
            index += 1
            img_filename = re.sub('[^a-zA-Z]+', '', img_data['image_description'])
            img_filename = str(index) + "-" + img_filename + ".jpg"
            try:
                get_image_and_add_metadata(img_data['image_link'], output_directory, img_filename)
            except:
                try:
                    get_image_and_add_metadata(img_data['image_thumbnail_url'], output_directory, img_filename)
                except:
                    pass


def get_image_and_add_metadata(source, output_directory, img_filename):
    urllib.request.urlretrieve(source, output_directory + "/" + img_filename)

    #TODO add metadata///
    # with open(output_directory + "/" + img_filename) as f:
    #     f.fileinfo = {'image_source': img_data['image_source']}
        # metadata = pyexiv2.ImageMetadata(f)
        # metadata.read()

# def check_fileinfo(path):
#     for file in os.listdir(path):
#         print (os.stat(path+"/"+file))