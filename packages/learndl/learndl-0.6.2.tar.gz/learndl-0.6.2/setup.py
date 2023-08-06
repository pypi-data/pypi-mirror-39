import setuptools

long_description = """
LearnDL: Deep Learning for beginners
written in Python and NumPy.

Just for learning Deep Learning.

LearnDL is compatible with Python 3.6
and is distributed under the Apache license 2.0.
"""

setuptools.setup(
    name="learndl",
    version="0.6.2",
    author="indeep",
    author_email="qianshuai2018@aliyun.com",
    description="Deep Learning for beginners",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mrcorecoder/learndl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
