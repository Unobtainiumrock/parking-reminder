from setuptools import setup, find_packages

setup(
    name="parking-reminder",
    version="0.1.0",  # Initial version
    description="A tool to set up parking reminders with cron jobs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Nicholas Fleischhauer",
    author_email="unobtainiumrock@gmail.com",
    url="https://github.com/Unobtainiumrock/parking-reminder",
    license="GPL-3.0",
    packages=find_packages(),
    include_package_data=True,  # Include non-Python files defined in MANIFEST.in
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version
    entry_points={
        "console_scripts": [
            "parking-reminder=parking_reminder.parking_reminder:main",  # Optional CLI entry point
        ],
    },
)
