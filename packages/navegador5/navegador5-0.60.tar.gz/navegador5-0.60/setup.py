from setuptools import setup, find_packages
setup(
      name="navegador5",
      version = "0.60",
      description="tools for http request",
      author="dapeli",
      url="https://github.com/ihgazni2/navegador5",
      author_email='terryinzaghi@163.com', 
      license="MIT",
      long_description = "refer to .md files in https://github.com/ihgazni2/navegador5",
      classifiers=[
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'Programming Language :: Python',
          ],
      packages= find_packages(),
      py_modules=['navegador5'], 
      )


# python3 setup.py bdist --formats=tar
# python3 setup.py sdist

