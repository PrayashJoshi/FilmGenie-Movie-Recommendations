import spacy
from spacy.tokens import Span
import random
from spacy.util import minibatch, compounding
import re
from spacy.training import Example
from spacy.pipeline import EntityRecognizer


class ner:
    '''
        Spacy's named entity recognizer finetuned to recognize labels and movie names
        sources can be found here : https://spacy.io/usage/training#ner
                                    https://spacy.io/usage/saving-loading/
                                    https://towardsdatascience.com/train-ner-with-custom-training-data-using-spacy-525ce748fab7
    '''

    def __init__(self):
        nlp = spacy.load('en_core_web_sm')
        self.nlp = nlp

    def train_new_label(self, train_file, label, epochs):
        nlp = self.nlp

        train_data = self.get_train_data(train_file, label)

        ner = EntityRecognizer(nlp.vocab, entity_types=['MOVIE'])
        nlp.add_pipe(ner)
        """         for data in train_data:
            # print(data[1])
            start, end, label = data[1]['entities']
            ex = (data[0], {"entities": [(start, end, label)]})
            nlp.update([ex], drop=0.5, sgd=nlp.create_optimizer())
        """
        total_train_losses = []

        print('Training ...........')
        nlp.begin_training()
        for i in range(epochs):
            print('Epoch ' + str(i + 1))
            random.shuffle(train_data)
            losses = {}
            batches = minibatch(train_data, size=5)
            for batch in batches:
                for example in batch:
                    doc = nlp(example[0])
                    ex = Example.from_dict(
                        doc, example[1])
                    nlp.update([ex], losses=losses, sgd=nlp.create_optimizer())
            total_train_losses.append(losses)

        return total_train_losses

    def get_train_data(self, train_file, label):
        train_data = []

        with open(train_file, 'r') as f:
            for line in f.readlines():
                # find the index of the first quotation mark
                try:
                    sentence = re.search(r'"([^"]*)"', line)
                    match = sentence.group(1)
                    # print(match)
                except AttributeError:
                    continue
                # extract the sentence between the quotations
                # find the index of the opening bracket
                bracket_idx = line.find('[')

                indxs = list(
                    map(int, line[bracket_idx+1:line.find(']', bracket_idx)].split(', ')))
                train_data.append(
                    (match, {"entities": [(indxs[0], indxs[1], label)]}))

        return train_data

    def save_pipeline(self, dir):
        self.nlp.to_disk("./" + str(dir))

    def get_model(self):
        return self.nlp
