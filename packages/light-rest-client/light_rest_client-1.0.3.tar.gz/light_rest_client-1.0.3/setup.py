from distutils.core import setup

with open('requirements.txt') as stream:
    install_requires = stream.read()

setup(
    name="light_rest_client",
    version="1.0.3",
    packages=["light_rest_client"],
    install_requires=install_requires,

    url="https://github.com/mediascopegroup/light_rest_client/",
    description="A very lightweight REST client for Python.",
    long_description=open("README.md").read(),

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Build Tools",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ],

    author="Kacper Duras",
    author_email="kacper.duras@mediascope.group"
)
