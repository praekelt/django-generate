from setuptools import setup, find_packages

setup(
    name='django-generate',
    version='dev',
    description='Django slightly smarter than fixtures content generation app.',
    author='Praekelt Consulting',
    author_email='dev@praekelt.com',
    url='https://github.com/praekelt/django-generate',
    packages = find_packages(),
    include_package_data=True,
)
