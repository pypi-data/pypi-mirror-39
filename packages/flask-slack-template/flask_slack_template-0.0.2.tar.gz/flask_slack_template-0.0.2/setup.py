import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flask_slack_template",
    version="0.0.2",
    author="Jamie WU",
    author_email="jamiewu2@illinois.com",
    description="A light decorator around flask and slack to remove the boilerplate for handling Slack slash commands",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jamiewu2/flask-slack-template",
    packages=setuptools.find_packages(),
    install_requires=[
        'Flask',
        'slackclient',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)