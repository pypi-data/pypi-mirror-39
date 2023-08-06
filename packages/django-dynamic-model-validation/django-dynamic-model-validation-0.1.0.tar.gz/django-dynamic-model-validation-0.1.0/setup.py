import os
from io import open

from setuptools import find_packages, setup

with open('README.rst', 'r', encoding='utf-8') as f:
    readme = f.read()

install_requires = ['Django>=1.11.10', 'future==0.17.1']

test_requires = [
    'tox==2.9.1',
    'pytest-django==3.4.4',
    'pluggy>=0.7',
    'mock==2.0.0',
    'codacy-coverage==1.3.10',
]

deploy_requires = [
    'bumpversion==0.5.3',
]

lint_requires = [
    'flake8==3.4.1',
    'yamllint==1.10.0',
    'isort==4.2.15',
]

local_dev_requires = [
    'pip-tools==3.1.0',
]

extras_require = {
    'development': [
        local_dev_requires,
        install_requires,
        test_requires,
        lint_requires,
    ],
    'test': test_requires,
    'lint': lint_requires,
    'deploy': deploy_requires,
}

BASE_DIR = os.path.dirname(__file__)
README_PATH = os.path.join(BASE_DIR, 'README.md')

LONG_DESCRIPTION_TYPE = 'text/markdown'
if os.path.isfile(README_PATH):
    with open(README_PATH) as f:
        LONG_DESCRIPTION = f.read()
else:
    LONG_DESCRIPTION = ''

VERSION = (0, 1, 0)

version = '.'.join(map(str, VERSION))

setup(
    name='django-dynamic-model-validation',
    version=version,
    description='Extra django model validation.',
    python_requires='>=2.6',
    long_description=readme,
    author='Tonye Jack',
    author_email='jtonye@ymail.com',
    maintainer='Tonye Jack',
    maintainer_email='jtonye@ymail.com',
    url='https://github.com/jackton1/django-dynamic-model-validation.git',
    license='MIT/Apache-2.0',
    keywords=[
        'django', 'model validation', 'django models', 'django object validation',
        'field validation', 'conditional validation', 'cross field validation',
        'django validation', 'django validators', 'django custom validation',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    install_requires=install_requires,
    tests_require=['coverage', 'pytest'],
    extras_require=extras_require,
    packages=find_packages(exclude=['test*', '*_test', 'demo'], include=['dynamic_validator']),
)
