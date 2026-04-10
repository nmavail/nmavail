# Nmck

[![PyPI version](https://badge.fury.io/py/nmck.svg)](https://badge.fury.io/py/nmck)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Nmck** is a powerful command-line tool designed to check the availability of names across multiple domains and platforms. Whether you are naming a startup, a new project, or an open-source library, Nmck helps you secure your brand identity by verifying if a name is already taken.

## Features

- **Domain Availability**: Checks popular TLDs (e.g., `.com`, `.io`, `.dev`, `.ai`) via WHOIS and DNS lookups.
- **Developer Platforms**: Verifies username availability on GitHub and GitLab (including JiHu GitLab for better connectivity in China).
- **Package Registries**: Checks if a name is available on PyPI, NPM, Crates.io, and Go Modules.
- **Asynchronous & Fast**: Uses async I/O to perform checks in parallel, providing real-time streaming results.
- **Clean CLI Interface**: Provides a beautiful, easy-to-read terminal output with loading animations.

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
nmck check my-awesome-name
```

**Example Output:**
```
Domains:
    ✓   my-awesome-name.com   : Available
    ✗   my-awesome-name.io    : Taken

GitHub:
    ✓   User/Org              : Available

Software & Packages:
    ✓   PyPI                  : Available
    ✗   NPM                   : Taken
```

### Configuration

**Important:** GitHub and GitLab have API rate limits. **Tokens are required for higher rate limits and complete functionality.**

**Rate Limits:**
- **GitHub (no token)**: 60 requests/hour, full functionality
- **GitHub (with token)**: 5,000 requests/hour
- **GitLab (no token)**: Limited API access, no `x-total` header in repo search
- **GitLab (with token)**: Full API access with complete metadata

**Set a Token:**

**GitHub Token:**
1. Go to [GitHub Settings > Developer settings > Personal access tokens > Fine-grained tokens](https://github.com/settings/tokens?type=beta)
2. Click "Generate new token"
3. Set expiration and name (e.g., `nmck-checker`)
4. **Required permissions**:
   - Repository permissions: **Contents** (Read-only) - for searching repositories
   - Account permissions: **Email addresses** (Read-only) - for user verification
5. Copy the token and run:
   ```bash
   nmck set github_token ghp_xxxxxxxxxxxx
   ```

**GitLab Token:**
1. Go to [GitLab Settings > Access Tokens](https://gitlab.com/-/user_settings/personal_access_tokens)
2. Click "Add new token"
3. Set expiration date and name (e.g., `nmck-checker`)
4. **Required scopes**:
   - `read_api` - **Required** for API access (search repositories & users)
   - `read_user` - Optional, for enhanced user verification
5. Copy the token and run:
   ```bash
   nmck set gitlab_token glpat-xxxxxxxxxxxx
   ```

**Check Version:**
```bash
nmck --version
```

**Get Help:**
```bash
nmck --help
nmck help check
```

## Supported Platforms

| Category | Platforms |
| :--- | :--- |
| **Domains** | `.com`, `.org`, `.net`, `.io`, `.co`, `.dev`, `.app`, `.xyz`, `.ai`, `.me`, `.cn`, `.tv`, `.ly`, `.it` |
| **Code Hosting** | GitHub (User/Org & Repo Search), GitLab (User/Group & Repo Search) |
| **Packages** | PyPI, NPM, Crates.io, Go Modules |

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
