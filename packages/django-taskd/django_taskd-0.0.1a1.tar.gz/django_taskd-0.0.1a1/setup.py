try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

README = open('README.md').read()
# LICENSE = open('LICENSE.md').read()

setup(
    name="django_taskd",
    version="0.0.1a1",
    url="https://github.com/Colorless-Green-Ideas/django-taskd",
    author="amelia sabine",
    author_email="amelia.sabine@getpizza.cat",
    license="AGPLv3",
    zip_safe=False,
    packages=find_packages(exclude=["tests", "test_utils"]),
    description="""A taskd implementation for the Django web framework. Enables django applications to easily integrate
        tasks with Taskwarrior.""",
    long_description=README,
    long_description_content_type="text/markdown",
    install_requires=["django", "taskc", "requests"],
    classifiers=[
        "Framework :: Django",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
