#!/usr/bin/env python3
"""
Setup configuration for EduScan Somalia deployment
"""

from setuptools import setup, find_packages

setup(
    name="eduscan-somalia",
    version="1.0.0",
    description="Learning Risk Assessment Application for Somalia",
    packages=find_packages(include=['utils', 'database']),
    include_package_data=True,
    package_data={
        '': ['*.txt', '*.md', '*.json', '*.pkl', '*.toml'],
        'data': ['*.pkl', '*.json'],
        '.streamlit': ['*.toml']
    },
    python_requires=">=3.11",
    install_requires=[
        "streamlit>=1.28.0",
        "pandas>=2.0.0", 
        "numpy>=1.24.0",
        "scikit-learn>=1.3.0",
        "plotly>=5.15.0",
        "psycopg2-binary>=2.9.0",
        "sqlalchemy>=2.0.0"
    ],
    entry_points={
        'console_scripts': [
            'eduscan-somalia=app_desktop:main',
        ],
    },
)