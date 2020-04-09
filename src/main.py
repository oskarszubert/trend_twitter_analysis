# -*- coding: utf-8 -*-
from OfflineMenu import * 

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    try:
        input_method = int(input('------------Run tool: \
                            \n\t[ 1 ]  Predict Tweets and create Raport.\
                            \n\t[ 2 ]  Collect Tweets.\
                            \n\t[ 3 ]  Create Vocabulary.\
                            \n\t[ 4 ]  Scrap from site.\
                            \n\t[ 5 ]  Clean single sentence.\
                            \n\t[ 6 ]  Create Dataset.\
                            \n\t[ 7 ]  Create Model.\
                            \n\t[ 8 ]  Vectorize twitter test data.\
                            \n\t[ 9 ]  Automatic tests.\
                            \n\t[ 0 ]  Exit \
                            \nYour choice: '))
    except Exception:
        print('*** Something went wrong! ***')
        exit(-1)

    menu = OfflineMenu()
    if input_method == 1:
        menu.predic_and_raport_ui()
    elif input_method == 2:
        menu.twitter_ui(save_to_file_switch=True)
    elif input_method == 3:
        menu.create_vocab_ui()
    elif input_method == 4:
        menu.scrapper_ui()
    elif input_method == 5:
        menu.clean_single_sentence_ui()
    elif input_method == 6:
        menu.create_dataset_ui()
    elif input_method == 7:
        menu.create_model_ui()
    elif input_method == 8:
        menu.vectorize_twitter_test_ui()
    elif input_method == 9:
        menu.model_test_ui()
    else:
        exit()
