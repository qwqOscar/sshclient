from dotenv import load_dotenv
import os


class Config:
    def __init__(self, path='./.env'):
        load_dotenv(dotenv_path=path, verbose=True)
        self.dict = {}
        self.dict['host'] = os.getenv('HOST')
        self.dict['port'] = int(os.getenv('PORT'))
        self.dict['username'] = os.getenv('USER')
        self.dict['pwd'] = os.getenv('pwd')
    def get(self, key:str):
        return self.dict[key]
