import tensorflow as tf
import os

class TPUColab:
    def __init__(self):
        # init TPU
        try:
            self.device_name = os.environ['COLAB_TPU_ADDR']
            self.TPU_ADDRESS = 'grpc://' + self.device_name
            print('Found TPU')
        except KeyError:
            self.device_name = ''
            self.TPU_ADDRESS = ''
            print('TPU not found')

    def get_device_name(self):
        return self.device_name

    def get_TPU_ADDRESS(self):
        return self.TPU_ADDRESS

    def is_tpu_available(self):
        return self.TPU_ADDRESS != ''

    def compiled_model_to_tpu_model(self, model):
        tf.contrib.tpu.keras_to_tpu_model(
            model,
            strategy=tf.contrib.tpu.TPUDistributionStrategy(
                tf.contrib.cluster_resolver.TPUClusterResolver(self.TPU_ADDRESS)))
