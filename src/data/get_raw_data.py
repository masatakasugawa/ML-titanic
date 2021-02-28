# -*- coding: utf-8 -*-
import os
from dotenv import find_dotenv, load_dotenv
from requests import session
import logging

# payload for login to kaggle
payload = {
            'action': 'login',
            'username': os.environ.get("KAGGLE_USERNAME"),
            'password': os.environ.get("KAGGLE_PASSWORD")
}

def extract_data(url, file_path):
    '''method to extract data'''
    # setup session
    with session() as c:
        c.post('https://www.kaggle.com/account/login', data=payload)
        
        # open file to write
        with open(file_path, 'wb') as file:
            response = c.get(url, stream=True)
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)

def main(project_dir):
    '''main method'''
    # get logger
    logger = logging.getLogger(__name__)
    logger.info('getting raw data')
                
    # urls
    train_url = 'https://storage.googleapis.com/kagglesdsdata/competitions/3136/26502/train.csv?GoogleAccessId=web-data@kaggle-161607.iam.gserviceaccount.com&Expires=1614771183&Signature=DffBf59T2E5QVnaYMEX2YK%2FukJSZ9Cye8cjvqjJfOce2Y4IbDKilwIVZ425RfbKqYwwrgJa7fgOclR%2Foadu7oHil%2Fhprs3OcjivXRY3%2BKVR5ZxF9WI9FTzsejPPXgSlfa3RN7QQs%2BWOeE2hA0KS9Vx05rxkiOWAAm3TpIE2F4CAxvl5grOh67WoaC1Aozy3YOGAgjGsjsn3ugXDzkP9vs9JJzRHw5Zfc%2FidJMZx1P9rSzbajB6iTDLG2hy3J3PnqTdGeArIfs9ehZ8SWniW5Uoqjl17NKgcF4GCAZndIOO4XCGEDAoUi7a5ovgZNpmFxqb22%2Fs7pf9l%2FUjdjXPT71g%3D%3D&response-content-disposition=attachment%3B+filename%3Dtrain.csv'
    test_url = 'https://storage.googleapis.com/kagglesdsdata/competitions/3136/26502/test.csv?GoogleAccessId=web-data@kaggle-161607.iam.gserviceaccount.com&Expires=1614771979&Signature=tDQwDZc9uRaSjjLWIeid7PTxPonxrWVSiNHwf7%2FoNauZ3hLFpy5Uh5K6jLrimc0ncxCJToh2dPp%2BV1WB%2FXdfUmnkipDSXVsDAgt%2BL017NU6WzvNBfFxtbhTX7aD3QslB5DhKidI6VYhwOq%2B0NdW0CIKHeJdWvj4NBUcgWnQXTf%2BbpwyvQy%2Fu1Aas%2B4LEy%2F8dojED4Uv9sKVnUyL0t6Q3%2FqXkeWnEb2YW4wtruH4lJAAWKpKWFgJmFYINixsGp60Cz%2F6jPsYKFc0rYHgxqf0b2Dcuv0I4j7w%2B5nQdepLHUc9n%2FT%2FBSSVwbCBaRm0zoWpDbBExClLJAJJmERNVqHc%2Fmg%3D%3D&response-content-disposition=attachment%3B+filename%3Dtest.csv'

    # file paths
    raw_data_path = os.path.join(project_dir, 'data', 'raw')
    train_data_path = os.path.join(raw_data_path, 'train.csv')
    test_data_path = os.path.join(raw_data_path, 'test.csv')

    # extract data
    extract_data(train_url, train_data_path)
    extract_data(test_url, test_data_path)
    logger.info('downloaded raw tranining and test data')

if __name__ == '__main__':
    # getting root directory
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    
    # setup logger
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    
    # find .env automatically by walking up directories until it's found
    dotenv_path = find_dotenv()
    # load up the entries as environment variables
    load_dotenv(dotenv_path)
    
    # call the main
    main(project_dir)
