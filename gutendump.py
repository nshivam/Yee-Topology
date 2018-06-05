import random
import os
import sys
import re
import math
import optparse
import urllib.request
import requests

# Format: random.sample(sample range, number of samples)
file_numbers = random.sample(range(1, 53017), 5)

# Specify path to a folder where you want your Gutendump
path = 'C:\\Users\\shivn\\Desktop\\Gutendump\\'

for i in range(len(file_numbers)):
    file_number = str(file_numbers[i])
    URL = "http://www.gutenberg.org/files/" + file_number + "/" + file_number + ".txt"

    open_file = urllib.request.urlopen(URL)
    data = open_file.read()

    number = file_number + ".txt"
    fileName = path + number

    file = open(fileName, 'wb')
    file.write(data)
