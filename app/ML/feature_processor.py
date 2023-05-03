import en_core_web_sm
from fuzzywuzzy import fuzz


class feature_processor:
    """
    This is what processes the features within sentences.  Uses cosine similarity to find whether a specifically labeled entity is in a sentence
    entities : a list of files containing the specific elements to look out for
    labels : the labels that each of these file's elements should be labelled in respective order of entities
    """

    def __init__(self, entities, labels):
        self.tagged_entities = []
        self.labels = []
        for i in range(len(entities)):
            try:
                with open(entities[i]) as f:
                    lines = f.readlines()
                    self.tagged_entities.append([line.strip() for line in lines])
                self.labels.append(labels[i])

            except FileNotFoundError:
                pass

    def process_features(self, text):
        """
        This processes the text to extract features
        """
        nlp = en_core_web_sm.load()
        normalized_words = text.lower().split(" ")
        text = nlp(text)
        ents = [
            (i, i.label_)
            for i in text.ents
            if i.label_ == "PERSON"
            or i.label_ == "FAC"
            or i.label_ == "WORK_OF_ART"
            or i.label_ == "ORG"
        ]
        matches = []
        for token, label in ents:
            if label != "PERSON":
                m = self.find_match(str(token))
                if m is not None:
                    print(m)
                    matches.append(m)
            else:
                matches.append((token, label))

        for word in normalized_words:
            m = self.find_match(word)
            if m is not None:
                matches.append(m)

        return matches

    def find_match(self, token):
        """
        Helper linear search method that looks for a fuzzy match between the token and the items you find in the list
        token : the token we are searching for in our tagged_entities
        """
        for i, entities in enumerate(self.tagged_entities):
            for entity in entities:
                if fuzz.ratio(entity, token) > 90:
                    return (entity, self.labels[i])
        return None
