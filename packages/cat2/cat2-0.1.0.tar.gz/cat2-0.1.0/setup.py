from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='cat2',
    version='0.1.0',

    description='Print file contents like a boss',
    long_description=readme(),
    long_description_content_type='text/markdown',

    url='https://github.com/arrrlo/cat2',
    licence='MIT',

    author='Ivan Arar',
    author_email='ivan.arar@gmail.com',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='cat, print, file, contents',

    packages=['cat2'],
    install_requires=[
        'click~=6.7',
        'colorama~=0.3',
        'db-transfer~=0.3.3',
        'requests~=2.18.4',
        'pyfiglet~=0.7.5',
        'termcolor~=1.1.0',
    ],
    entry_points={
        'console_scripts': [
            'cat2=cat2.cli:cli'
        ],
    },

    project_urls={
        'Source': 'https://github.com/arrrlo/cat2',
    },
)
