# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-04-10

### Added
- Support for GitLab JiHu (jihulab.com) for better connectivity in China
- System package availability checking (Homebrew, AUR, Debian/Ubuntu, Alpine Linux)
- Loading animation during checks for better UX
- Environment variable support for tokens (`GITHUB_TOKEN`, `GITLAB_TOKEN`)
- Intelligent data source selection based on token availability

### Changed
- **GitLab integration**: 
  - Split results into 3 lines (User/Group, Total Repos, Top Stars) to match GitHub display format
  - Improved error handling - single source per request, no fallback loops
  - Added `x-total` header parsing for accurate repository counts (requires token)
  - Renamed "User/Org" to "User/Group" for GitLab accuracy
- **Smart source selection**:
  - With token → Uses GitLab.com for complete API features
  - Without token → Uses JiHu GitLab for better stability in China
- **Documentation**: Added detailed token generation guides with required permissions
- **CLI help**: Enhanced command descriptions with token requirements

### Fixed
- Fixed GitLab API HTTP 400 error caused by unsupported `order_by=stars` parameter
- Fixed GitLab Total Repos display showing "Found" instead of actual count
- Aligned GitLab and GitHub output formatting (removed extra indentation)
- Removed infinite retry loops when mirrors fail (now shows Timeout directly)

### Removed
- Automatic fallback between GitLab.com and JiHu GitLab (now uses single source based on token presence)

## [0.1.0] - Initial Release

### Added
- Domain availability checking via WHOIS and DNS
- GitHub username and repository search
- GitLab username and repository search
- Package registry checking (PyPI, NPM, Crates.io, Go Modules)
- Async parallel execution for fast checks
- Beautiful CLI interface with Rich library
- Configuration management for API tokens
