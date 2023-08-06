import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='autodiff-py',
	version='1.0',
	description='Automatic Differentiation package',
	author='Ellie Han, Julien Laasri, Brian Lin, Bhaven Patel',
	long_description=long_description,
	long_description_content_type="text/markdown",
	packages=['autodiff'],
	install_requires=[
	  'numpy',
	  'scipy',
	],
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	url="https://github.com/cs207FinalProjectGroup/cs207-FinalProject",
	license="MIT",
)
