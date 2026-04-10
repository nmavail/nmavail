import asyncio
import itertools
import sys

from rich.console import Console

from .platforms.domains import POPULAR_TLDS, DomainChecker
from .platforms.github import GitHubChecker, GitHubRepoChecker
from .platforms.gitlab import GitLabChecker, GitLabRepoChecker
from .platforms.packages import CRATES_CHECKER, GO_CHECKER, NPM_CHECKER, PYPI_CHECKER
from .platforms.unix import AlpineChecker, AptChecker, AurChecker, HomebrewChecker

console = Console()

# 动态生成所有域名检查器
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
    """跑马灯动画"""
    chars = itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "", "⠦", "⠧", "⠇", ""])
    while not stop_event.is_set():
        sys.stdout.write(f"\r{next(chars)} {prefix}...")
        sys.stdout.flush()
        await asyncio.sleep(0.1)
    # 清除动画行
    sys.stdout.write("\r" + " " * 60 + "\r")
    sys.stdout.flush()


async def check_name(name: str):
    console.print()  # 先空一行

    # 启动跑马灯
    stop_event = asyncio.Event()
    loading_task = asyncio.create_task(_loading_animation(stop_event, "Checking"))

    # 定义分组任务
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

    # 使用 asyncio.as_completed 按完成顺序处理
    for idx, completed_task in enumerate(
        asyncio.as_completed([domain_task, github_task, package_task, system_task]),
        start=1,
    ):
        results = await completed_task

        # 清除跑马灯
        stop_event.set()
        await loading_task

        # 判断属于哪个分组
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

        # 如果还有未完成的，重新启动跑马灯
        if idx < total_count:
            stop_event.clear()
            loading_task = asyncio.create_task(
                _loading_animation(stop_event, "Checking remaining")
            )

    console.print()


def _print_group(title, results, name=""):
    console.print(f"[bold]{title}:[/bold]")

    # 如果是 Developer Platforms，我们手动分组打印以保持整洁
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
            console.print("  GitHub:")
            for checker, result in gh_results:
                if "Repo Search" in checker.name:
                    _print_github_repo_lines(checker, result, indent=4)
                else:
                    _print_status_line(checker, result, indent=4, name=name)

        if gl_results:
            console.print("  GitLab:")
            for checker, result in gl_results:
                if "Repo Search" in checker.name:
                    _print_github_repo_lines(checker, result, indent=4)
                else:
                    _print_status_line(checker, result, indent=4, name=name)
    else:
        for checker, result in results:
            if "Repo Search" in checker.name:
                _print_github_repo_lines(checker, result, indent=4)
            else:
                _print_status_line(checker, result, indent=4, name=name)

    console.print()  # 空行分隔


def _print_github_repo_lines(_checker, result, indent=0):
    """打印 GitHub/GitLab Repo Search 的两行信息"""
    prefix = " " * indent
    # Repo Search 的三行与 User/Org 对齐
    width = 18

    if isinstance(result, dict) and "error" in result:
        # 错误情况
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
            # 无重名
            color = "green"
            icon = "✓  "
            console.print(
                f"[{color}]{prefix}{icon} {'Total Repos':<{width}}  : None[/{color}]"
            )
        else:
            # 有重名
            color = "red"
            icon = "✗  "
            star_word = "star" if stars_info == 1 else "stars"
            # 显示仓库总数
            count_display = total_count
            console.print(
                f"[{color}]{prefix}{icon} {'Total Repos':<{width}}  : {count_display}[/{color}]"
            )
            # 第二行：与第一行对齐
            console.print(
                f"[{color}]{prefix}{icon} {'Top Stars':<{width}}  : {stars_info} {star_word}[/{color}]"
            )


def _print_status_line(checker, result, indent=0, is_gh_repo=False, name=""):
    """统一处理单行状态的打印逻辑"""
    prefix = " " * indent

    # 判断是否出错
    if isinstance(result, dict) and "error" in result:
        icon = "!  "
        color = "yellow"
        status_str = result["error"]
    elif isinstance(result, dict):
        # dict 类型（GitHub Repo Search 等）
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
                count_str = f" ({total_count} repos)" if total_count > 0 else ""
                status_str = f"{stars_info} {star_word}{count_str}"
            else:
                status_str = "Taken"
    else:
        # bool 类型（域名、GitHub User/Org、GitLab 等）
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
        # 域名检查：动态生成显示名称
        tld = display_name.split("(")[-1].split(")")[0]
        full_domain = f"{name}.{tld}"
        display_name = f".{tld}" if len(full_domain) > 20 else full_domain
    elif (
        "Repology" in display_name
        and isinstance(result, dict)
        and not result.get("available", True)
    ):
        # Unix/Linux 检查：显示占用的仓库数量
        repo_count = result.get("repo_count", 0)
        status_str = f"Taken ({repo_count} repos)"

    width = 18 if indent <= 4 else 14
    # 整行统一颜色
    console.print(
        f"[{color}]{prefix}{icon} {display_name:<{width}}  : {status_str}[/{color}]"
    )
