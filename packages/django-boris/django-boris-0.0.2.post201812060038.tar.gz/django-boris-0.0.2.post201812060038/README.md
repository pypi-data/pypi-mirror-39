## Boris

Boris* is a simple django app that can be used for storing the results
of crawled web pages and, more importantly, allows you to create custom
spider classes which can provide site- or url- specific content extraction.

Boris is one of the django applications developed for the nofollow.io
project. Currently the only spider implemented is the
`ReadabilitySpider`, which extracts the content from the url using
[Python's port of Readability project](https://pypi.org/project/readability-lxml/)

Due to the fact that all of the crawling and content processing is
done out of the request-response cycle, this app does not provide any
view, only celery tasks.


