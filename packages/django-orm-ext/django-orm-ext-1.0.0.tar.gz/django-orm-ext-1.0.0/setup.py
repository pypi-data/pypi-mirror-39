# coding:utf-8
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-orm-ext",
    version="1.0.0",
    author="@neoctobers",
    author_email="neoctobers@gmail.com",
    description="A Python list extension.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/neoctobers/py_django_orm_ext",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
    ],
)
