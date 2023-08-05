from pathlib import Path
from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = []

setup(
    name='naucse_render',
    version='0.0.0',
    author="Petr Viktorin",
    author_email='encukou@gmail.com',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Renderer for course materials",
    install_requires=requirements,
    license="MIT license",
    long_description=Path('README.md').read_text(encoding='utf-8'),
    include_package_data=True,
    packages=find_packages(),
    url='https://github.com/encukou/naucse_render',
    zip_safe=False,
)
