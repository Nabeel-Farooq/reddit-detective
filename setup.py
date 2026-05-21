from pathlib import Path

from setuptools import find_packages, setup

from reddit_detective import VERSION

BASE_DIR = Path(__file__).parent

README = (BASE_DIR / "README.md").read_text(
    encoding="utf-8"
)

setup(
    name="reddit_detective",
    version=VERSION,

    author="Ümit Kaan Usta",
    author_email="u.kaanusta@gmail.com",

    description="Play detective on Reddit",
    long_description=README,
    long_description_content_type="text/markdown",

    url="https://github.com/umitkaanusta/reddit-detective",

    license="MIT",

    packages=find_packages(
        include=[
            "reddit_detective",
            "reddit_detective.*",
        ]
    ),

    include_package_data=True,

    python_requires=">=3.8",

    install_requires=[
        "praw>=7.7.0",
        "neo4j>=5.0.0",
    ],

    keywords=[
        "reddit",
        "reddit-analysis",
        "analytics",
        "neo4j",
        "graph",
        "social-network",
        "data-analysis",
        "social-media",
        "information-analysis",
        "campaign-analysis",
        "influencer-analysis",
        "comment-analysis",
        "elections",
        "news",
        "politics",
    ],

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",

        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Sociology",
        "Topic :: Education",

        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],

    project_urls={
        "Source": "https://github.com/umitkaanusta/reddit-detective",
        "Issues": "https://github.com/umitkaanusta/reddit-detective/issues",
    },
)
