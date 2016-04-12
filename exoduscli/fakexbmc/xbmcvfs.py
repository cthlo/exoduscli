import os

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def delete(file):
    raise NotImplementedError

def listdir(path):
    raise NotImplementedError

class File(object):
    pass
