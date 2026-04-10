# Nmck

**Nmck** is a powerful command-line tool designed to check the availability of names across multiple domains and platforms. Whether you are naming a startup, a new project, or an open-source library, Namok helps you secure your brand identity by verifying if a name is already taken.

## Features

- **Domain Availability**: Checks popular TLDs (e.g., `.com`, `.io`, `.dev`, `.ai`) via WHOIS and DNS lookups.
- **Developer Platforms**: Verifies username availability on GitHub and GitLab (including JiHu GitLab for better connectivity in China).
- **Package Registries**: Checks if a name is available on PyPI, NPM, Crates.io, and Go Modules.
- **Asynchronous & Fast**: Uses async I/O to perform checks in parallel, providing real-time streaming results.
- **Clean CLI Interface**: Provides a beautiful, easy-to-read terminal output with loading animations.

## Installation

### Prerequisites
- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) (recommended)

### Option 1: Install via uv (Recommended)
```bash
# Clone the repository
git clone https://github.com/your-username/nmck.git
cd nmck

# Install as a global tool
uv tool install .

# Now you can use it directly
nmck --version
```

### Option 2: Install via pip
```bash
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
Namok allows you to set authentication tokens to increase API rate limits and avoid blocks.

**Set a Token:**
```bash
nmck set github_token ghp_xxxxxxxxxxxx
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
| **Code Hosting** | GitHub (User/Org & Repo Search), GitLab.com, JiHu GitLab |
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
