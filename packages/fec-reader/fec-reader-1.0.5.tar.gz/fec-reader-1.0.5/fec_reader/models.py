import os
import time
import requests
import pandas as pd
from . import utils


class DataReader():

    def __init__(self, DATA_DIR=None):
        if DATA_DIR:
            self.DATA_DIR = DATA_DIR
        else:
            self.DATA_DIR = os.getcwd()
        self.website = 'https://www.fec.gov'


    def get_pac_summary(self):

        PAC_DIR = os.path.join(self.DATA_DIR, 'pac_summary')
        utils.check_dir(PAC_DIR)

        utils.get_header(self.website + '/campaign-finance-data/pac-and-party-summary-file-description/', PAC_DIR, 'header.txt')

        pac_files = [   '/files/bulk-downloads/2018/webk18.zip',
                        '/files/bulk-downloads/2016/webk16.zip',
                        '/files/bulk-downloads/2014/webk14.zip',
                        '/files/bulk-downloads/2012/webk12.zip',
                        '/files/bulk-downloads/2010/webk10.zip',
                        '/files/bulk-downloads/2008/webk08.zip',
                        '/files/bulk-downloads/2006/webk06.zip',
                        '/files/bulk-downloads/2004/webk04.zip'    ]

        for url in pac_files:
            utils.print_to_shell("Getting file from {}".format(url))
            req = requests.get( self.website + url )
            utils.save_zip(req.content, PAC_DIR)

            time.sleep(5)


    def get_candidate_master(self):

        CAN_DIR = os.path.join(self.DATA_DIR, 'candidate_master')
        utils.check_dir(CAN_DIR)

        utils.get_header(self.website + '/campaign-finance-data/candidate-master-file-description/', CAN_DIR, 'header.txt')

        can_files = [   '/files/bulk-downloads/2018/cn18.zip',
                        '/files/bulk-downloads/2016/cn16.zip',
                        '/files/bulk-downloads/2014/cn14.zip',
                        '/files/bulk-downloads/2012/cn12.zip',
                        '/files/bulk-downloads/2010/cn10.zip',
                        '/files/bulk-downloads/2008/cn08.zip',
                        '/files/bulk-downloads/2006/cn06.zip',
                        '/files/bulk-downloads/2004/cn04.zip',
                        '/files/bulk-downloads/2002/cn02.zip'  ]

        for url in can_files:
            utils.print_to_shell("Getting file from {}".format(url))
            req = requests.get( self.website + url )
            utils.save_zip(req.content, CAN_DIR)

            # janky fix to all candidate master files being named 'cn.txt' LOL
            fix = url.replace('.zip', '')
            filename = 'cn' + str(fix[-2:]) + '.txt'
            os.rename( os.path.join(CAN_DIR, 'cn.txt'), os.path.join(CAN_DIR, filename) )

            time.sleep(5)
