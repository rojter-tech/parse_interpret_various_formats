import setuptools
from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
        name='parse_interpret_various_formats',
        version='0.0.1',
        description='Parsing and interpret various formats and contents',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/rojter-tech/parse_interpret_various_formats',
        author='Daniel Rickard Reuter',
        author_email='dreuter@kth.se',
        classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        ],
        keywords='parse word setuptools development',
        package_dir={'': 'src'},
        packages=find_packages(where='src'),
        python_requires='!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
        install_requires=['pandas'],
        extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
        },
        package_data={
        'sample': ['package_data.dat'],
        },
        data_files=[('my_data', ['data/data_file'])],
        entry_points={  # Optional
        'console_scripts': [
            'sample=sample:main',
        ],
        },
        project_urls={  # Optional
        'Bug Reports': 'https://github.com/rojter-tech/parse_interpret_various_formats/issues',
        'Authors Web': 'https://www.rojter.tech',
        'Source': 'https://github.com/rojter-tech/parse_interpret_various_formats/',
        },
)
