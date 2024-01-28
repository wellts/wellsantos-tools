import pathlib
from setuptools import setup, find_packages


setup(
    name='wellsantos-tools',
    author='Wellington Tadeu dos Santos',
    author_email='wellsantos@wellsantos.com',
    version='1.0.1',
    description='Simple wrappers for Dependency Injection and Hierarchical Settings',
    long_description=(pathlib.Path(__file__).parent / 'README.md').read_text(),
    long_description_content_type='text/markdown',
    url='https://github.com/wellts/wellsantos-tools',
    packages=find_packages(),
    install_requires=[
        'pydantic>=2.5.2',
        'pydantic_settings>=2.1.0',
    ],
    license='MIT',
    python_requires=">=3.10",
)
