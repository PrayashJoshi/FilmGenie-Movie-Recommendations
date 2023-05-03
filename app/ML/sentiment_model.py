from tensorflow import keras
import tensorflow as tf
from transformers import TFBertForSequenceClassification, BertTokenizer
import os
from huggingface_hub import login


class sentiment_model:
    """
    This class houses our sentiment analysis model and allows for training, validation, and metrics reporting
    """

    def __init__(self):
        with tf.device('/cpu:0'):
            # load the model which is pretrained from a SaveModel object
            model = tf.saved_model.load("./binary_sa_bert_final")
            self.tok = BertTokenizer.from_pretrained("bert-base-uncased")
            self.model = model

    def getModel(self):
        return self.model

    def getTokenizer(self):
        return self.tok

    def train(self):
        """
        TODO: write in training alg
        """
        pass

    def validate(self):
        """
        TODO: create a validation loop for our model
        """
        pass

    def metrics_report(self):
        """
        TODO: return a metrics report for our sentiment analysis model
        """
        pass
