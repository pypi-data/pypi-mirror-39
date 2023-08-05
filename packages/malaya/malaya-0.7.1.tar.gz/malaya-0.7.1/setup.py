import os
from distutils.core import setup
from distutils import dir_util
from distutils import sysconfig
import setuptools
import atexit
from setuptools.command.install import install


def _post_install():
    print(
        'Please install keras-contrib, `pip install git+https://www.github.com/keras-team/keras-contrib.git`'
    )
    print(
        'Cudnn 7 and above seems has problem with Malaya fast-text models, we prefer to use Tensorflow Version 1.5 CUDA 8.0 Cudnn 5'
    )
    print(
        'You can simply downgrade by `pip uninstall tensorflow && pip install tensorflow==1.5`'
    )


class new_install(install):
    def __init__(self, *args, **kwargs):
        super(new_install, self).__init__(*args, **kwargs)
        atexit.register(_post_install)


__packagename__ = 'malaya'

setuptools.setup(
    name = __packagename__,
    packages = setuptools.find_packages(),
    version = '0.7.1',
    description = 'Natural-Language-Toolkit for bahasa Malaysia, powered by Deep Learning.',
    author = 'huseinzol05',
    author_email = 'husein.zol05@gmail.com',
    url = 'https://github.com/DevconX/Malaya',
    download_url = 'https://github.com/DevconX/Malaya/archive/master.zip',
    keywords = ['nlp', 'bm'],
    install_requires = [
        'xgboost==0.80',
        'sklearn',
        'scikit-learn==0.19.1',
        'requests',
        'fuzzywuzzy',
        'tqdm',
        'nltk',
        'unidecode',
        'tensorflow',
        'numpy',
        'scipy',
        'python-levenshtein',
        'pandas',
        'keras',
        'PySastrawi',
    ],
    cmdclass = {'install': new_install},
    classifiers = [
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Text Processing',
    ],
    long_description = open('readme-pypi.srt').read(),
)
