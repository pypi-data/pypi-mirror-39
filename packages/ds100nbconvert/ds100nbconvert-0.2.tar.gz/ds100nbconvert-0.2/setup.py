from setuptools import setup

setup(name='ds100nbconvert',
      version='0.2',
      description='dsin100days custom nbconvert, copied from nbextensions',
      url='',
      install_requires=['nbconvert'],
      author='dinesh',
      author_email='dinesh@micropyramid.com',
      license='LICENCE',
      packages=['ds100nbconvert'],
      zip_safe=False,
      entry_points = {
          'nbconvert.exporters': [
              'html_embed = ds100nbconvert:EmbedHTMLExporter',
          ],
      })
