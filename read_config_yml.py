import yaml


class Config:

    def __init__(self, file):
        with open(file, 'r') as ymlfile:
            self.cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)['python2to3']

    def get_path(self):
        try:
            return self.cfg['path']
        except KeyError:
            raise Exception('python2to3/path parameter in config.yml is mandatory')

    def get_excludes(self):
        try:
            return self.cfg['exclude']
        except KeyError:
            return None
