from setuptools import setup, find_packages

setup(
    name="parrot-terminal",
    version="v0.1.1",
    author="Tuan Nguyen",
    author_email="tuan.nguyenviet271@gmail.com",
    description="PARTY OR DIE",
    url="",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        parrot=parrot.cli:cli
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)