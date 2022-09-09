import os
import sqlite3
import json
import requests
import re
import matplotlib

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

from glob import glob

def get_doi_from_dir_path(dir_path):
    doi = dir_path.split("datasets/")[1]
    doi = doi.replace("-", ":", 1)
    doi = doi.replace("-", "/")
    return(doi)

def strip_newlines(doi):
    return(doi.strip("\n"))
strip_newlines_v = np.vectorize(strip_newlines)

def write_file_from_string(filename, to_write):
    with open("../md_inserts/" + filename, "w") as outfile:
        outfile.write(to_write)
        
def get_doi_from_results_filename(filename):
    doi = filename.split("/")[3]
    doi = doi.replace("-", ":", 1)
    doi = doi.replace("-", "/")
    return(doi)
get_doi_from_results_filename_v = np.vectorize(get_doi_from_results_filename)

def get_doi_from_tag_name(image_tag):
    return(image_tag[6:9] + image_tag[9:len(image_tag)].replace("-", ":", 1).upper().replace("-", "/"))

def get_doi_from_report(report):
    report_dict = json.loads(report)
    return(get_doi_from_tag_name(report_dict["Additional Information"]["Container Name"]))
get_doi_from_report_v = np.vectorize(get_doi_from_report)

def get_time_from_report(report):
    report_dict = json.loads(report)
    return(report_dict["Additional Information"]["Build Time"])
get_time_from_report_v = np.vectorize(get_time_from_report)

def create_script_id(doi, filename):
    return(doi + ":" + os.path.basename(filename).lower())
create_script_id_v = np.vectorize(create_script_id)

# This function categorizes error messages by searching for the most unique and common phrases in different types of R error messages
def determine_error_cause(error_msg):
    ret_val = "other"
    if(error_msg == "success"):
        ret_val = error_msg
    elif(error_msg == "timed out"):
        ret_val = error_msg
    elif("Error in setwd" in error_msg):
        ret_val = "working directory"
    elif("Error in library" in error_msg): 
        ret_val = "library"
    elif("unable to find required package" in error_msg): 
        ret_val = "library"
    elif("Error in file" in error_msg):
        ret_val = "missing file" 
    elif("such file or directory" in error_msg):
        ret_val = "missing file" 
    elif("unable to open" in error_msg):
        ret_val = "missing file"
    elif("cannot open file" in error_msg):
        ret_val = "missing file"
    elif("does not exist in current working directory" in error_msg):
        ret_val = "missing file"  
    elif("does not exist" in error_msg and (".checkpoint" not in error_msg and "Unsupported get request" not in error_msg)):
        ret_val = "missing file"  
    elif("Error in readChar" in error_msg):
        ret_val = "missing file"
    elif("File to copy does not exist" in error_msg):
        ret_val = "missing file"
    elif("could not find function" in error_msg):
        ret_val = "function"
    elif("there is no package called" in error_msg):
        ret_val = "library"
    elif("cannot open the connection" in error_msg):
        ret_val = "missing file"
    elif("object" in error_msg and "not found" in error_msg):
        ret_val = "missing object"
    return(ret_val)
determine_error_cause_v = np.vectorize(determine_error_cause)

# Download metadata of a doi from a dataset
def get_dataset_metadata(doi, api_url="https://dataverse.harvard.edu/api/"):
    '''
    problem_set = set(["doi:10.7910/DVN/I6H7L5\n",
                       "doi:10.7910/DVN/IBY3PN\n",
                       "doi:10.7910/DVN/NEIYVD\n",
                       "doi:10.7910/DVN/HVY5GR\n",
                       "doi:10.7910/DVN/HVY5GR\n",
                       "doi:10.7910/DVN/UPL4TT\n",
                       "doi:10.7910/DVN/65XKJO\n",
                       "doi:10.7910/DVN/VUHAXF\n",
                       "doi:10.7910/DVN/0WAEAM\n",
                       "doi:10.7910/DVN/PJOMF1\n"])
    # This data has to be hard-coded later. Not sure why, these always time out
    if doi in problem_set:
        print("Skipping problematic dataset")
        return (False,False)
    '''
    api_url = api_url.strip("/")
    subject = None
    year = None
    num_files = None
    timeout_duration = 7
    timeout_limit = 4
    attempts = 0
    while (attempts < timeout_limit):
        try:
            request = requests.get(api_url + "/datasets/:persistentId",
                             params={"persistentId": doi}).json()
            if(request["status"] == "ERROR"):
                print("Possible incorrect permissions for " + doi)
                return (False, False)
            # query the dataverse API for all the files in a dataverse
            files = request['data']
        except requests.exceptions.ReadTimeout as e:
            attempts += 1
            if(attempts == timeout_limit):
                print("Timed-out too many times. Check internet connection?")
                print(doi)
                with open("../data/metadata_problem.txt", "a") as meta_prob:
                    meta_prob.write(doi + " timeout\n")
                return (False, False)
            else:    
                print("Timeout hit trying again")
                continue
        except Exception as e:
            print("Could not get dataset info from dataverse")
            print(e)
            with open("../data/metadata_problem.txt", "a") as meta_prob:
                meta_prob.write(doi + " " + e + "\n")
            return (False, False)
        break
        
    
    year = files["publicationDate"][0:4]
    if("latestVersion" not in files):
        print("latestVersion issue")
        print(doi)
    else:
        for field in files["latestVersion"]["metadataBlocks"]["citation"]["fields"]:
            if(field["typeName"] == "subject"):
                subject = field["value"]

    return(subject, year)

def is_clean(doi, scripts_df):
    ret_val = False
    doi_df = scripts_df[scripts_df["doi"] == doi]
    if len(doi_df.index) > 0:
        ret_val = False
        errors = set(doi_df["nr_error"].values)
        if "success" in errors and len(errors) == 1:
            ret_val = True
    return ret_val