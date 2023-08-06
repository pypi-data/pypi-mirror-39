import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()


setuptools.setup(
    name = 'crazybee',
    version = '0.0.1',
    author = 'handaochang',
    author_email = 'hanleilei@outlook.com',
    description = 'crazybee to extract info from yanxuan website',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com',
    packages = setuptools.find_packages(),
    classifiers = [
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],

    install_requires = ['bs4', 'requests', 'xlwt', 'retrying'],
)