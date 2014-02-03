__author__ = 'ismailsunni'
__project_name = 'NewsAnalytic'
__filename = 'Crawler'
__date__ = '03/02/14'
__copyright__ = 'imajimatika@gmail.com'
__doc__ = ''

import urllib2
import pickle
import os
from libs.xgoogle.search import GoogleSearch, SearchError
from BeautifulSoup import BeautifulSoup

from NewsTitle import NewsTitle

DATA_DIRECTORY = '../data'

def get_page_soup(url):
    """Download a page and return a BeautifulSoup object of the html
    """
    try:
        content = urllib2.urlopen(url).read()
        return BeautifulSoup(content)
    except Exception, e:
        print e
        return None

def search_all(query, site=''):
    """
    Search all from a site of a keyword.
    Return list of instance of SearchResult which has url, desc, and title
    """
    if site != '':
        query = query + ' site:' + site
    results = []
    try:
        gs = GoogleSearch(query)
        gs.results_per_page = 100
        while True:
            tmp = gs.get_results()
            if not tmp: # no more results were found
                break
            results.extend(tmp)
        return results
    except SearchError, e:
        print 'Search failed: %s' % e
        return []

def save_pickle(data, filepath):
    """
    Pickle data, return the path
    """
    try:
        pickle.dump(data, open(filepath, 'wb'))
        return filepath
    except IOError, e:
        print 'Error save_pickle', e
        return None

def load_pickle(filepath):
    """
    Load data, return the data
    """
    try:
        data = pickle.load(open(filepath, 'rb'))
        return data
    except IOError, e:
        print 'Error load_pickle', e
        return None

def main():
    if not os.path.exists(DATA_DIRECTORY):
        os.mkdir(DATA_DIRECTORY)
    public_figures = ['jokowi', 'wiranto']
    sites = ['kompas.com', 'detik.com', 'okezone.com', 'vivanews.com']
    for public_figure in public_figures:
        for site in sites:
            print 'Search ', public_figure, 'in', site
            # Get all result from Google search
            results = search_all(public_figure, site)

            print 'We got', len(results),

            # Save to external file, to save a rate limit from Google
            filename = public_figure + '_' + site.replace('.', '') + '.pickle'
            filepath = os.path.join(DATA_DIRECTORY, filename)
            save_flag = save_pickle(results, filepath)
            if  save_flag is None:
                print 'Save to', filepath, 'failed'

            # Get all real title from the real site and create NewsTitle object
            news_titles = []
            for result in results:
                title = ''
                try:
                    print 'Get result from ', result.url
                    soup = get_page_soup(result.url)
                    # noinspection PyUnresolvedReferences
                    title = soup.title.string.encode()
                except Exception, e:
                    print e
                news_title = NewsTitle(title, public_figure, site,
                                       result.url, result.title, result.desc)
                news_titles.append(news_title)
            filename = 'newstitles_' + filename
            filepath = os.path.join(DATA_DIRECTORY, filename)
            save_flag = save_pickle(results, filepath)
            if  save_flag is None:
                print 'Save to', filepath, 'failed'

if __name__ == '__main__':
    main()