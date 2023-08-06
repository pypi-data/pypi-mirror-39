from setuptools import setup

# from pip.req import parse_requirements


# parse_requirements() returns generator of pip.req.InstallRequirement objects
# install_reqs = parse_requirements('requirements-prod.txt')

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
# reqs = [str(ir.req) for ir in install_reqs]


setup(name='dict_pretty_printer',
      version='0.1',
      description=('a good description for dict pretty printer'),
      url='https://github.com/JackonYang/dict-pretty-printer',
      author='Jackon Yang',
      author_email='i@jackon.me',
      license='MIT',
      packages=['dict_pretty_printer'],
      package_dir={'': 'src'},
      # install_requires=reqs,
      zip_safe=False)
