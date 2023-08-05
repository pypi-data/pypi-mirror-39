# mo-fabric

A façade atop [fabric](http://www.fabfile.org/)

## Overview

I have revisited [Fabric](http://www.fabfile.org/) (September 2018) to find it can handle multiple threads and multiple connections. This makes all my automation faster!

Like with most APIs, I made a façade because Fabric is not congruent to my own programming conventions. This is not bad, just different: The domain I work in is slightly different than what the Fabric developers expect. 

Here are the differences:

* All `stdout` and `strerr` from the remote machine is annotated, and shunted, the the local logging module.
* A few convenience methods are added:
  * `conn.exists(path)` - to test if a remote file exists
  * `with conn.warn_only():` - context manager if you do not care if your commands fail
  * `get(remote, local)` - allows you to use tilde (`~`) on Windows to refer to home directory
  * `put(local, remote, use_sudo=False)` - same as `get` plus the ability to upload as root
  * `sudo(command)` works with the `cd()` context manager
* Added `Result.__contains__()` so checking for patterns in command output is simpler
