from setuptools import setup

setup(
    name='convertcurl',
    version='0.0.2',
    author='golmic',
    author_email='ljq0225@gmail.com',
    url='https://github.com/lujqme',
    description='把curl命令转换成requests或者scrapy的请求',
    packages=['convertcurl'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'convert=convertcurl:main'
        ]
    }
)
