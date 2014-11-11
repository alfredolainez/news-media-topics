from multiprocessing import Pool
import newspaper

exclude = ['.jp', 'espanol', 'mexico', 'arabic']

def has_exclusion(url, exclude = exclude):
	'''
	Takes as input a string of a URL, and matches it 
	against a list of substrings that should not appear
	in URLS to consider
	'''
	for ex in exclude:
		if ex in url.lower():
			return True
	return False

def get_parsed(article, verbose=False):
	'''
	Takes a newspaper.Article object, downloads, parses it, 
	and sticks it in a dictionary.
	'''
	if verbose:
		print 'Processing {}'.format(a) 
	article.download()
	article.parse()
	return {'title' : article.title, 'text' : article.text, 'url' : article.url}

class Engine(object):
    def __init__(self, verbose = False):
        self.verbose = verbose
    def __call__(self, article):
        return get_parsed(article, self.verbose)


def article_cleaner(corpus, generator=True):
	def _is_empty(elem):
		for value in elem.values():
			if len(value) == 0:
				return True
		return False

	def _is_invalid(elem):
		if elem['title'] == 'Page not found':
			return True
		if 'page is not available' in elem['text'].lower():
			return True
		return False

	def _is_excluded(elem):
		return has_exclusion(elem['url'], exclude)
	def _is_clean(elem):
		return (not (_is_invalid(elem) or _is_empty(elem) or _is_excluded(elem)))

	if generator:
		return (article for article in corpus if _is_clean(article))
	return [article for article in corpus if _is_clean(article)]


def DefaultClean(elem):
	def _is_empty(elem):
		for value in elem.values():
			if len(value) == 0:
				return True
		return False
	def _is_invalid(elem):
		if elem['title'] == 'Page not found':
			return True
		if 'page is not available' in elem['text'].lower():
			return True
		return False
	def _is_excluded(elem):
		return has_exclusion(elem['url'], exclude)

	return (not (_is_invalid(elem) or _is_empty(elem) or _is_excluded(elem)))

class NewsScraper(object):
	"""NewsScraper -- A generic class for pulling from a news site, and dumping to a usable format.

	>>> news = NewsScraper('http://cnn.com')
	>>> news.pull()
	>>> news.scrape(10)
	>>> articles = news.polished()
	"""
	def __init__(self, website = '', nthreads = 10, memoize_articles = False):
		super(NewsScraper, self).__init__()
		self.website = website
		self.nthreads = nthreads
		self.memoize_articles = memoize_articles
		self.paper = None
		self.last_processed = 0
		self.corpus = []

	def pull(self, website = None):
		'''
		Builds a cached newspaper from the given website. 
		By Default, it looks at the website passed to the constructor
		'''
		if not (website is None):
			self.website = website
		if self.website is None:
			raise ValueError('NewsScraper does not have a website.')

		self.paper = newspaper.build(self.website, memoize_articles= self.memoize_articles, number_threads = 20, fetch_images = False, verbose = False)

	def scrape(self, num_articles = None):
		'''
		Performs mapreduce on the article downloading and parsing process.
		'''
		pool = Pool(self.nthreads) # on 100 processors
		engine = Engine(False)
		if num_articles is not None:
			self.corpus += pool.map(engine, self.paper.articles[self.last_processed:(num_articles + self.last_processed)])
			self.last_processed += num_articles
		else:
			self.corpus += pool.map(engine, self.paper.articles)
 
	def polished(self, cleaner = DefaultClean):
		'''
		By default, uses DefaultClean() which deletes empty articles and urls that 
		match the default exclude list. The cleaner parameter can be any function 
		that takes as input a dictionary with the fields 'text', 'url', and 'title', 
		and produces a boolean indicating whether or not it should be included.

		This produces a generator through list comprehention to save memory.
		'''
		if cleaner is not None:
			return (article for article in self.corpus if cleaner(article))
		return self.corpus

