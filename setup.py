from importlib.metadata import entry_points
from setuptools import setup, find_namespace_packages

setup(name='personal_virtual_assistant',
      version='1.0.5.0',
      description='Personal virtual assistant (pva) for notes, addressbok, junk sorter.',
      url='https://github.com/DenysTantsiura/pva',
      author='Always on the right track team',
      author_email='ghost0002501@gmail.com',
      license='MIT',
      packages=find_namespace_packages(),
      install_requires=['colorama'],
      entry_points={'console_scripts': ['pva = pva.start:main']})
