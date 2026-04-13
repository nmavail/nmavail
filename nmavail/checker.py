import asyncio
import itertools
import sys

from rich.console import Console

from .platforms.domains import POPULAR_TLDS, DomainChecker
from .platforms.github import GitHubChecker, GitHubRepoChecker
from .platforms.gitlab import GitLabChecker, GitLabRepoChecker
from .platforms.packages import CRATES_CHECKER, GO_CHECKER, NPM_CHECKER, PYPI_CHECKER
from .platforms.unix import AlpineChecker, AptChecker, AurChecker, HomebrewChecker

console = Console(highlight=False)

# Dynamically generate all domain checkers
domain_checkers = [DomainChecker(tld) for tld in POPULAR_TLDS]

CHECKERS = [
    *domain_checkers,
    GitHubChecker(),
    GitHubRepoChecker(),
    GitLabChecker(),
    PYPI_CHECKER,
    NPM_CHECKER,
    CRATES_CHECKER,
    GO_CHECKER,
]


async def _loading_animation(stop_event: asyncio.Event, prefix="Checking"):
    """Loading spinner animation"""
    chars = itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])
    while not stop_event.is_set():
        sys.stdout.write(f"\r{next(chars)} {prefix}...")
        sys.stdout.flush()
        await asyncio.sleep(0.1)
    sys.stdout.write("\r" + " " * 60 + "\r")  # Clear line when done
    sys.stdout.flush()


async def check_name(name: str):
    # Start loading spinner
    stop_event = asyncio.Event()
    loading_task = asyncio.create_task(_loading_animation(stop_event, "Checking"))

    # Define group tasks
    async def run_group(checkers_list, _group_name):
        tasks = [checker.check(name) for checker in checkers_list]
        results = await asyncio.gather(*tasks)
        return list(zip(checkers_list, results, strict=False))

    domain_task = asyncio.create_task(run_group(domain_checkers, "Domains"))
    github_task = asyncio.create_task(
        run_group(
            [
                GitHubChecker(),
                GitHubRepoChecker(),
                GitLabChecker(),
                GitLabRepoChecker(),
            ],
            "Developer Platforms",
        )
    )
    package_task = asyncio.create_task(
        run_group(
            [PYPI_CHECKER, NPM_CHECKER, CRATES_CHECKER, GO_CHECKER],
            "Package Registries",
        )
    )
    system_task = asyncio.create_task(
        run_group(
            [HomebrewChecker(), AurChecker(), AptChecker(), AlpineChecker()],
            "System Packages",
        )
    )

    total_count = 4

    # Use asyncio.as_completed to handle results in order of completion
    for idx, completed_task in enumerate(
        asyncio.as_completed([domain_task, github_task, package_task, system_task]),
        start=1,
    ):
        results = await completed_task

        # Clear loading spinner
        stop_event.set()
        await loading_task

        # Determine which group this belongs to
        if results and "Domain" in results[0][0].name:
            _print_group("Domains", results, name)
        elif results and "GitHub" in results[0][0].name:
            _print_group("Developer Platforms", results, name)
        elif results and results[0][0].name in [
            "PyPI",
            "NPM",
            "Crates.io",
            "Go Modules",
        ]:
            _print_group("Package Registries", results, name)
        else:
            _print_group("System Packages", results, name)

        # Restart loading spinner if there are more tasks
        if idx < total_count:
            stop_event.clear()
            loading_task = asyncio.create_task(
                _loading_animation(stop_event, "Checking remaining")
            )


def _print_group(title, results, name=""):
    console.print(f"[bold]{title}:[/bold]")

    # For Developer Platforms, we manually group the output for clarity
    if title == "Developer Platforms":
        from .platforms.github import GitHubChecker, GitHubRepoChecker
        from .platforms.gitlab import GitLabChecker, GitLabRepoChecker

        gh_results = [
            (c, r)
            for c, r in results
            if isinstance(c, (GitHubChecker, GitHubRepoChecker))
        ]
        gl_results = [
            (c, r)
            for c, r in results
            if isinstance(c, (GitLabChecker, GitLabRepoChecker))
        ]

        if gh_results:
            console.print("  - GitHub:")
            for checker, result in gh_results:
                if "Repo Search" in checker.name:
                    _print_github_repo_lines(result, indent=4)
                else:
                    _print_status_line(checker, result, indent=4, name=name)

        if gl_results:
            # Check if GitLab has more results (only fetched 1 page)
            has_more = False
            for checker, result in gl_results:
                if "Repo Search" in checker.name and isinstance(result, dict):
                    has_more = result.get("has_more", False)
                    break

            if has_more:
                console.print("  - GitLab (list first 100 results only):")
            else:
                console.print("  - GitLab:")

            for checker, result in gl_results:
                if "Repo Search" in checker.name:
                    _print_github_repo_lines(result, indent=4, need_token=has_more)
                else:
                    _print_status_line(checker, result, indent=4, name=name)
    else:
        for checker, result in results:
            if "Repo Search" in checker.name:
                _print_github_repo_lines(result, indent=4)
            else:
                _print_status_line(checker, result, indent=4, name=name)


