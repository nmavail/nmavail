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

**Important:** GitHub and GitLab have strict API rate limits. **To get complete search results (including repo search with exact total counts), you must configure API tokens.** Without tokens, some features will be limited or return incomplete data.

Namok allows you to set authentication tokens to increase API rate limits and avoid blocks.

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
1. Go to [GitLab Settings > Access Tokens](https://gitlab.com/-/user_settings/personal_access_tokens) (or JiHu GitLab equivalent)
2. Click "Add new token"
3. Set expiration date and name (e.g., `nmck-checker`)
4. **Required scopes**:
   - `read_api` - **Required** for API access (search repositories & users)
   - `read_user` - Optional, for user verification
5. Copy the token and run:
   ```bash
   nmck set gitlab_token glpat-xxxxxxxxxxxx
   ```

> **Note:** GitLab.com may restrict access from certain regions. If you're in mainland China, the tool will automatically use JiHu GitLab (jihulab.com) when no token is configured.

**Using Environment Variables (Alternative):**
```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
export GITLAB_TOKEN=glpat-xxxxxxxxxxxx
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
