from setuptools import setup, find_packages
setup(
    name='hscraper',
    version='1.1.3',
    description='A tool to rip galleries from ehentai, r34.xxx, danbooru.donmai and hitomi.la',
    url='https://github.com/XrossFox/hscraper',
    author='XrossFox',
    author_email='warhead_1090@hotmail.com',
    license='MIT',
    packages=find_packages(exclude=(["*.tests", "*.tests.*", "tests.*", "tests"])),
    install_requires=[
        'beautifulsoup4>=4.6.3',
        'requests>=2.19.1',
        'click>=6.7',
    ],
    entry_points={
        'console_scripts': [
            'hscraper = hscraper.h_core:clickerino'
        ]
    },
)