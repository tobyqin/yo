from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name='my-yo',
    version='0.1',
    description="Yo, a powerful self customizable cli. (https://github.com/tobyqin/yo)",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Toby Qin",
    author_email='toby.qin@live.com',
    url='https://github.com/tobyqin/yo',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'pyyaml'
    ],
    entry_points='''
        [console_scripts]
        yo=yo:cli
    ''',
)
