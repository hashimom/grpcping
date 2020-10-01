from setuptools import find_packages, setup

setup(
    name='grpcping',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/hashimom/grpcping',
    entry_points={
        "console_scripts": [
            "grpcping = grpcping.ping:main",
        ]
    },
    license='MIT',
    author='Masahiko Hashimoto',
    author_email='hashimom@geeko.jp',
    description=''
)
