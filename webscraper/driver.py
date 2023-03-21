from webscraper import webscraper
import pandas as pd
import sys


def main():
    '''
        Driver for the webscraper
    '''
    f_name = sys.argv[1]
    f = open(f_name)
    set_of_lines = set([line for line in f])
    dfs = []
    i = 0
    for line in set_of_lines:
        link = change_link(line)
        df = movie_review_to_df(link, line.split('/')[4])
        '''
        dfs.append(df)
        i += 1
        if i % 25 == 0:
            df = pd.concat(dfs)
            csv_name = f_name + str(i) + '_df.csv'
            df.to_csv(csv_name)
            dfs.clear()
        '''


def movie_review_to_df(link, movie_id):
    print(link)
    scraper = webscraper(link)
    dirty_reviews = scraper.get_dirty_reviews()
    ratings = [scraper.get_rating(review) for
               review in dirty_reviews]
    reviews = [scraper.get_review(review) for review in dirty_reviews]
    name = [scraper.get_name() for review in dirty_reviews]
    usernames = [scraper.get_username(review) for review in dirty_reviews]
    usefulness_rating = [scraper.get_usefulness_rating(
        review) for review in dirty_reviews]

    content = list(zip(usernames, ratings, reviews, usefulness_rating, name))
    df = pd.DataFrame(content, columns=[
                      'usernames', 'ratings', 'reviews', 'usefulness_rating', 'name'])
    df['id'] = movie_id
    df.set_index('id')
    return df


def change_link(link):
    link = link.split('/')
    link[-1] = 'reviews'
    link = '/'.join(link)
    return link


if __name__ == "__main__":
    main()
