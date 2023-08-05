from setuptools import setup, find_packages

setup(
    name='django-test-utils3',
    version='0.11.25',
    packages=find_packages(),
    author='Jon Froiland',
    author_email='jon@crowdkeep.com',
    description='A package to help testing in Django',
    long_description='Using 2to3, refactored code for Python3. Version references <version>.<month>.<change>',
    long_description_content_type='text/markdown',
    url='https://github.com/phroiland/django-test-utils',
    download_url='https://github.com/phroiland/django-test-utils',
    test_suite='test_project.run_tests.run_tests',
    include_package_data=True,
    install_requires=[
        'BeautifulSoup4',
        'twill3', 'django', 'six'
    ]
)
