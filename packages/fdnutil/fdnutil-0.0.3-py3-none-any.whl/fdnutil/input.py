import logging
from fdnutil.whoami import iam
logger = logging.getLogger(name=iam())

def choice(text):
        yes = {'yes','y','ye',''}
        no = {'no','n'}
        c = input(text).lower()
        if c in yes:
            return True
        elif c in no:
            return False
        else:
            raise Exception("Please response with yes/no")