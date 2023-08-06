import setuptools
import os

if os.environ.get('CI_COMMIT_TAG'):
  version = os.environ['CI_COMMIT_TAG']
elif os.environ.get('CI_JOB_ID'):
  version = os.environ.get('CI_JOB_ID')
else:
  version = '999'

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="yapij-py",
  version=version,
  author="Michael Wooley",
  author_email="michael.wooley@us.gt.com",
  description="Python-side of YAPIJ js-to-python interpreter.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/michaelwooley/yapij",
  packages=setuptools.find_packages(),
  python_requires='>=3.5',
  classifiers=[
    'Development Status :: 3 - Alpha',
    "Programming Language :: Python :: 3.7",
    "Operating System :: OS Independent",
  ],
  install_requires=['dill',
'traitlets',
'typing',
'msgpack_python',
'pyzmq'
]
)
