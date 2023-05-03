from ner import ner


def main():
    ner_sample = ner()
    losses = ner_sample.train_new_label('train_file_movie.txt', "MOVIE", 5)
    print(losses)

    with open('val_file.txt', 'r') as f:
        sentences = f.readlines()
        for s in sentences:
            tokens = ner_sample.get_model()(s)
            print(tokens)
            print([ent for ent in tokens.ents])


if __name__ == "__main__":
    main()
