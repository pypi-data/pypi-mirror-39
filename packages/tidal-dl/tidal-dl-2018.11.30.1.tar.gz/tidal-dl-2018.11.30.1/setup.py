from setuptools import setup, find_packages

setup(
    name = 'tidal-dl',
    version='2018.11.30.1',
    license = "MIT Licence",
    description = "Tidal Music Download.",

    author = 'YaronH',
    author_email = "yaronhuang@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires=["aigpy>=1.0.0.12", "requests", "ffmpeg", "futures"],

    entry_points={'console_scripts': [
        'tidal-dl = tidal_dl:main', ]}
)
