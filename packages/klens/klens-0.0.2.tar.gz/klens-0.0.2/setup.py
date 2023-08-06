import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="klens",
    version="0.0.2",
    author="azohra",
    author_email="admin@azohra.com",
    description="Simple wrapper around kubectl",
    url="https://github.com/azohra/klens",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
      'console_scripts': [
          'klens=klens:main'
      ]
    }
)