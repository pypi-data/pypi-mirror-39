import setuptools

setuptools.setup(
    name="socialknife",
    version="0.0.1",
    author="Eliseo Martelli",
    author_email="me@eliseomartelli.it",
    description="Socialblade api wrapper",
    long_description="Socialblade api wrapper",
    install_requires=['aiohttp', 'async_timeout'],
    long_description_content_type="text/markdown",
    url="https://github.com/eliseomartelli/SocialKnife",
    packages=setuptools.find_packages()
)