from setuptools import setup, find_packages

setup(
    name='frcrawler',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click', 'beautifulsoup4', 'requests', 'terminaltables'
    ],
    entry_points='''
        [console_scripts]
        yekki=frcrawler.main:cli
    ''',
)
