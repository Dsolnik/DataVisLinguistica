# [
#       {
#        stem: 'cool', 
#        total_occurance : 15, 
#        instances : { 'er' : 10, 'es' : 20, 'ed' 30, 'er' : 40}
#        weighted_instances : {'er' : 0.1, 'es' : 0.2, 'ed' : 0.3, 'er' : 0.4}
#       }
# ]

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.tools.plotting import radviz

plt.style.use('ggplot')

def get_data_from_stem(word):
        data = {}
        infile =  "browncorpus_stemtowords_2.txt"
        with open (infile, "r" ) as infile:
                for line in infile:
                        items = line.split()
                        if len(items) == 0 or line[0] == '-':
                                continue
                        if not (items[0] == word):
                                continue
                        data['stem'] = items[0]
                        data['total_occurances'] = int(items[1])
                        data['instances'] = dict()
                        num_stems = (len(items) - 3) / 3
                        for i in range(num_stems):
                                new_word = items[(i + 1) * 3]
                                num_occur = int(items[(i + 1) * 3 + 1])
                                percent = float(items[(i + 1) * 3 + 2][:-1]) / 100.0
                                data['instances'][new_word] = [num_occur, percent]
                return data

def get_words_from_stem(word):
        data = []
        infile = "browncorpus_Signatures.txt"
        with open (infile, "r") as infile:
                found = False
                for line in infile:
                        if not (found):
                                if line[0] == '=' and line.split()[1] == word:
                                        found = True
                        else:
                                if len(line) == 0:
                                        continue
                                else: 
                                        if line[0] == '-':
                                                return data
                                        else:
                                                words = line.split()
                                                for i in words:
                                                        data.append(i)
                return data

def get_words_data_from_signature(word):
        data = {}
        list_stems = get_words_from_stem(word)
        if len(list_stems) == 0:
                return 0
        for stem in list_stems:
                word_data = get_data_from_stem(stem)
                data[word_data['stem']] = word_data
        return data 

def normalize(series):
        a = min(series)
        b = max(series)
        if b - a == 0:
                return (series * 10000) / 9999
        return (series - a) / (b - a)

def max(array):
        max = array[0]
        for i in array:
                if i > max:
                        max = i
        return max

        
def min(array):
        min = array[0]
        for i in array:
                if i < min:
                        min = i
        return min 

def replace(array):
        for index, item in enumerate(array):
                array[index] = (item * 10000 + index + 1)/ 9999

while True:
        test = True
        colors = ['r', 'g', [0,0,0,0]]
        query = raw_input('Enter the signature to search for: ')
        if len(get_words_from_stem(query)) == 0:
                print "no signature matching that found"
        else:
                plt.figure()
                list_words = get_words_data_from_signature(query)
                print len(list_words.keys())
                # suffixes = query.split('-')
                # stems = []
                # values = dict()
                # # initialize dictionary of arrays as:
                # # {'suffix' : [] , 'suffix' : []}
                # for suffix in suffixes:
                #         values[suffix] = [0]
                # values["Name"] = [0]
                
                for word in list_words.itervalues():
                        suffixes = query.split('-')
                        stems = []
                        values = dict()
                        # initialize dictionary of arrays as:
                        # {'suffix' : [] , 'suffix' : []}
                        for suffix in suffixes:
                                values[suffix] = [0]
                        values["Name"] = [0]
                        stems.append(word["stem"])
                        stems.append("placeholder1")
                        if word["total_occurances"] > 10:
                                values["Name"].append('Greater Than 10')                    
                        else:
                                values["Name"].append('Less than 10')
                        values["Name"].append('BAD')
                        minimum = 999999
                        maximum = 0
                        for suffix in suffixes:
                                new_word = word["stem"] + suffix
                                if suffix == "NULL":
                                        new_word = word["stem"]
                                occur = word["instances"][new_word][0] * 1.0
                                if occur > maximum:
                                        maximum = occur
                                if occur < minimum:
                                        minimum = occur
                                values[suffix].append(occur)
                        for suffix in suffixes:
                                values[suffix].append(maximum)
                        for index in values:
                                if(min(values[index]) == max(values[index]) and len(values[index]) != 1):
                                        replace(values[index])
                        data = pd.DataFrame(values)
                        ax = radviz(data, "Name", color = colors)
                        ax.legend_.remove()
                        if test:
                                print data.iloc[[1]]
                                plt.show()
                print "done"
                plt.show() 

def normalize(array):
        maximum = max(array)
        return map(lambda x: x / maximum, array)

def generate_points_on_circle(num):
        arr = []
        for i in range(num):
                rad = i * 2 * math.pi / num
                arr.append( [ math.sin(rad), math.cos(rad) ])

def generate_weighted_average(dict):
        
