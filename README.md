# Nmck

[![PyPI version](https://badge.fury.io/py/nmck.svg)](https://badge.fury.io/py/nmck)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Nmck** is a powerful command-line tool designed to check the availability of names across multiple domains and platforms. Whether you are naming a startup, a new project, or an open-source library, Nmck helps you secure your brand identity by verifying if a name is already taken.

## Features

- **Domain Availability**: Checks popular TLDs (e.g., `.com`, `.io`, `.dev`, `.ai`) via WHOIS and DNS lookups
- **Developer Platforms**: Verifies username availability on GitHub and GitLab
- **Package Registries**: Checks if a name is available on PyPI, NPM, Crates.io, and Go Modules
- **System Packages**: Checks Homebrew, AUR, Debian/Ubuntu, and Alpine Linux
- **Asynchronous & Fast**: Uses async I/O to perform checks in parallel (~13 seconds total)
- **Clean CLI Interface**: Provides a beautiful, easy-to-read terminal output with smooth loading animations
- **No Configuration Required**: Works out of the box, no tokens or setup needed

## Installation

### Option 1: Install via pip (Recommended)
The easiest way to install Nmck is via pip:
```bash
pip install nmck
```

### Option 2: Install via uv
If you prefer using [uv](https://github.com/astral-sh/uv):
```bash
uv tool install nmck
```

### Option 3: Install from Source
For developers or those who want the latest unreleased features:
```bash
git clone https://github.com/cphotor/nmck.git
cd nmck
pip install .
```

## Usage

### Check Name Availability
To check a name across all supported platforms:
```bash
nmck my-awesome-name
```

**Example Output:**
```
Package Registries:                                         
    ✗   PyPI                : Taken
    ✗   NPM                 : Taken
    ✓   Crates.io           : Available
    ✓   Go Modules          : Available

System Packages:                                            
    ✓   Homebrew            : Available
    ✓   Arch (AUR)          : Available
    ✓   Debian/Ubuntu       : Available
    ✓   Alpine Linux        : Available

Developer Platforms:                                        
  - GitHub:
    ✗   User/Org            : Taken
    ✗   Total Repos         : 9702854
    ✗   Top Stars           : 25920 stars
  - GitLab (list first 100 results only):
    ✗   User/Group          : Taken
    ✗   Total Repos         : 100+
    ✗   Top Stars           : more than 0 stars

Domains:                                                    
    ✗   my-awesome-name.com : Taken
    ✓   my-awesome-name.io  : Available
    ✓   my-awesome-name.dev : Available
```

### Command Line Options

**Show Version:**
```bash
nmck --version
nmck -V
```

**Show Help:**
```bash
nmck --help
nmck -H
```

**Examples:**
```bash
nmck test
nmck google
nmck myproject
```

## Supported Platforms

| Category | Platforms |
| :--- | :--- |
| **Domains** | `.com`, `.org`, `.net`, `.io`, `.co`, `.dev`, `.app`, `.xyz`, `.ai`, `.me`, `.cn`, `.tv`, `.ly`, `.it` |
| **Developer Platforms** | GitHub (User/Org & Repo Search), GitLab (User/Group & Repo Search) |
| **Package Registries** | PyPI, NPM, Crates.io, Go Modules |
| **System Packages** | Homebrew, Arch (AUR), Debian/Ubuntu, Alpine Linux |

## Performance

- **Total check time**: ~13 seconds (varies based on network conditions)
- **Parallel execution**: All checks run concurrently
- **Smart pagination**: GitLab limited to 1 page (100 results) for speed
- **Optimized timeouts**: 10 second timeout per request

## Development

This project uses [Ruff](https://github.com/astral-sh/ruff) for linting and formatting.

```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check .
```

## License

MIT
