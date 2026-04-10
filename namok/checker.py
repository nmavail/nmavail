import asyncio

from rich.console import Console

from .platforms.domains import POPULAR_TLDS, DomainChecker
from .platforms.github import GitHubChecker, GitHubRepoChecker
from .platforms.gitlab import GitLabChecker
from .platforms.packages import CRATES_CHECKER, GO_CHECKER, NPM_CHECKER, PYPI_CHECKER

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


async def check_name(name: str):
    console.print(f"\n[bold blue]Checking availability for: {name}[/bold blue]\n")
    tasks = [checker.check(name) for checker in CHECKERS]
    results = await asyncio.gather(*tasks)

    table_available = []
    table_taken = []

    # 分组显示：域名、GitHub、其他
    domain_results = []
    github_results = []
    other_results = []

    for checker, result in zip(CHECKERS, results):
        # 统一提取状态
        is_available = False
        is_error = False
        error_msg = ""

        if isinstance(result, dict):
            if "error" in result:
                is_error = True
                error_msg = result["error"]
            else:
                is_available = result.get("available", False)
        else:
            is_available = bool(result)

        if "Domain" in checker.name:
            domain_results.append((checker, result))
        elif "GitHub" in checker.name:
            github_results.append((checker, result))
        else:
            other_results.append((checker, result))

        if not is_error:
            if is_available:
                table_available.append(checker.name)
            else:
                table_taken.append(checker.name)

    # 输出域名部分（带缩进）
    if domain_results:
        console.print("[bold]Domains:[/bold]")
        for checker, result in domain_results:
            _print_status_line(checker, result, indent=4, name=name)
        console.print()  # 空行分隔

    # 输出 GitHub 部分（带缩进）
    if github_results:
        console.print("[bold]GitHub:[/bold]")
        for checker, result in github_results:
            if "Repo Search" in checker.name:
                _print_github_repo_lines(checker, result, indent=4)
            else:
                _print_status_line(checker, result, indent=4)
        console.print()  # 空行分隔

    # 输出其他平台部分
    if other_results:
        console.print("[bold]Other Platforms & Packages:[/bold]")
        for checker, result in other_results:
            _print_status_line(checker, result, indent=4)
        console.print()


def _print_github_repo_lines(checker, result, indent=0):
    """打印 GitHub Repo Search 的两行信息"""
    prefix = " " * indent
    if isinstance(result, dict) and "error" in result:
        # 错误情况
        color = "yellow"
        status_str = result['error']
        icon = "!  "
        console.print(f"[{color}]{prefix}{icon} {'Repo Search':<18}  : {status_str}[/{color}]")
    elif isinstance(result, dict):
        stars_info = result.get("top_stars")
        total_count = result.get("total_count", 0)
        
        if stars_info is None:
            # 无重名
            color = "green"
            icon = "✓  "
            console.print(f"[{color}]{prefix}{icon} {'Total Repos':<18}  : None[/{color}]")
        else:
            # 有重名
            color = "red"
            icon = "✗  "
            star_word = "star" if stars_info == 1 else "stars"
            console.print(f"[{color}]{prefix}{icon} {'Total Repos':<18}  : {total_count}[/{color}]")
            # 第二行：与第一行对齐，前面也用相同宽度的占位符
            console.print(f"[{color}]{prefix}{icon} {'Top Stars':<18}  : {stars_info} {star_word}[/{color}]")

def _print_status_line(checker, result, indent=0, is_gh_repo=False, name=""):
    """统一处理单行状态的打印逻辑"""
    prefix = " " * indent
    
    # 判断是否出错
    if isinstance(result, dict) and "error" in result:
        icon = "!  "
        color = "yellow"
        status_str = result['error']
    elif isinstance(result, dict):
        # dict 类型（GitHub Repo Search 等）
        is_available = result.get("available", False)
        if is_available:
            icon = "✓  "
            color = "green"
            if is_gh_repo:
                status_str = "None"
            else:
                status_str = "Available"
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
        if len(full_domain) > 20:
            display_name = f".{tld}"
        else:
            display_name = full_domain
        
    width = 18 if indent > 0 else 22
    # 整行统一颜色
    console.print(f"[{color}]{prefix}{icon} {display_name:<{width}}  : {status_str}[/{color}]")
