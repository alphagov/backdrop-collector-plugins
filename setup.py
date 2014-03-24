from setuptools import setup, find_packages

setup(
    name='backdrop-collector-plugins',
    version="1.0.0",
    packages=["backdrop.collector.plugins"],
    namespace_packages=['backdrop', 'backdrop.collector'],

    # metadata for upload to PyPI
    author='Government Digital Service',
    author_email='',
    maintainer='Government Digital Service',
    # TODO(pwaller): url='https://github.com/alphagov/backdrop-ga-collector',

    description='backdrop-ga-collector-plugins: plugins for backdrop collectors',
    license='MIT',
    keywords='api data performance_platform google_analytics',

    setup_requires=['setuptools'],
)