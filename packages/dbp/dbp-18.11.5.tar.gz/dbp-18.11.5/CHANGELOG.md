# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Calendar Versioning](https://calver.org/).

## [Unreleased]

## [18.11.5] - 2018/11/29
### Changed
- opx-build has been upgraded from `installer/3.0.0` to `installer/3.1.0`

## [18.11.4] - 2018/11/26
### Added
- Option to always remove any running container first

### Changed
- Dbp log messages now to go stderr
- Use full name of directory for container name, not stem

### Fixed
- Missing user in container at runtime
- `dbp shell` returning 0 on error

## [18.11.3] - 2018/11/19
### Fixed
- Running command before container and user are ready

### Removed
- Isolate ordering options for dbp build

## [18.11.2] - 2018/11/12
### Added
- Subcommand for creating parallel Makefile

### Changed
- `debuild` is *only* run for `3.0 (git)` packages
- Shell process ID has been removed from container name

### Fixed
- Missing source tarball (now `gbp buildpackage` will run)
- `dbp build` and `dbp shell` now work from within repositories (not just the workspace)

## [18.11.1] - 2018/11/07
### Changed
- `dbp build` now runs `debuild` instead of `gbp buildpackage` to better support `3.0 (git)` packages

### Fixed
- Return code of 0 on failed builds instead of !0

## [18.11.0] - 2018/11/03
### Fixed
- "the input device is not a TTY" Docker run and exec error

## [18.10.7] - 2018/10/31
### Added
- Ability to set container name with `$CNAME` environment variable

### Changed
- Local package index is now stored separately from packages

### Fixed
- Parallel containers conflicting when writing package indexes

## [18.10.6] - 2018/10/23
### Fixed
- Debuild now uses `~/.devscripts` instead of hard-coding flags

## [18.10.5] - 2018/10/22
### Fixed
- Pooling multiple changes files with one call to `pool-packages`

## [18.10.4] - 2018/10/19
### Added
- New script for sorting packages into per-repository directories

### Changed
- Bump `gbp-docker` to 2.0.0
- Build artifacts are deposited into `/mnt` container-side (instead of `/mnt/pool/$DIST-$ARCH/src`)
- Local packages are indexed from `/mnt` (instead of `/mnt/pool/$DIST-$ARCH`)

### Fixed
- Packages built with `fakeroot debian/rules binary` are now correctly indexed

## [18.10.3] - 2018/10/12
### Changed
- Default upstream tag from `v%(version)s` to `upstream/%(version)s`

## [18.10.2] - 2018/10/10
### Added
- `--debug` flag for building unstripped, unoptimized binaries. Sets `DEB_BUILD_OPTIONS="nostrip noopt debug"`

