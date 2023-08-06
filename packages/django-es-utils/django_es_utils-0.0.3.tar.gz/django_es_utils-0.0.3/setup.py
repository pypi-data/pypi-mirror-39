from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="django_es_utils",
    version="0.0.3",
    url="https://github.com/Edraak/django-es-utils",
    description="Elasticsearch utilities for Django projects.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Fahmi Al-Najjar",
    author_email="fahmi.najjar@gmail.com",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "Django==1.8",
        "requests",
        "urllib3>= 1.21.1, < 1.22",
        "elasticsearch==6.3.0",
        "elasticsearch_dsl==6.2.1",
        "ElasticMock==1.3.2"
    ],
)
