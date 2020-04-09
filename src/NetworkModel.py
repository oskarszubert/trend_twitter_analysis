import os
import pandas as pd
import numpy as np
from sklearn.utils import shuffle
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix 
import re


class NetworkModel():
    def predict_tweets(self, df, model_name, path_to_file='collected_data/tagged/', save_to_file_switch=True):
        filename = df[1]
        df = df[0]
        model = tf.keras.models.load_model(model_name)
        tweets, sentient = self.get_array_from_dataset(df=df)

        predictions = model.predict(tweets)

        for i in range(df.shape[0]):
            df.loc[i, 'sentient'] = -1 if np.argmax(predictions[i]) == 2 else np.argmax(predictions[i])

        if not os.path.exists(path_to_file):
            os.makedirs(path_to_file)
        df = df.drop(columns=['vector'])  # 'text'
        df.to_excel(path_to_file + filename.lower() + '.xlsx', index=False)
        if save_to_file_switch:
            print('File \'' + str(path_to_file +
                                  filename.lower() + '.xlsx \''), 'saved!')
        else:
            return df


    def create_model(self, vocabulary_size, layers, epochs):
        model = tf.keras.Sequential()
        filename = str(epochs) + ';' + str(vocabulary_size) + ';' + str(layers)

        model.add(tf.keras.layers.Dense(
            layers[0], activation='relu', input_shape=(vocabulary_size,)))
        for neuron in layers[1:]:
            model.add(tf.keras.layers.Dense(neuron, activation='relu'))

        model.add(tf.keras.layers.Dense(3, activation='softmax'))
        model.summary()

        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])

        train_text, train_sentient = self.get_array_from_dataset(
            'model_train_data/dataset/train_dataset.xlsx', vocabulary_size=vocabulary_size)
        test_text, test_sentient = self.get_array_from_dataset(
            'model_train_data/dataset/test_dataset.xlsx', vocabulary_size=vocabulary_size)

        print(len(train_text), len(train_sentient))
        print(len(test_text), len(test_sentient))
        model_history = model.fit(train_text,
                                  train_sentient,
                                  epochs=epochs,
                                  validation_data=(test_text, test_sentient),
                                  verbose=1)

        model.save('config/model.h5')
        self.model_plots(model_history, filename)
        # self.evaluate_tweets(model_name='config/model.h5',vocabulary_size=vocabulary_size)
        self.create_confusion_matrix(model_name='config/model.h5',vocabulary_size=vocabulary_size)


    def get_array_from_dataset(self, filename='', df=None, vocabulary_size=300):
        if filename:
            df = pd.read_excel(filename)
        text = []
        sentient = []
        number_of_documents = df.shape[0]
        for i in range(number_of_documents):
            if df.loc[i, 'sentient'] != 5:
                if int(df.loc[i, 'sentient']) == -1:
                    sentient.append(2)
                else:
                    sentient.append(int(df.loc[i, 'sentient']))
            vector = df.loc[i, 'vector']
            vector = re.sub(r'\'', '', vector)
            vector = re.sub(r'\[|\]', '', vector)

            vector = [float(x) for x in vector.split(', ')]
            text.append(vector[:vocabulary_size])

        return np.array(text), sentient

    def shuffe_dataset(self, filename, path_to_file):
        df = pd.read_excel(filename)
        df = shuffle(df)
        test_train_border = int(df.shape[0] * 0.7)

        if not os.path.exists(path_to_file):
            os.makedirs(path_to_file)
        df[:test_train_border].to_excel(
            path_to_file+'train_' + filename.split('/')[-1], index=False)
        df[test_train_border:].to_excel(
            path_to_file+'test_' + filename.split('/')[-1], index=False)


    def save_dataset_to_dir(self, percent, df):
        df = shuffle(df)
        test_train_border = int(df.shape[0] * percent/100)

        path_to_file = 'model_train_data/dataset/'
        if not os.path.exists(path_to_file):
            os.makedirs(path_to_file)

        df[:test_train_border].to_excel(
            path_to_file+'test_dataset.xlsx', index=False)
        return df[test_train_border:]


    def model_plots(self, model_history, filename):
        path_to_file = 'model_train_data/plots/'
        if not os.path.exists(path_to_file):
            os.makedirs(path_to_file)

        plt.plot(model_history.history['acc'])
        plt.plot(model_history.history['val_acc'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.savefig(path_to_file+filename+'_accuracy.png')

        plt.clf()

        plt.plot(model_history.history['loss'])
        plt.plot(model_history.history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.savefig(path_to_file+filename+'_loss.png')

        plt.clf()

        file = open('model_train_data/model_results.csv', 'a')

        file.write(filename + ';' +
                   str(model_history.history['acc'][-1]) + ';' +
                   str(model_history.history['loss'][-1]) + ';' +
                   str(model_history.history['val_acc'][-1]) + ';' +
                   str(model_history.history['val_loss'][-1]) + ';')
        file.close()


    def evaluate_tweets(self,model_name,vocabulary_size):
        model = tf.keras.models.load_model(model_name)

        file = open('model_train_data/model_results.csv', 'a')

        path_to_dir = 'model_train_data/dataset/twitter_test/'
        filename = 'test_dataset.xlsx'
        dir_list = ['music/','politics/','realityshow/','services/','sport/','all_twitter/']

        for dir_name in dir_list:
            test_text = ''
            test_sentient = ''
            test_text, test_sentient = self.get_array_from_dataset(path_to_dir + dir_name + filename,
                                                                    vocabulary_size=vocabulary_size)
            scores = model.evaluate(test_text, test_sentient)
            file.write(str(scores[1]) + ';' +str(scores[0]) + ';')


        file.write('\n')
        file.close()


    def create_confusion_matrix(self,model_name,vocabulary_size):
        model = tf.keras.models.load_model(model_name)

        test_text, test_sentient = self.get_array_from_dataset(
            'model_train_data/dataset/test_dataset.xlsx', vocabulary_size=vocabulary_size)
        
        predictions_vect = model.predict(test_text)
        predictions = []

        for vect in predictions_vect:
            predictions.append(np.argmax(vect))
        matrix = confusion_matrix(test_sentient, predictions)

        file = open('model_train_data/confusion_matrix.txt', 'a')
        file.write('test_dataset matrix:\n'+str(matrix)+'\n')

        path_to_dir = 'model_train_data/dataset/twitter_test/'
        filename = 'test_dataset.xlsx'
        dir_list = ['music/','politics/','realityshow/','services/','sport/','all_twitter/']

        for dir_name in dir_list:
            test_text = ''
            test_sentient = ''
            test_text, test_sentient = self.get_array_from_dataset(path_to_dir + dir_name + filename,
                                                                    vocabulary_size=vocabulary_size)
            predictions = []
            predictions_vect = model.predict(test_text)

            for vect in predictions_vect:
                predictions.append(np.argmax(vect))
            matrix = confusion_matrix(test_sentient, predictions)
            matrix = matrix/len(test_sentient)
            
            scores = model.predict(test_text)
            file.write(dir_name[:-1]+':\n'+str(matrix)+'\n')

        file.close()
