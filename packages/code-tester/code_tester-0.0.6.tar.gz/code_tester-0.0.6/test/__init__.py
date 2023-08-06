'''
import glob
import os.path

for filename in glob.glob(os.path.join(os.path.dirname(__file__), "test_*.py")):
    __import__("test." + os.path.basename(filename)[:-3])
'''
'''
I removed these are they were useless as pytest made it too simple to write tests
simply import things without worrying
'''
