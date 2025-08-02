"""
Author: Nik Alleyne   
Author Blog: https://www.securitynik.com   
Author GitHub: github.com/securitynik   

Author Other Books: [   

            "https://www.amazon.ca/Learning-Practicing-Leveraging-Practical-Detection/dp/1731254458/",   
            
            "https://www.amazon.ca/Learning-Practicing-Mastering-Network-Forensics/dp/1775383024/"   
        ]   


This script ***(load_model.py)*** is part of the series of notebooks From ***A Little Book on Adversarial AI***  A free ebook released by Nik Alleyne

"""
# TO DO: add a command argument for making predictions

# This script will be used to load our models going forward

import argparse
import logging
import sys
import os
import pickle
import torch

# Clear the screen
os.system('clear')
print(f'Torch version used:  {torch.__version__}')


# Setup the logger
# https://docs.python.org/3/howto/logging.html
#logger = logging.getLogger(name='SANS_SEC_5XX')
logging.getLogger(name='SANS_SEC_5')
logging.basicConfig(level=logging.INFO)


def usage_info():
    print(f'*'*25)
    print('Author: Nik Alleyne (SecurityNik)')
    print('Code designed specifically for SANS SEC5')
    print('$ python ./load_model.py --model /path/to/some_model_file')
    print(f'Date: February, 2025')
    print(f'*'*25)


# Define the function to load the model
def load_model(model_file_path:str=None):
    logging.info(msg=f'Loading model file {model_file_path} ...')
    
    if model_file_path.endswith('.pkl'):
        logging.info(msg='Processing a pickle file ...')

        with open(file=model_file_path, mode='rb') as fp:
            # read the model into a variable
            trusted_model = pickle.load(file=fp)

        # When we look at the trusted_model or the results returned from the load, we see
        print(f'This is the original content of the file: {trusted_model}')

    
    elif model_file_path.endswith('.pt') or model_file_path.endswith('.pth'):
        logging.info(msg='Processing a torch file ...')

        with torch.no_grad():
            try:
                trusted_model = torch.load(model_file_path, weights_only=False)
                print(f'This is the original content of the file: {trusted_model}')
            except Exception as e:
                logging.WARNING('[!] Looks like there might have been a warning here ...')


    elif model_file_path.endswith('.onnx'):
        logging.info(msg='Processing ONNX file. This format is considered very secure')
        logging.info(msg='NICE CHOICE!')
    
    else:
        logging.WARNING(msg='Processing an unknown file ...')



if __name__ == '__main__': 
    # Check the number of arguments passed to the script
    if len(sys.argv) < 3:
        usage_info()
        sys.exit(1)
    
    parser = argparse.ArgumentParser(
        usage='./load_model.py --model /path/to/some_model_file',
        prog='sans_sec_595',
        description='Load a model'
        )
    
    #parser.add_argument('--help', './load_model.py --model /path/to/model_file')
    parser.add_argument('-m', '--model', help='The path to the model file')
    cmd_args = parser.parse_args()

    if cmd_args.model:
        load_model(model_file_path=sys.argv[2])