def _print_github_repo_lines(result, indent=0, need_token=False):
    """Print two lines of GitHub/GitLab Repo Search information"""
    prefix = " " * indent
    # Align Repo Search lines with User/Org
    width = 18

    if isinstance(result, dict) and "error" in result:
        # Error case
        color = "yellow"
        status_str = result["error"]
        icon = "!  "
        console.print(
            f"[{color}]{prefix}{icon} {'Repo Search':<{width}}  : {status_str}[/{color}]"
        )
    elif isinstance(result, dict):
        stars_info = result.get("top_stars")
        total_count = result.get("total_count", 0)

        if stars_info is None:
            # No matches
            color = "green"
            icon = "✓  "
            console.print(
                f"[{color}]{prefix}{icon} {'Total Repos':<{width}}  : [not italic]None[/not italic][/{color}]"
            )
        else:
            # Has matches
            color = "red"
            icon = "✗  "
            star_word = "star" if stars_info == 1 else "stars"
            # Display total repo count (if has_more, show "+")
            count_display = f"{total_count}" if not need_token else str(total_count)
            console.print(
                f"[{color}]{prefix}{icon} {'Total Repos':<{width}}  : [not bold]{count_display}[/not bold][/{color}]"
            )
            # Second line: align with first line
            # If has_more, show "more than" for stars
            if need_token:
                console.print(
                    f"[{color}]{prefix}{icon} {'Top Stars':<{width}}  : more than [not bold]{stars_info}[/not bold] {star_word}[/{color}]"
                )
            else:
                console.print(
                    f"[{color}]{prefix}{icon} {'Top Stars':<{width}}  : [not bold]{stars_info}[/not bold] {star_word}[/{color}]"
                )


def _print_status_line(checker, result, indent=0, is_gh_repo=False, name=""):
    """Unified handling for printing single-line status"""
    prefix = " " * indent

    # Check if there's an error
    if isinstance(result, dict) and "error" in result:
        icon = "!  "
        color = "yellow"
        status_str = result["error"]
    elif isinstance(result, dict):
        # Dict type (GitHub Repo Search, etc.)
        is_available = result.get("available", False)
        if is_available:
            icon = "✓  "
            color = "green"
            status_str = "None" if is_gh_repo else "Available"
        else:
            icon = "✗  "
            color = "red"
            if is_gh_repo:
                stars_info = result.get("top_stars", 0)
                total_count = result.get("total_count", 0)
                star_word = "star" if stars_info == 1 else "stars"
                count_str = (
                    f" ([not bold]{total_count}[/not bold] repos)"
                    if total_count > 0
                    else ""
                )
                status_str = f"[not bold]{stars_info}[/not bold] {star_word}{count_str}"
            else:
                status_str = "Taken"
    else:
        # Bool type (domain, GitHub User/Org, GitLab, etc.)
        is_available = bool(result)
        if is_available:
            icon = "✓  "
            color = "green"
            status_str = "Available"
        else:
            icon = "✗  "
            color = "red"
            status_str = "Taken"

    display_name = checker.name
    if is_gh_repo:
        display_name = "Repo Search"
    elif "GitHub (" in display_name:
        display_name = display_name.replace("GitHub (", "").replace(")", "")
    elif "Domain (" in display_name and indent > 0 and name:
        # Domain check: dynamically generate display name
        tld = display_name.split("(")[-1].split(")")[0]
        full_domain = f"{name}.{tld}"
        display_name = f".{tld}" if len(full_domain) > 20 else full_domain
    elif (
        "Repology" in display_name
        and isinstance(result, dict)
        and not result.get("available", True)
    ):
        # Unix/Linux check: display number of occupied repos
        repo_count = result.get("repo_count", 0)
        status_str = f"Taken ([not bold]{repo_count}[/not bold] repos)"

    width = 18 if indent <= 4 else 14
    # Print entire line with unified color
    console.print(
        f"[{color}]{prefix}{icon} {display_name:<{width}}  : {status_str}[/{color}]"
    )
