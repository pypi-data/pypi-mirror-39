import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'py_flood',
    version = '0.0.2',
    author = 'Dane Morgan',
    author_email = 'danemorgan91@gmail.com',
    description = 'udp port flooding, use a cli or just its modules. Integrates with Bro (Zeek) to flood hosts according to their traffic',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/deadlift1226/py_flood',
    install_requires = ['joblib', 'bat', 'multiprocessing',], #3rd party pip packages
    packages = setuptools.find_packages(),
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