## [18.10.1] - 2018/10/10
### Added
- OPX Installer build support (see [docs](https://opx-infra.github.io/dbp/#openswitch-installer))

## [18.10.0] - 2018/10/09
### Added
- Changelog
- Documentation and [docs site](https://opx-infra.github.io/dbp/)

### Changed
- Start using Calendar Versioning

## [0.7.1] - 2018/10/08
### Added
- `--no-extra-sources` flag for testing fully-local builds

### Changed
- Default OPX apt sources are used if no extra sources are specified
- Extra source files now expect a `.list` suffix
- Docker images are not pulled if the `--image` flag contains a colon

## [0.6.1] - 2018/10/08
### Changed
- Bump [gbp-docker](https://github.com/opx-infra/gbp-docker/tree/v1.0.5) version to v1.0.5, which fixes lintian issues

## [0.6.0] - 2018/10/08
### Added
- [Controlgraph](https://github.com/opx-infra/controlgraph) for resolving local build dependencies and the proper build order

### Removed
- [Builddepends](https://github.com/opx-infra/builddepends) support

## [0.5.5] - 2018/09/12
### Changed
- Upgrade gbp-docker to 1.0.3

## [0.5.4] - 2018/09/07
### Added
- Progress bar when pulling Docker images

## [0.5.3] - 2018/09/06
### Fixed
- Missing timezone and DEB email/name in container

## [0.5.2] - 2018/09/05
### Changed
- Upgrade gbp-docker to 1.0.1

## [0.5.1] - 2018/09/05
### Fixed
- Exception when `~/.gitconfig` is missing

## [0.5.0] - 2018/09/04
### Added
- Options for filtering isolated repositories when building

## [0.4.4] - 2018/09/04
### Fixed
- Git-buildpackage option parsing

## [0.4.3] - 2018/09/04
### Fixed
- Missing shell environment pieces due to non-login shell

## [0.4.2] - 2018/09/04
### Fixed
- Duplicate `bash -l` in container command

## [0.4.1] - 2018/09/03
### Fixed
- Missing user on container start

## [0.4.0] - 2018/09/02
### Added
- Support for `builddepends` input

## [0.3.3] - 2018/08/29
### Fixed
- Noisy output when starting/removing containers

## [0.3.2] - 2018/08/29
### Fixed
- Missing bash arguments

## [0.3.1] - 2018/08/29
### Added
- Everything

[Unreleased]: https://github.com/opx-infra/dbp/compare/v18.11.5...HEAD
[18.11.5]: https://github.com/opx-infra/dbp/compare/v18.11.4...v18.11.5
[18.11.4]: https://github.com/opx-infra/dbp/compare/v18.11.3...v18.11.4
[18.11.3]: https://github.com/opx-infra/dbp/compare/v18.11.2...v18.11.3
[18.11.2]: https://github.com/opx-infra/dbp/compare/v18.11.1...v18.11.2
[18.11.1]: https://github.com/opx-infra/dbp/compare/v18.11.0...v18.11.1
[18.11.0]: https://github.com/opx-infra/dbp/compare/v18.10.7...v18.11.0
[18.10.7]: https://github.com/opx-infra/dbp/compare/v18.10.6...v18.10.7
[18.10.6]: https://github.com/opx-infra/dbp/compare/v18.10.5...v18.10.6
[18.10.5]: https://github.com/opx-infra/dbp/compare/v18.10.4...v18.10.5
[18.10.4]: https://github.com/opx-infra/dbp/compare/v18.10.3...v18.10.4
[18.10.3]: https://github.com/opx-infra/dbp/compare/v18.10.2...v18.10.3
[18.10.2]: https://github.com/opx-infra/dbp/compare/v18.10.1...v18.10.2
[18.10.1]: https://github.com/opx-infra/dbp/compare/v18.10.0...v18.10.1
[18.10.0]: https://github.com/opx-infra/dbp/compare/v0.7.1...v18.10.0
[0.7.1]: https://github.com/opx-infra/dbp/compare/v0.6.1...v0.7.1
[0.6.1]: https://github.com/opx-infra/dbp/compare/v0.6.0...v0.6.1
[0.6.0]: https://github.com/opx-infra/dbp/compare/v0.5.5...v0.6.0
[0.5.5]: https://github.com/opx-infra/dbp/compare/v0.5.4...v0.5.5
[0.5.4]: https://github.com/opx-infra/dbp/compare/v0.5.3...v0.5.4
[0.5.3]: https://github.com/opx-infra/dbp/compare/v0.5.2...v0.5.3
[0.5.2]: https://github.com/opx-infra/dbp/compare/v0.5.1...v0.5.2
[0.5.1]: https://github.com/opx-infra/dbp/compare/v0.5.0...v0.5.1
[0.5.0]: https://github.com/opx-infra/dbp/compare/v0.4.4...v0.5.0
[0.4.4]: https://github.com/opx-infra/dbp/compare/v0.4.3...v0.4.4
[0.4.3]: https://github.com/opx-infra/dbp/compare/v0.4.2...v0.4.3
[0.4.2]: https://github.com/opx-infra/dbp/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/opx-infra/dbp/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/opx-infra/dbp/compare/v0.3.3...v0.4.0
[0.3.3]: https://github.com/opx-infra/dbp/compare/v0.3.2...v0.3.3
[0.3.2]: https://github.com/opx-infra/dbp/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/opx-infra/dbp/compare/40462d74eaff1cf85f52c497372be5e37d43e564...v0.3.1
