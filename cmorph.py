#!/usr/bin/env python
"""
Copyright 2022 ARC Centre of Excellence for Climate Extremes

author: Paola Petrelli <paola.petrelli@utas.edu.au>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

This script is used to download, checksum and update the CMORPH 8km-30min v1.0 dataset on
 the NCI server
 modified from autogenerated script from the website
 Original code by tcram@ucar.edu (Thomas Cram)
The dataset is stored in /g/data/ia39/aus-ref-clim-data-nci/cmorph/data
The code logs files are currently in /g/data/ia39/aus-ref-clim-data-nci/cmorph/code/update_log.txt
 Created:
      2022-06-01
 Last change:
      2022-06-28

 Usage:
 Inputs are:
   y - year to download/update the only one required
   m - month to download/update multiple allowed as -m 02 03 ...
   u - user RDA account email
   d - to run in debug mode
 The RDA account  password should be set as the environment variable: RDAPSWD

 Uses the following modules:
   requests to download files and html via http
   argparse to manage inputs
   sys, os, calendar and datetime 
   utility functions from util.py file

"""

import sys, os
import requests
import argparse
import calendar
from datetime import datetime
from util import set_log, check_mdt, print_summary
import dateutil.parser


def parse_input():
    '''Parse input arguments '''

    parser = argparse.ArgumentParser(description='''
    Retrieve CMORPH v1.0 netcdf files from the RDA server
        https://rda.ucar.edu/data/ds502.2/
    using requests to download the files.
    Usage: python cmorph.py -y <year> -u <username>  
    where username is the email account on RDA''',
             formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-y','--year', type=str, required=True,
                        help="year to process")
    parser.add_argument('-m','--month', type=str, required=False,
                        nargs='*', help="month to process")
    parser.add_argument('-d','--debug', action='store_true', required=False,
                        help='Print out debug information, default is False'),
    parser.add_argument('-u','--user', required=True,
              help="Username for rda.ucar.edu account")
    return vars(parser.parse_args())


def check_file_status(filepath, filesize):
    status = 'incomplete'
    sys.stdout.write('\r')
    sys.stdout.flush()
    size = int(os.stat(filepath).st_size)
    percent_complete = (size/filesize)*100
    sys.stdout.write('%.3f %s' % (percent_complete, '% Completed'))
    sys.stdout.flush()
    if percent_complete == 100:
        status = 'complete' 
    return status

def authenticate(username, data_log):
    """ """ 
    pswd = os.environ['RDAPSWD']
    url = 'https://rda.ucar.edu/cgi-bin/login'
    values = {'email' : username, 'passwd' : pswd, 'action' : 'login'}
    # Authenticate
    ret = requests.post(url,data=values)
    if ret.status_code != 200:
        data_log.info('Bad Authentication')
        data_log.info(ret.text)
        exit(1)
    return ret


def download_file(ret, filename, file_base, update, data_log):
    req = requests.get(filename, cookies = ret.cookies, allow_redirects=True, stream=True)
    filesize = int(req.headers['Content-length'])
    if update:
        exists = check_mdt(req, file_base, data_log)
        if exists:
            return 'skip' 
    with open(file_base, 'wb') as outfile:
        chunk_size=1048576
        for chunk in req.iter_content(chunk_size=chunk_size):
            outfile.write(chunk)
            if chunk_size < filesize:
                check_file_status(file_base, filesize)
    status = check_file_status(file_base, filesize)
    return status


def get_filelist(yr, mns, data_dir):
    """Create file list based on year and months"""
    flist = []
    for mn in mns:
        fpath = f'v1.0/30min/8km/{yr}/{mn}/' 
        os.makedirs(f"{data_dir}/{fpath}", exist_ok=True)
        fname = f'CMORPH_V1.0_ADJ_8km-30min_{yr}{mn}DD00.nc'
        lastday = calendar.monthrange(int(yr), int(mn))[1]
        days = ["%.2d" % i for i in range(1,lastday+1)]
        fmonth = [fpath+fname.replace('DD', x) for x in days] 
        flist.extend(fmonth)  
    return flist


def main():
    # get input arguments
    # if month is not specified download all
    args = parse_input()
    yr = args['year']
    allmns = ["%.2d" % i for i in range(1,13)]
    mns= args['month']
    if mns is None:
        mns = allmns

    # set paths and filenames
    root_dir = os.getenv("AUSREFDIR", "/g/data/ia39/aus-ref-clim-data-nci")
    data_dir = f"{root_dir}/cmorph/data"
    dspath = 'https://rda.ucar.edu/data/ds502.2/'
    flog = f"{root_dir}/cmorph/code/update_log.txt"

    # set log
    today = datetime.today().strftime('%Y-%m-%d')
    user = os.getenv('USER')
    level = "info"
    if args["debug"]:
        level = "debug"
    data_log = set_log('cmorphlog', flog, level)
    data_log.info(f"Updated on {today} by {user}")

    # authenticate
    username = args['user']  
    ret = authenticate(username, data_log)

    # create file list based on year and months
    flist = get_filelist(yr, mns, data_dir) 
    updated = []
    new = []
    error = []
    # download
    # NB remote dir is cmorph_v1.0, we use only v1.0 locally as cmorph is included in drs already 
    for fpath in flist:
        remote = dspath + f"cmorph_{fpath}"
        file_base = f"{data_dir}/{fpath}"
        exists = os.path.exists(file_base)
        if exists:
            update = True
        else:
            update = False
        status = download_file(ret, remote, file_base, update, data_log)
        if status == 'complete':
            if update:
                updated.append(fpath)
            else:
                new.append(fpath)
        elif status == 'incomplete':
            error.append(fpath)

    print_summary(updated, new, error, data_log)

if __name__ == "__main__":
    main()
