from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='webdownloader',
      version='0.1',
      description='webdownloader is a tool for web data extraction',
      long_description=readme(),
	  classifiers = ['Programming Language :: Python',
					 'License :: OSI Approved :: MIT License',
					 'Operating System :: OS Independent',
					 'Development Status :: 4 - Beta',
					 'Intended Audience :: Developers',
					 'Topic :: Internet :: WWW/HTTP',
					 'Topic :: Internet :: WWW/HTTP :: Site Management',
	  ],
      keywords='webdownloader downloder web extraction parsing scraping mining',
      url='http://github.com/devStarkes/webdownloader',
      author='Starkes org.',
      author_email='devStarkes@gmail.com',
      license='MIT',
      packages=['webdownloader'],
      install_requires=[
          'validators',
          'requests',
          'requests_html'
      ],
      include_package_data=True,
      zip_safe=False)
