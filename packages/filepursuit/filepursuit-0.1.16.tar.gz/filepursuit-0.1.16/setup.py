import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="filepursuit",
    version="0.1.16",
    author="JCatrielLopez",
    author_email="jcatriel.lopez@gmail.com",
    description="A python tool for scraping and downloading files from filepursuit",
    entry_points={
        'console_scripts': ['filepursuit=filepursuer.filepursuer:main']
    },
    packages=["filepursuer"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/JCatrielLopez/pylocate",
    python_requires='>=3',
    install_requires=[
          'requests',
          'bs4',
          'requests_html',
          'clint'
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)