'''
  By: Michael Shea

  This python scripts removes flawed major data that was saved to the
  MajorsData folder.
'''

import os

# delete any file that is less than 1kb
for file in os.listdir('MajorsData'):
    if(os.path.getsize('MajorsData/' + file) < 1000):
        print("Removing Major Data for " + file)
        os.remove('MajorsData/' + file)
