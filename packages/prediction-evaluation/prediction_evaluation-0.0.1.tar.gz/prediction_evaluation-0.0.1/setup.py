from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()
with open("requirements.txt") as f:
	required = f.read().splitlines()

setup(
name = "prediction_evaluation",
version="0.0.1",
description = "evaluation of prediction of binary, multiclass and regression",
long_description= readme,
author = "Xinyu Zhang, Yijia Chen, Xiaochi Ge",
author_email = "mandy_zhang512@gwu.edu",
url = "https://github.com/MandyZhangxy/DATS6450-final-project.git",
license = "GNU",
classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
],
keywords = "binary classification, regression, multiclass, evaluation",
install_requires = required
#package_data = {
#    "sample_data": ["data/"]
#}
)
