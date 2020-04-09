
# -*- coding: utf-8 -*-
from PreprocessData import *
from math import log

class CreateVocabulary():
    def __init__(self):
        self.vocabulary = {}
        self.prepare_text = PreprocessData()
        self.number_of_documents = 0

    def create(self,filename,size):
        path_to_dict = 'config/vocabulary/tmp/vocab_with_numbers.txt'
        if os.path.exists( path_to_dict ):
            self.read_dict_from_file( path_to_dict )

        path_to_file = 'model_train_data/tagged/' + filename
        df = pd.read_excel(path_to_file)
        self.number_of_documents += df.shape[0]
        for i in range( df.shape[0] ):
            tweet = self.prepare_text.clean_data( df.loc[i,'text'] )
            set_tweet = list(set(tweet))
            for token in tweet:
                if token in self.vocabulary:
                    self.vocabulary[token][0] += 1
                else:
                    tmp_list = [1,0]
                    self.vocabulary[token] = tmp_list
            for token in set_tweet:
                if token in self.vocabulary:
                    self.vocabulary[token][1] += 1

        vocabulary = self.vocabulary
        sorted_vocabulary = sorted(vocabulary.items(), key=lambda vocabulary: vocabulary[1], reverse=True)
        self.save_vocab_with_numbers(sorted_vocabulary[:3000])
        self.vocabulary_to_file(sorted_vocabulary[:size])


    def read_dict_from_file(self, path_to_dict):
        try:
            file = open(path_to_dict,"r")
        except Exception as e:
            print("Error! Cannot create file")
            print(e)
            exit(0)

        self.number_of_documents += int(file.readline())
        for line in file:
            line = line.strip('\n').split(';')
            if len(line) == 1:
                continue
            if line[0] in self.vocabulary:
                self.vocabulary[ line[0] ][0] += int(line[1])
                self.vocabulary[ line[0] ][1] += int(line[2])
            else:
                self.vocabulary[ line[0] ] = [int(line[1]),int(line[2])]


    def save_vocab_with_numbers(self, vocabulary, filename='vocab_with_numbers.txt'): 
        path_to_file = 'config/vocabulary/tmp/'
        if not os.path.exists( path_to_file ):
            os.makedirs(path_to_file)

        path_to_file += filename
        try:
            file = open(path_to_file,"w+")
        except Exception as e:
            print("Error! Cannot create file")
            print(e)
            exit(0)

        file.write(str(self.number_of_documents)+'\n')
        for token in vocabulary:
            file.write(str(token[0]) + ';' + str(token[1][0]) + ';' + str(token[1][1]) +'\n')
        file.close()


    def vocabulary_to_file(self, vocabulary, filename='vocabulary.txt'): 
        path_to_file = 'config/vocabulary/'
        if not os.path.exists( path_to_file ):
            os.makedirs(path_to_file)

        path_to_file += filename
        try:
            file = open(path_to_file,"w+")
        except Exception as e:
            print("Error! Cannot create file")
            print(e)
            exit(0)

        vocabulary.sort()

        for token in vocabulary:
            idf = log(int(self.number_of_documents)/int(token[1][1]))
            file.write(token[0] + ';' + str(idf) + '\n')

        file.close()
        print('File: \'' + filename + '\' saved!')
