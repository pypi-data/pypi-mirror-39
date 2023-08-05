from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='yoyopkg',
    version='2.5',
    packages=['src', 'src.core', 'src.stores', 'src.modules', 'src.plugins'],
    url='https://github.com/ethanquix/yoyo',
    license='MIT',
    author='dwyzlic',
    author_email='dimitriwyzlic@gmail.com',
    description='A modular package manager',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
   'colorama',
   'requests'
    ],

    include_package_data=True,
    entry_points={
        'console_scripts': [
            'yoyo=src:main',
        ],
    },

)
