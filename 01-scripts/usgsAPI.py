import os
import json

import pandas as pd

from datetime import datetime
from urllib3.util.retry import Retry

import requests
from requests.adapters import HTTPAdapter

# For plotting from the USGS URL in a scene:
import matplotlib.pyplot as plt
from PIL import Image
import requests
import numpy as np
from io import BytesIO
import matplotlib.image as mpimg

URL_USGS = "https://m2m.cr.usgs.gov/api/api/json/stable"

# send http request
def send_request(url, data, apiKey):  
    json_data = json.dumps(data)
    
    headers = {'X-Auth-Token': apiKey}              
    r = requests.post(url, json_data, headers = headers)       
    response = r.json()
    
    if r == None:
        print("No output from service")
        return None
        
    if r.status_code != 200:
        print("ERROR! ",r.text)
        return None
        
    return response["data"]

def login(username, password):
    USGS_API = "https://m2m.cr.usgs.gov/api/api/json/stable"
    url = '{}/login'.format(USGS_API)
    payload = json.dumps({
        "username": username,
        "password": password
    })

    # Create the request
    r = requests.post(url, payload)
    response = r.json()
    api_key = response["data"]
        
    if api_key is None:
        print(response.get("errorMessage", "Authentication failed"))

    return api_key

def logout(api_key):
    USGS_API = "https://m2m.cr.usgs.gov/api/api/json/stable"
    url = '{}/logout'.format(USGS_API)
    r = send_request(url, '', api_key)
    return r


def dataset_search(api_key, dataset="", catalog="", start_date=None, end_date=None, 
                   ll=None, ur=None):
    URL_USGS = "https://m2m.cr.usgs.gov/api/api/json/stable/"
    
    payload = {
        "datasetName": dataset,
        "catalog": catalog
    }

    if start_date and end_date:
        payload["temporalFilter"] = {
            "start": start_date,
            "end": end_date}

    if ll and ur:
        payload["spatialFilter"] = {
            "filterType": "mbr",
            "lowerLeft": ll,
            "upperRight": ur
        }
    
    datasets = send_request(URL_USGS+"dataset-search", payload, api_key)
    return datasets


def dataset_search_multi(api_key, dataset_aliases, catalog="EE", start_date=None, end_date=None, 
                   ll=None, ur=None):
    datasets = []
    for alias in dataset_aliases:    
        d = dataset_search(api_key, alias, catalog, start_date, end_date, ll, ur)
        if d!=None:
            datasets.append(d)
    return [d[0] for d in datasets]

def scene_search(api_key, dataset,
        max_results=5000,
        metadata_type=None,
        start_date=None, end_date=None,
        ll=None, ur=None,
        where=None, starting_number=1, sort_order="DESC"):
    
    URL_USGS = "https://m2m.cr.usgs.gov/api/api/json/stable/"
  
    payload = {
        "datasetName": dataset['datasetAlias'],
        "maxResults": max_results,
        "startingNumber": starting_number,
        "metadata_type": metadata_type
    }

    if (start_date is not None) and (end_date is not None):
        payload["sceneFilter"] = {}
        payload["sceneFilter"]["acquisitionFilter"] = {
            "start": start_date,
            "end": end_date
        }

    if ll and ur:
        payload["sceneFilter"]["spatialFilter"] = {
            "filterType": "mbr",
            "lowerLeft": ll,
            "upperRight": ur
        }

    if where:
        payload["sceneFilter"]["metadataFilter"] = {
            "filterType": "value",
            "filterId": where["filter_id"],
            "value": where["value"],
            "operand": "="
        }

    scenes = send_request(URL_USGS+"scene-search", payload, api_key)
    return scenes

def scene_search_multi(api_key, datasets, year_start, year_end, ll, ur):
    years = [str(x) for x in range(year_start, year_end)]
    scene_list = []
    
    for dataset in datasets:
        for y in years:
            date_start = y + "-06-21"
            date_end = y + "-09-22"

            scenes = scene_search(api_key, dataset, 5000, None, date_start, date_end, ll, ur) 
            if scenes["recordsReturned"] > 0:
                scene_list.append(scenes["results"])
    return scene_list



def filter_cloud_cover(scenes, cloud_limit=10.0):
    '''
    Given a list of scenes, filter for ones with cloud cover <= cloud_limit.
    
    I sense there is a way to do this within the API query, but I could not 
    find it. 
    '''
    filtered_scenes = []
    for sc in scenes:
        if float(sc["cloudCover"]) <= cloud_limit and \
            float(sc["cloudCover"]) >= 0.0:
            filtered_scenes.append(sc)
    return filtered_scenes

def is_contained(corner, coordspd):
    coordsmin = coordspd.min()
    coordsmax = coordspd.max()
    
    if corner['latitude'] > coordsmin[1] and \
        corner['latitude'] < coordsmax[1] and \
        corner['longitude'] > coordsmin[0] and \
        corner['longitude'] < coordsmax[0]:
        return True
    return False

def filter_lr_ul(scenes, lr, ul):
    '''
    Filter only for scenes that contain the latitude and longitude of the entire
    square of interest, so search for ones containing the lower right and upper
    left corners of the square.
    '''
    filtered_scenes = []
    for sc in scenes:
        # Not sure whether "spatialBounds" or "spacialCoverage" is more appropriate
        coordspd = pd.DataFrame(sc["spatialCoverage"]["coordinates"][0])
        if is_contained(lr, coordspd) and is_contained(ul, coordspd):
            filtered_scenes.append(sc)
                    
    return filtered_scenes


def view_scene(scene):
    """
    Given a scene object, plot the image by calling the 
    hyperlink in the metadata. 
    """
    r = requests.get(scene["browse"][0]["browsePath"])
    pil_im = Image.open(BytesIO(r.content))
    im_array = np.asarray(pil_im)
    plt.imshow(im_array)
    plt.show()