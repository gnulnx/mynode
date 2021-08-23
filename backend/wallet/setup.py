import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    # name="example-pkg-YOUR-USERNAME-HERE", # Replace with your own username
    # version="0.0.1",
    # author="John Furr",
    # author_email="john.furr@gmail.com",
    description="A simple bitcoin wallet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "jfurr=test:main",
        ],
    },
    # classifiers=[
    #     "Programming Language :: Python :: 3",
    #     "License :: OSI Approved :: MIT License",
    #     "Operating System :: OS Independent",
    # ],
    # python_requires='>=3.6',
)
