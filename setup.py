from setuptools import setup, find_packages

setup(
    name="swhid-mkdocs-plugins",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "mkdocs>=1.0.0",
    ],
    entry_points={
        'mkdocs.plugins': [
            'unified_navbar = plugins.unified_navbar:UnifiedNavbarPlugin',
        ],
    },
)
