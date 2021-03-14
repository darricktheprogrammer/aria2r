import setuptools

import aria2r

setuptools.setup(
	name="aria2r",
	version=aria2r.__version__,
	url="https://github.com/darricktheprogrammer/aria2r",

	author="Darrick Herwehe",
	author_email="darrick@exitcodeone.com",

	description="Placeholder text for short description",
	long_description=open('README.md').read(),
	license='MIT',

	packages=setuptools.find_packages(),

	install_requires=[],

	classifiers=[
		'Development Status :: 2 - Pre-Alpha',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.6',
	],
)
