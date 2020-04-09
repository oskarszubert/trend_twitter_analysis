# -*- coding: utf-8 -*-
import collections
import re
import os
from math import log
try:
    from src.PreprocessData import *
except:
    from PreprocessData import *

class Vectorization():
    def __init__(self):
        self.p_text = PreprocessData()


    def df_vectorization(self, df, algo='tf-idf'):  # df-idf is default value
        self.df = df[0]
        self.p_text = PreprocessData()

        self.read_vocabulary()
        self.term_frequency(algo)
        return (self.df,df[1])


    def df_vectorization_from_file(self,read_file,path_to_file, algo='tf-idf'):  # df-idf is default value
        self.df = pd.read_excel(path_to_file + read_file)
        self.p_text = PreprocessData()

        self.read_vocabulary()
        self.term_frequency(algo)
        self.save_to_file(read_file, path_to_file=path_to_file)


    def df_vectorization_twitter_test(self,algo='tf-idf'):
        path_to_file = 'model_train_data/twitter_test/'
        dir_list = ['music/','politics/','realityshow/','services/','sport/','all_twitter/']

        for dir_name in dir_list:

            self.df = pd.read_excel(path_to_file + dir_name + 'test_dataset.xlsx')
            self.p_text = PreprocessData()

            self.read_vocabulary()
            self.term_frequency(algo)
            self.save_to_file('test_dataset.xlsx', path_to_file='model_train_data/dataset/twitter_test/'+dir_name)


    def read_vocabulary(self, filename='config/vocabulary/vocabulary.txt'):
        vocabulary = []
        self.idf_dict = {}
        try:
            file = open(filename,'r')
        except Exception as e:
            print("Error! Cannot open file")
            print(e)
            exit(0)

        for line in file:
            line = line.strip('\n').split(';')
            self.idf_dict[line[0]] = line[1]
            vocabulary.append(line[0])
        file.close()

        self.vector_template = dict.fromkeys(set(vocabulary),0)


    def term_frequency(self,algo):
        for i in range( self.df.shape[0] ):
            vector = dict(self.vector_template)
            tweet = self.p_text.clean_data( self.df.loc[i,'text'] )
            tweet_len = len(tweet)
            for token in tweet:
                if token in vector:
                    vector[token] += 1
            vector_tf = []
            if len(tweet):
                for token in vector:
                    if token in vector:
                        if algo == 'tf-idf':
                            vector_tf.append( (vector[token]/tweet_len ) * float(self.idf_dict[token]) )
                        elif algo == 'tf':
                            vector_tf.append( (vector[token]/tweet_len ) )
                        elif algo == 'bow':
                            vector_tf.append( vector[token] )
                        elif algo == 'binary':
                            if vector[token]:
                                vector_tf.append(1)
                            else:
                                vector_tf.append(0)
            else:
                vector_tf = list(self.vector_template.values())

            self.df.loc[i,'vector'] = str( vector_tf )


    def save_to_file(self,filename, path_to_file = 'collected_data/vectorized/'):
        if not os.path.exists( path_to_file ):
            os.makedirs(path_to_file)
        filename = path_to_file + filename.lower()

        self.df.to_excel(filename,index=False)
        print('File: \'' + filename + '\' saved!')
