gpuview
=======

[![pypi](https://img.shields.io/pypi/v/gpuview.svg?maxAge=86400)][pypi_gpuview]
[![Build Status](https://travis-ci.org/fgaim/gpuview.svg?branch=master)](https://travis-ci.org/fgaim/gpuview)
[![license](https://img.shields.io/github/license/fgaim/gpuview.svg?maxAge=86400)](LICENSE)


GPU is an expensive resources and deep learning practitioners generally have to monitor the
health and usage of their GPUs, such as the temperature, memory, utilization, and process users. 
This can be done with tools like `nvidia-smi` and `gpustat` from the terminal or command-line.  

However, often times, it is not convenient to `ssh` into servers to just check the status,
especially for a long running training that could last from hours to days. `gpuview` is meant
to serve this exact purpose, it is lightweight web dashboard that runs on top of 
[`gpustat`][repo_gpustat].  

With `gpuview` one can monitor GPUs on the go through a web browser. What is more, multiple 
servers can be registered into one dashboard and their stats is aggregated and accessible from
one place.

![Screenshot: gpuview -cp](imgs/screenshot.png)

> With `gpuview` you get the latest version of `gpustat` installed from `pypi`, 
so all the usual commands are directly available from the terminal. 
See `gpustat -h` and `gpuview -h` for all command-line options.


Setup
-----

Install from [PyPI][pypi_gpuview]:

```
pip install gpuview
```

[or] Install directly from repo:

```
pip install git+https://github.com/fgaim/gpuview.git@master
```


Usage
-----

Once `gpuview` is installed, it can be started as follows:
```
$ gpuview start --safe-zone
```
This will start the dasboard at `http://0.0.0.0:9988`.


By default, `gpuview` listens to IP `0.0.0.0` and port `9988`, but these can be changed using `--host` and `--port`. The `safe-zone` option implies reporting all detials including user names, but it can be turned off for security reasons.


Execute `gpuview -h` to see runtime options.

* `start`              : Start dashboard server
  * `--host`           : Name or IP address of host (default: 0.0.0.0)
  * `--port`           : Port number to listen to (default: 9988)
  * `--safe-zone`      : Safe to report all details including user names
  * `--exclude-self`   : Don't report to others but to self dashboard
  * `-d`, `--debug`    : Run server in debug mode (for developers)
* `add`                : Add a GPU host to dashboard
  * `--url`            : URL of host [IP:Port], eg. X.X.X.X:9988
  * `--name`           : Optional readable name for the host, eg. Node101
* `remove`             : Remove a registered host from dashboard
  * `--url`            : URL of host to remove, eg. X.X.X.X:9988
* `-v`, `--version`    : Print versions of `gpuview` and `gpustat`
* `-h`, `--help`       : Print help for command-line options


### Run as Service

To permanently run `gpuview` it needs to be started as a background service. This can be done using `nohup` and `&` as follows:

```
sudo nohup gpuview start --safe-zone &
```

Better way of handling this is coming soon...


### Monitoring multiple hosts

To aggregate the stats of multiple machines, they can be registered to one dashboard using their address and the port number running `gpustat`.

Add a host as follows:
```
gpuview add --url <ip:port> --name <name>
```

Remove a registered host as follows:
```
gpuview remove --url <ip:port> --name <name>
```

> Note: `gpuview` should be run in all hosts in addition to the controller, which by itself can be a none GPU machine.


etc
---

Helpful tips related to the underlying performance are available at the [`gpustat`][repo_gpustat] repo.


For the sake of similicity, `gpuview` does not have user authentication feature, therefore, by default it does not report sensitive details such as user and process names as security measure. However, the service is being run in a trusted network then all information can be reported using the `--safe-zone` option of the start command. Similarly, the `--exclude-self` option can be used to prevent other dashboards from getting gpuview of the current machine. This way the stats of the host are only shown on its own dashboard.


Thumbnail view of GPUs across multiple hosts.  

![Screenshot: gpuview](imgs/dash-1.png)

Detailed view of GPUs across multiple hosts.  

![Screenshot: gpuview](imgs/dash-2.png)


License
-------

[MIT License](LICENSE)



[repo_gpustat]: https://github.com/wookayin/gpustat
[pypi_gpuview]: https://pypi.python.org/pypi/gpuview
