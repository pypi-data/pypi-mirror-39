from setuptools import setup, find_packages

setup(
    name='flask-sharething',
    version='0.2.5',
    url='https://github.com/qileroro/flask-sharething/',
    license='Apache License, Version 2.0',
    author='Kevin Wong',
    author_email='qileroro@qq.com',
    packages=find_packages(),
    install_requires=[
    ],
    description='Share extensions in multiple flask sub-applications',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.7'
    ],
)
