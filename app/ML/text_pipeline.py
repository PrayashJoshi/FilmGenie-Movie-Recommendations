import itertools
import tensorflow as tf
from .sentiment_model import sentiment_model
import nltk
from .feature_processor import feature_processor


class text_pipeline:
    """
    Combines our sentiment analysis model and our feature extraction pipeline to extract important features that were positively rated from a user's reviews
    genres : a list of genres that the model should look for when extracting important features
    movies : a list of movies that the model should look for when extracting important features
    otherwise, the model will rely on spacy to extract important nouns such as movies, genres, actors, and actresses
    """

    def __init__(self) -> None:
        """
        constructor
        genres : the list of genres that we may find in our text
        movies : the list of movies that we may find our text
        """
        sm = sentiment_model()
        self.model = sm.getModel()
        self.tokenizer = sm.getTokenizer()
        self.feature_processor = feature_processor(
            ["genres.txt", "movie_names.txt", "filmitems.txt"],
            ["GENRE", "MOVIE", "FILMITEM"],
        )

    def gauge_sentiment(self, text) -> int:
        """
        gauges the sentiment on the body of text sent in
        1 reflects a positive rating
        0 reflects a negative rating
        """
        
        with tf.device('/cpu:0'):
            batch = self.tokenizer(
                text, max_length=128, padding=True, truncation=True, return_tensors="tf"
            )
            out = self.model(batch)
            predictions = tf.nn.softmax(out["logits"], axis=-1)
            label = tf.argmax(predictions, axis=1)[0]
            label = label.numpy()
            return label

    def extract_features(self, corpus) -> list:
        """
        extracts the important features from a corpus of text.  These can be movie elements including names,
        """
        return self.feature_processor.process_features(corpus)

    def gauge_and_extract(self, corpus) -> list:
        """
        combines the sentiment analysis and feature extraction to return only the movie elements from a review that are rated positively
        returns a list of elements that are positively rated by the user
        """
        all_extracted_features = []
        for sent in nltk.sent_tokenize(corpus):
            if self.gauge_sentiment(sent) == 1:
                all_extracted_features.append(self.extract_features(sent))

        return list(itertools.chain.from_iterable(all_extracted_features))
