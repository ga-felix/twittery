import csv
import os

# Get settings directory
dir = os.path.dirname(__file__)

# Setup global target variables
def init():

    global user_timeline
    user_timeline = set()

    with open(dir + '/targets/user_timeline.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        first = True
        for row in csv_reader:
            if first:
                first = False
                continue
            user_timeline.add(row[0])