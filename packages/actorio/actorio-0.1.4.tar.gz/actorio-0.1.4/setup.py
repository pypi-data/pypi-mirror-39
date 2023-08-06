import os

from setuptools import setup, find_packages

base_dir = os.path.dirname(__file__)

with open(os.path.join(base_dir, "README.md")) as f:
    long_description = f.read()

setup(
        name="actorio",
        description="A simple actor framework for asyncio",
        long_description=long_description,
        long_description_content_type="text/markdown; charset=UTF-8; variant=GFM",
        url="https://gitlab.com/python-actorio/actorio",
        use_scm_version=True,
        setup_requires=['setuptools_scm'],
        author="Jonathan GAYVALLET",
        author_email="jonathan.mael.gayvallet@gmail.com",
        license="MIT",
        packages=find_packages(exclude=("tests",)),
        install_requires=[
            "pytz>=2018.7"
        ],
        python_requires=">=3.6",
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: POSIX :: Linux",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: POSIX :: BSD",
            "Operating System :: Microsoft :: Windows",
            "Programming Language :: Python :: Implementation :: CPython",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
        ],
)
