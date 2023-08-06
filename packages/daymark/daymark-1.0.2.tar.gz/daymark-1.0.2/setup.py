from distutils.core import setup

setup(name = 'daymark',
	version = '1.0.2',
	scripts =['daymark'],
	licence = 'MIT',
	description = 'daymark is a helper package.',
	author = 'Samarthya Choudhary',
	author_email = 'samarthyachoudhary7@gmail.com',
	url = 'https://gitlab.com/aman.indshine/lighthouse-function-helper.git',
	install_requires =['requests', 'redis', 'boto'],
	classifiers=['Development Status :: 3 - Alpha', 'Intended Audience :: Developers', 'Topic :: Software Development :: Build Tools', 'License :: OSI Approved :: MIT License'])