from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='webbrowserdownloader',
      version='0.1',
      description='webbrowserdownloader is a wrapper for selenium browser',
      long_description=readme(),
	  classifiers = ['Programming Language :: Python',
					 'License :: OSI Approved :: MIT License',
					 'Operating System :: MacOS',
                     'Operating System :: Unix',
                     'Operating System :: Microsoft :: Windows',
					 'Development Status :: 4 - Beta',
					 'Intended Audience :: Developers',
					 'Topic :: Internet :: WWW/HTTP',
                     'Topic :: Internet :: WWW/HTTP :: Browsers',
					 'Topic :: Internet :: WWW/HTTP :: Site Management',
	  ],
      keywords='webbrowserdownloader selenium browser downloder web extraction parsing scraping mining',
      url='http://github.com/devStarkes/webbrowserdownloader',
      author='Starkes org.',
      author_email='devStarkes@gmail.com',
      license='MIT',
      packages=['webbrowserdownloader'],
      install_requires=[
          'validators',
          'selenium',
          'pyvirtualdisplay',
          'pillow',
      ],
      include_package_data=True,
      zip_safe=False)
