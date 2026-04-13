# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.3] - 2026-04-13

### Changed
- **Output formatting**: Disabled Rich auto-highlighting for consistent text display (numbers and brackets no longer highlighted)
- **Help text**: Added GitHub star and bug report links to `--help` output
- **Cleanup**: Removed extra empty lines from command output

### Fixed
- GitLab display text formatting (removed bold styling from "100" in parenthetical note)

## [0.4.2] - 2026-04-12

### Changed
- **Documentation**: Replaced badge.fury.io with shields.io for PyPI version badge (more reliable)

## [0.4.1] - 2026-04-11

### Changed
- **Development Status**: Upgraded from Alpha to Beta to reflect project maturity

## [0.4.0] - 2026-04-11

### Changed
- **Project renamed**: Changed from `nmck` to `nmavail` for better brand identity
- **Installation**: Updated documentation to recommend `uv tool install` as primary method
- **Documentation**: All references updated from `nmck` to `nmavail`

### Breaking Changes
- Command name changed from `nmck` to `nmavail`
- Package name changed from `nmck` to `nmavail`
- Migration required: users must reinstall as `nmavail`

## [0.3.1] - 2026-04-11

### Fixed
- Fixed `--help` parameter conflict with Click's built-in handler
- Removed manual `--help` option definition (Click handles it automatically)
- Cleaned up duplicate `if __name__ == "__main__"` block

### Changed
- Documentation: Updated installation guide to recommend uv tool and pipx
- Documentation: Removed direct pip install recommendation (avoids system Python issues)
- Documentation: Clarified that uv/pipx automatically manage Python environment

## [0.3.0] - 2026-04-11

### Breaking Changes
- **Removed token configuration**: No more `nmavail set` command or config files required
- **Simplified CLI**: Changed from `nmavail check <name>` to `nmavail <name>`
- **Removed GitLab JiHu support**: Now uses only GitLab.com

### Added
- Command-line options: `--version`/`-V` and `--help`/`-H`
- System packages support: Homebrew, AUR, Debian/Ubuntu, Alpine Linux
- Smart pagination for GitLab (100 results per page with `100+` indicator)
- WHOIS retry mechanism for more reliable domain checks
- Smooth loading animation without text jitter

### Changed
- **No configuration required**: Works out of the box, no tokens needed
- **Unified timeout**: All requests use `DEFAULT_TIMEOUT = 10s`
- **Improved error handling**: Distinguish between timeout and network errors
- **GitLab output**: Shows "list first 100 results only" when results exceed 100
- **Domain checking**: Uses WHOIS status field for accurate detection
- **Performance**: Reduced query time from 40-60s to 11-15s

### Fixed
- Fixed `.ly` domain check logic (status field instead of domain_name)
- Fixed AUR and Debian package check logic
- Fixed GitLab pagination showing `+` for small result counts
- Fixed bold formatting in numbers output
- Fixed loading animation text jitter

### Removed
- Token configuration system (`~/.config/nmavail/config.json`)
- `nmavail set` and `nmavail check` subcommands
- Environment variable support (no longer needed)
- GitLab JiHu mirror support

## [0.2.1] - 2026-04-10

### Fixed
- Fixed `.ly` domain check logic (use status field instead of domain_name)
- Fixed AUR and Debian package check logic
- Fixed old 'namok' references to 'nmck'
- Fixed timeout error handling (distinguish Timeout vs Network errors)
- Fixed bold formatting issue in numbers output

### Changed
- Unified timeout configuration (DEFAULT_TIMEOUT=10s)
- GitLab pagination (list first 100 results only)
- WHOIS retry mechanism for domain checks
- Translated all Chinese comments to English
- Added '- ' prefix for GitHub/GitLab sections
- Better GitLab output (more than X stars)


### Performance
- Reduced query time from 40-60s to 11-15s
- GitLab query from 10-20s to 2-3s (1 page only)

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
