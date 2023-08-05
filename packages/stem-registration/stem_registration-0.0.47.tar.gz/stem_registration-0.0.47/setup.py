from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="stem_registration",
    version="0.0.47",
    author="Dmitry Shevelev",
    author_email="shevelev.dmitriy@stemsc.com",
    description="A small registration package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.stemsc.com/shevelev/registration",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'django>=1.11,<2',
        'Pillow>=5.3.0',
        'django-registration-redux>=2.4',
        'django-bootstrap4>=0.0.6',
        'django-cities-light>=3.5.0',
        'django-select2>=6.3.1',
    ]
)
