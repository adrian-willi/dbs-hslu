from pymongo import MongoClient
import logging
import logging.handlers

#TODO connection to MongoDB on enterpriseLab server
class ConnectToDB:
    #logger setup, use logger.info(or level needed)('Log message') to log
    logging.basicConfig(filename='log.txt', level=logging.INFO, format='Class: %(name)s - Time: %(asctime)s - Level: %(levelname)s - Message: %(message)s')
    logger = logging.getLogger('ConnectToDB')


    def get_client(self):
        self.logger.info('Connect to MongoDB')
        return MongoClient()

    def get_clientRemote(self):
        self.logger.info('RemoteConnection to MongoDB')
        return MongoClient('IpAddress')




