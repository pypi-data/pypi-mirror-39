
from setuptools import setup, find_packages
import os

version = '0.1'
long_description = '\n'.join([
    open('README.rst').read()
    ])

setup(
    name='pygments_solarized_style',
    version=version,
    description='Pygments version of the Solarized theme.',
    long_description=long_description,
    keywords=['pygments', 'style', 'solarized', 'syntax highlighting'],
    author='Jason Xu',
    author_email='hongyi.xu@gmail.com',
    url='https://github.com/lordjx/pygments-solarized_style',
    license='MIT',
    packages=find_packages(),
    install_requires=['pygments >= 1.5'],
    entry_points="""
        [pygments.styles]
        solarizedlight=pygments_solarized_style.light:LightStyle
        solarizeddark=pygments_solarized_style.dark:DarkStyle
    """,
    zip_safe=False,
)
