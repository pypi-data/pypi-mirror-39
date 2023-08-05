# encoding: utf-8
from __future__ import unicode_literals
from setuptools import setup
setup(
    description="Thin facade over fabric",
    license="MPL 2.0",
    author="Kyle Lahnakoski",
    author_email="kyle@lahnakoski.com",
    long_description_content_type="text/markdown",
    include_package_data=True,
    classifiers=["Development Status :: 4 - Beta","Topic :: Software Development :: Libraries","Topic :: Software Development :: Libraries :: Python Modules","License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)"],
    install_requires=["fabric2","invoke","mo-dots>=2.20.18318","mo-files>=2.26.18331","mo-future","mo-kwargs","mo-logs","mo-math"],
    version="2.28.18331",
    url="https://github.com/klahnakoski/mo-fabric",
    zip_safe=False,
    packages=["mo_fabric"],
    long_description="# mo-fabric\n\nA façade atop [fabric](http://www.fabfile.org/)\n\n## Overview\n\nI have revisited [Fabric](http://www.fabfile.org/) (September 2018) to find it can handle multiple threads and multiple connections. This makes all my automation faster!\n\nLike with most APIs, I made a façade because Fabric is not congruent to my own programming conventions. This is not bad, just different: The domain I work in is slightly different than what the Fabric developers expect. \n\nHere are the differences:\n\n* All `stdout` and `strerr` from the remote machine is annotated, and shunted, the the local logging module.\n* A few convenience methods are added:\n  * `conn.exists(path)` - to test if a remote file exists\n  * `with conn.warn_only():` - context manager if you do not care if your commands fail\n  * `get(remote, local)` - allows you to use tilde (`~`) on Windows to refer to home directory\n  * `put(local, remote, use_sudo=False)` - same as `get` plus the ability to upload as root\n  * `sudo(command)` works with the `cd()` context manager\n* Added `Result.__contains__()` so checking for patterns in command output is simpler\n",
    name="mo-fabric"
)