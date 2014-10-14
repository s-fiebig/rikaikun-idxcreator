# -*- coding: utf-8 -*-
#
# Create idx file for rikaikun extension from edict(2).
# No error checks are done、e.g., missing files!
#
# The idx format is more or less self-explanatory.
# a. The whole file is sorted after the keys.
# b. The comma-separated numbers show the position, 
# i.e. char position disregarding the byte size 
# for unicode, in the file for each occurrence.
# This includes the dict entry itself and the
# pronunciation, which is in squared brackets in
# the dict file. 
# c. Katakana symbols are converted to Hiragana, 
# except ヴ [vu].
#
# key,pos1,pos2
# key2,pos1,pos2,pos3 

import codecs
from collections import OrderedDict
import jcconv
import re

def create_idx_file(datfile, idxfile):
    print "Reading in dat file..."
    words = OrderedDict()
    position = 0
    with codecs.open(datfile, 'r', "utf-8") as f:
        for line in f:   
            # TODO create key for each ; separated value
            temp = line.split(' ', 1)[0]
            temp2 = line.split(';', 1)[0]
            if len(temp) < len(temp2):
                symbol = temp
            else:
                symbol = temp2

            # vu wouldn't be converted if not reserved, but for clarity purposes ...
            symbol = jcconv.kata2hira(symbol, 'ヴ')
            if not words.get(symbol):
                words.update({symbol : str(position)})
            else:
                words.update({symbol : words.get(symbol) + "," + str(position)})

            symbol_in_brackets = re.search(r'\[(.*?)\]', line.split('/', 1)[0])
            if symbol_in_brackets:
                symbol_in_brackets = symbol_in_brackets.group(1)
                # vu wouldn't be converted if not reserved, but for clarity purposes ...
                symbol_in_brackets = jcconv.kata2hira(symbol_in_brackets, 'ヴ')
                if words.get(symbol_in_brackets):
                    words.update({symbol_in_brackets : words.get(symbol_in_brackets) + "," + str(position)})
                else:
                    words.update({symbol_in_brackets : str(position)})   

            position += len(line)
    print "Finished reading in dat file, now sorting index..."

    words = OrderedDict(sorted(words.items(), key=lambda t: t[0]))
    print "Finished sorting index, now writing idx file..."

    with codecs.open(idxfile, 'w+', "utf-8") as f:
        for key, value in  words.iteritems():
            f.write(key + "," + value + "\n")
    print "Finished writing idx file"


if __name__ == '__main__':
    create_idx_file("dict.dat", "dict.idx")