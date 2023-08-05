from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='GraphiPy',
    version='0.0.2b',
    description='A Universal Social Data Extractor',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    author='Shobeir Fakhraei',
    url='https://github.com/shobeir/GraphiPy',
    author_email='shobeir@gmail.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=False,
    zip_safe=True,
    install_requires=['pytumblr>=0.0.8', 'httplib2>=0.11.3', 'google-api-python-client>=1.7.4',
    'google-auth>=1.5.1', 'google-auth-oauthlib>=0.2.0', 'google-auth-httplib2>=0.0.3',
    'oauth2client>=4.1.3', 'facebook-sdk>=3.0.0', 'pandas>=0.23.0', 'py2neo>=4.1.0',
    'networkX>=2.2']
)
