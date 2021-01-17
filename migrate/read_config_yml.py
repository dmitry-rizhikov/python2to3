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

    def do_clone(self):
        try:
            return self.cfg['clone']
        except KeyError:
            return False

    def do_pylint_before_futurize(self):
        try:
            return self.cfg['pylint-before-futurize']
        except KeyError:
            return True

    def do_futurize(self):
        try:
            return self.cfg['futurize']
        except KeyError:
            return True

    def get_replace_src(self):
        try:
            return self.cfg['replace-in-files']['src']
        except KeyError:
            return None

    def get_replace_dest(self):
        try:
            return self.cfg['replace-in-files']['dest']
        except KeyError:
            return None
