import setuptools
import re
import os

import jenkins


JENKINS_ADDRESS = 'http://192.168.0.11:8080/'
JENKINS_USERNAME = os.environ.get('JENKINS_USERNAME')  # /etc/environment
JENKINS_PASSWORD = os.environ.get('JENKINS_PASSWORD')  # /etc/environment
JENKINS_JOB_NAME = 'Package_YahooFinanceDashboard'


here = os.path.abspath(os.path.dirname(__file__))
PKG_NAME = os.path.basename(here).split(r'_')[1]  # this will only work on Jenkins, where the cwd (job
                                                  # name) always has the format "Action_Pkgname"


with open("README.md", "r") as fh:
    long_description = fh.read()


def _find_in_file(file_path, search_str='__version__'):
    """Finds in a file a variable equaling a string of the type
    'search_str = "xxxx" '

    Parameters
    ----------
    init_path : str
        path to the file to search
    search_str : str
        variable name to search on file

    Returns
    -------
    found variable content

    Raises
    ------
    RuntimeError : in case passed string followed by content is not found in file
    """
    with open(file_path) as ip:
        __init_file__ = ip.read()

    match = re.search(r"^{}\s*=\s*['\"]([^'\"]*)['\"]".format(search_str), __init_file__, re.M)
    if match:
        return match.group(1)

    raise RuntimeError("Unable to find version string.")


def get_next_jenkins_build():
    """returns the next jenkins build number of the given job

    Returns
    -------
    build number : int
    """
    jenkins_server = jenkins.Jenkins(JENKINS_ADDRESS, username=JENKINS_USERNAME, password=JENKINS_PASSWORD)
    info = jenkins_server.get_job_info(JENKINS_JOB_NAME)

    last_build = info.get('lastCompletedBuild').get('number')

    return last_build + 1


def get_current_pkg_version():
    """Returns the current package version my merging the major.minor
    values of the package __init__ file with the last build number of the
    packaging Jenkins Job

    Returns
    -------
    full_version : str
        current pkg version id in the form <major>.<minor>.<build_id>
    """
    current_major_minor = _find_in_file(os.path.join(here, PKG_NAME, '__init__.py'))
    last_jenkins_build_num = get_next_jenkins_build()

    full_version = f'{current_major_minor}.{last_jenkins_build_num}'

    return full_version


setuptools.setup(
    name=PKG_NAME,
    version=get_current_pkg_version(),
    author="Daniel Moseguí González",
    author_email="d.mosegui@gmail.com",
    description="API for accessing, synchronizing, managing locally and plotting Yahoo financial data",
    # long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mosegui/YahooFinanceDashboard",
    license='BSD3',
    packages=setuptools.find_packages(),
    install_requires=[
        "yahoofinancials",
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)