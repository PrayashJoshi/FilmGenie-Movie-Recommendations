from text_pipeline import text_pipeline


def main():
    """
    This is an example driver that we can use to generate values from the text pipelines
    """
    pipe = text_pipeline()
    sentence = "The Shawshank Redemption was an amazing experience.  Morgan Freeman gave a class act performance, and the plot and characters were both executed very well."
    print(pipe.gauge_sentiment(sentence))
    print(pipe.extract_features(sentence))


if __name__ == "__main__":
    main()
