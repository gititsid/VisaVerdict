from setuptools import find_packages, setup
from typing import List


with open("README.md", "r", encoding="utf-8") as long_desc_file:
    long_description = long_desc_file.read()

HYPHEN_E_DOT = '-e .'

SRC_REPO = "visa-verdict"
__version__ = "0.0.0"
AUTHOR_USER_NAME = "gititsid"
AUTHOR_EMAIL = "siddharth.iitp@gmail.com"
REPO_NAME = "VisaVerdict"


def get_requirements(file_path: str) -> List[str]:
    """
    This function will return the list of requirements.
    """
    with open(file_path) as req_file:
        requirements = req_file.readlines()
        requirements = [req.replace('\n', "") for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    return requirements


setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A Machine Learning project to predict the likelihood of US Visa approval",
    long_description=long_description,
    long_description_content="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=get_requirements(file_path='requirements.txt')
)
