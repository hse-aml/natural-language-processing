#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


def download_github_code(path):
    filename = path.rsplit("/")[-1]
    os.system("wget https://raw.githubusercontent.com/hse-aml/natural-language-processing/master/{} -O {}".format(path, filename))


def setup_common():
    download_github_code("common/requirements_colab.txt")
    download_github_code("common/download_utils.py")
    download_github_code("common/tqdm_utils.py")
    download_github_code("common/__init__.py")
    os.system("mkdir common")
    os.system("mv download_utils.py tqdm_utils.py __init__.py common/")
    os.system("mv requirements_colab.txt common/")

    os.system("pip install -r common/requirements_colab.txt --force-reinstall")


def setup_starspace():
    if not os.path.exists("/usr/local/bin/starspace"):
        os.system("wget https://dl.bintray.com/boostorg/release/1.63.0/source/boost_1_63_0.zip")
        os.system("unzip boost_1_63_0.zip && mv boost_1_63_0 /usr/local/bin")
        os.system("git clone https://github.com/facebookresearch/Starspace.git")
        os.system("cd Starspace && make && cp -Rf starspace /usr/local/bin")


def setup_week1():
    setup_common()
    download_github_code("week1/grader.py")
    download_github_code("week1/metrics.py")


def setup_week2():
    setup_common()
    download_github_code("week2/evaluation.py")


def setup_week3():
    setup_common()
    download_github_code("week3/grader.py")
    download_github_code("week3/util.py")
    setup_starspace()


def setup_week4():
    setup_common()


def setup_project():
    setup_common()
    download_github_code("week5/dialogue_manager.py")
    download_github_code("week5/utils.py")
    setup_starspace()


def setup_honor():
    setup_common()
    download_github_code("honor/datasets.py")
    download_github_code("honor/example.py")
    download_github_code("honor/download_cornell.sh")
    download_github_code("honor/download_opensubs.sh")
