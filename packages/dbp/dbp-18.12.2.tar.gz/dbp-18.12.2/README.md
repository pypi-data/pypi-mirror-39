# Docker-buildpackage

[![PyPI version](https://badge.fury.io/py/dbp.svg)](https://pypi.org/project/dbp/)
[![CalVer](https://img.shields.io/badge/calver-YY.0M.MICRO-blue.svg)](https://pypi.org/project/dbp/)
[![Build status](https://badge.buildkite.com/1767c846c36bcae205347eb72a5396be1474608249b0849f16.svg)](https://buildkite.com/opx/opx-infra-dbp)
[![codecov](https://codecov.io/gh/opx-infra/dbp/branch/master/graph/badge.svg)](https://codecov.io/gh/opx-infra/dbp)

Docker-buildpackage is a tool for building OpenSwitch Debian packages.

## Summary

* Docker-buildpackage has two parts: a cli app (`dbp`) and a Docker image ([`opxhub/gbp`](https://github.com/opx-infra/gbp-docker))
* `dbp` manages the Docker image and container lifecycle
* `dbp` resolves the local build dependency graph
* `dbp` runs [Git-buildpackage](https://honk.sigxcpu.org/piki/projects/git-buildpackage/) with [this configuration](https://github.com/opx-infra/gbp-docker/blob/master/assets/gbp.conf) to build packages
* Git-buildpackage runs [Debuild](https://manpages.debian.org/stretch/devscripts/debuild.1.en.html) with [this configuration](https://github.com/opx-infra/gbp-docker/blob/master/assets/devscripts) to build packages

## Install

```bash
pip3 install dbp
```

## Docs

Get started with the [documentation](https://opx-infra.github.io/dbp/).

## Support

For bug reports and feature requests, file an issue on [GitHub](https://github.com/opx-infra/dbp/issues/new/choose). For other support, drop by the [*dbp* support channel](https://chat.openswitch.net/channel/dbp) and we'll help you out.
