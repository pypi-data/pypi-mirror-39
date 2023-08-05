import setuptools

CLASSIFIERS = [
    'Environment :: Web Environment',
    'Framework :: Django',
    'Framework :: Django :: 2.0',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
]
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-user-settings",
    version="0.0.5",
    author="viethq.lucidfoundry",
    author_email="viet.hoang@lucidfoundry.com",
    description="Enable settings for each user",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",  # TODO add github url here
    packages=setuptools.find_packages(),
    classifiers=CLASSIFIERS
)
