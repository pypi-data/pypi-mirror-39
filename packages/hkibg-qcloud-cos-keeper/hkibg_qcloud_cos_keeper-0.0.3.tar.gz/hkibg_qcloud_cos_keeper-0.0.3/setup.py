import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hkibg_qcloud_cos_keeper",
    version="0.0.3",
    author="Luk Chun Pong",
    author_email="pongluk@tencent.com",
    description="a qcloud cos file/log keeper for hkibg",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/pongpersonal/hkibg_qcloud_cos_keeper/src/master/",
    packages=setuptools.find_packages(),
    install_requires=[
        "cos-python-sdk-v5==1.5.5",
        "pytz",
        "tzlocal"
    ],
    scripts=[
        "bin/qcloud_cos_keeper_file_cleaner.py",
        "bin/qcloud_cos_keeper_file_rotator.py",
        "bin/qcloud_cos_keeper_file_uploader.py"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
