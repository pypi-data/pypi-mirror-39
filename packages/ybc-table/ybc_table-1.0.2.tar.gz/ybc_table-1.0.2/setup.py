from distutils.core import setup

setup(name='ybc_table',
      version='1.0.2',
      description='Ascii Table',
      long_description='Create Ascii Table',
      author='zhangyun',
      author_email='zhangyun@fenbi.com',
      keywords=['pip3', 'table', 'python3','python','ascii table'],
      url='http://pip.zhenguanyu.com/',
      packages=['ybc_table'],
      package_data={'ybc_table': ['*.py']},
      license='MIT',
      install_requires=['ybc_exception', 'terminaltables'],
      )
