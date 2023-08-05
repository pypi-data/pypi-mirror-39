import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="brickbreaker",
    version="0.0.8",
    author="Brent Leeper, Joshua Green",
    author_email="bleeper@patriots.uttyler.edu, jgreen32@patriots.uttyler.edu",
    description="A Breakout clone with pygame.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    include_package_data = True,
    packages=setuptools.find_packages(),
    # data_files = [
        # ('assets',['sprites/ball.gif']),
    # ],
    classifiers=[],
    install_requires=[
          'pygame',
      ],
    entry_points={
        "console_scripts": [
            "brickbreaker=brickbreaker.__main__:main",
        ]
    },
)
