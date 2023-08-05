from distutils.core import setup


setup(
  name='ybc_china',
  packages=['ybc_china'],
  package_data={'ybc_china':['data/*', '*.py']},
  version='1.0.9',
  description='Get ALL Citys',
  long_description='Get ALL Citys',
  author='zhangyun',
  author_email='zhangyun@fenbi.com',
  keywords=['pip3', 'python3', 'python', 'citys'],
  license='MIT',
  install_requires=['ybc_exception']
)
