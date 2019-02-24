import urllib 
import zipfile
import csv
from redis_db import parseFile
import urllib.request

#downloads data for given date
def download(dirpath,filename):
    url = "https://www.bseindia.com/download/BhavCopy/Equity/"+filename
    urllib.request.urlretrieve(url, dirpath+filename)


def extract(filepath,outpath):
    with zipfile.ZipFile(filepath, "r") as z:
        z.extractall(outpath)

DOWNLOAD_PATH = "data/download/"
PROCESS_PATH = "data/process/"

#downloads, unzips and inserts data to redis
def scrapeData(date):
    # date = "210219"
    download(DOWNLOAD_PATH,"EQ"+date+"_CSV.ZIP")
    extract(DOWNLOAD_PATH+"EQ"+date+"_CSV.ZIP",PROCESS_PATH)
    parseFile(PROCESS_PATH+"EQ"+date+".CSV")
    return {"inserted data"}

