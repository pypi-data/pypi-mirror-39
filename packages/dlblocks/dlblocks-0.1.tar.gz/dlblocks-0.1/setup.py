from setuptools import find_packages, setup
setup(name="dlblocks",
      version="0.1",
      description="Contains a lot of util libraries used across projects",
      author="John Doe",
      author_email='authoremail@mail.com',
      platforms=["any"],  # or more specific, e.g. "win32", "cygwin", "osx"
      license="BSD",
      url="http://github.com/github/repo",
      packages=find_packages(),
      )