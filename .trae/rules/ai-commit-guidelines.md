# AI 提交规范

## 目的
确保所有代码提交的一致性、完整性和可追溯性，避免部分提交、版本不一致和文档缺失问题。

---

## 一、版本号管理

### 1.1 语义化版本规范 (SemVer)
版本号格式：`MAJOR.MINOR.PATCH`（如：`0.3.1`）

- **MAJOR**：破坏性变更（Breaking Changes）
- **MINOR**：向后兼容的功能新增
- **PATCH**：向后兼容的问题修复

### 1.2 版本升级规则

| 变更类型 | 升级位置 | 示例 |
|---------|---------|------|
| 破坏性变更 | MAJOR | 0.3.1 → 1.0.0 |
| 新功能 | MINOR | 0.3.1 → 0.4.0 |
| Bug 修复 | PATCH | 0.3.1 → 0.3.2 |
| 文档/重构 | PATCH | 0.3.1 → 0.3.2 |

### 1.3 版本号统一检查清单
提交前**必须**检查并统一以下位置：

- [ ] `pyproject.toml` - `version` 字段
- [ ] `CHANGELOG.md` - 最新版本标题
- [ ] `README.md` - 版本号 badge（如果有）
- [ ] 其他文档中的版本引用

---

## 二、文档更新要求

### 2.1 必须更新的文档

#### CHANGELOG.md
- [ ] 在顶部添加新版本条目
- [ ] 格式遵循 [Keep a Changelog](https://keepachangelog.com/)
- [ ] 包含版本号和日期
- [ ] 分类：Added/Changed/Deprecated/Removed/Fixed/Security

**示例**：
```markdown
## [0.4.0] - 2026-04-11

### Changed
- 项目名称从 nmck 更改为 nmavail

### Added
- 新功能描述
```

#### README.md
- [ ] 项目名称和描述
- [ ] 安装命令和示例
- [ ] 使用示例和输出
- [ ] Badge 版本号（如果有）
- [ ] 配置说明（如果有变更）

#### 其他文档
- [ ] 项目进度文档（docs/PROJECT_STATUS.md）
- [ ] API 文档
- [ ] 开发者文档

---

## 三、代码质量检查

### 3.1 提交前必检项目

```bash
# 1. 代码质量检查
uv run ruff check .

# 2. 代码格式检查
uv run ruff format --check .

# 3. 类型检查（如果有类型注解）
uv run pyright

# 4. 构建检查
uv build

# 5. 运行测试（如果有）
uv run pytest
```

### 3.2 检查标准
- ✅ Ruff：无 ERROR（WARNING 可接受）
- ✅ 格式：无差异
- ✅ 类型检查：无错误
- ✅ 构建：成功生成 sdist 和 wheel
- ✅ 测试：全部通过

---

## 四、Git 提交规范

### 4.1 提交信息格式
遵循 [Conventional Commits](https://www.conventionalcommits.org/)

**格式**：
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### 4.2 Type 类型

| Type | 说明 | 版本影响 |
|------|------|---------|
| `feat` | 新功能 | MINOR |
| `fix` | Bug 修复 | PATCH |
| `docs` | 文档更新 | PATCH |
| `style` | 代码格式（不影响逻辑） | PATCH |
| `refactor` | 重构（既不是新功能也不是修复） | PATCH |
| `chore` | 构建过程或辅助工具变动 | PATCH |
| `breaking` | 破坏性变更 | MAJOR |

### 4.3 提交示例

```bash
# 新功能
feat(cli): add --version flag

# Bug 修复
fix(domains): fix .ly domain check logic

# 文档更新
docs(readme): update installation guide

# 重构
refactor(checker): simplify async logic

# 破坏性变更
breaking: remove token configuration system
```

### 4.4 禁止的提交信息
- ❌ `fix`
- ❌ `update`
- ❌ `WIP`
- ❌ `temp`
- ❌ `asdf`

---

## 五、原子提交原则

### 5.1 什么是一个原子提交？
一个提交应该只包含**一个逻辑变更**：
- ✅ 修复一个 bug
- ✅ 添加一个功能
- ✅ 更新一组相关的文档
- ❌ 同时修复 bug 和添加新功能
- ❌ 混杂重构和新功能

### 5.2 部分提交的危害
- ❌ 难以回滚
- ❌ 难以审查
- ❌ 版本历史混乱
- ❌ 难以定位问题

### 5.3 正确的提交流程

1. **检查工作区**
   ```bash
   git status
   git diff --stat
   ```

2. **确认所有修改**
   - 列出所有修改的文件
   - 确认没有遗漏
   - 确认没有无关修改

3. **一次性提交所有相关修改**
   ```bash
   git add -A
   git commit -m "feat: description"
   ```

4. **验证提交**
   ```bash
   git log -1 --stat
   git status  # 应该是干净的
   ```

---

## 六、AI 操作特别规范

### 6.1 修改前必须确认

**AI 必须执行的步骤**：

1. **搜索所有引用**
   ```bash
   grep -r "旧名称" --include="*.py" --include="*.md" --include="*.toml"
   ```

2. **列出修改清单**
   - 文件列表
   - 修改点数量
   - 影响范围

3. **等待用户确认**
   - 展示修改计划
   - 获得用户同意后再动手

### 6.2 版本号修改特别规定

**AI 必须**：
1. 列出所有包含版本号的位置
2. 说明升级类型（MAJOR/MINOR/PATCH）
3. 建议新版本号
4. 等待用户确认

### 6.3 重构/改名特别规定

**AI 必须**：
1. 搜索所有引用位置
2. 评估影响范围
3. 制定详细修改计划
4. 分步骤执行（每步可回滚）
5. 每步完成后验证

---

## 七、发布流程

### 7.1 PyPI 发布前检查

```bash
# 1. 清理之前的构建
rm -rf dist/

# 2. 构建新版本
uv build

# 3. 检查构建产物
tar -tzf dist/*.tar.gz
unzip -l dist/*.whl

# 4. 本地安装测试
pip install dist/*.whl
nmavail --version

# 5. 上传到 PyPI
uv publish
```

### 7.2 发布后验证

- [ ] PyPI 页面显示正确版本号
- [ ] README 渲染正确
- [ ] 安装命令有效
- [ ] 版本号 badge 已更新

---

## 八、提交前自检清单

AI 在提交前**必须**完成以下检查：

### 8.1 一致性检查
- [ ] 所有文件版本号统一
- [ ] 文档和代码同步更新
- [ ] CHANGELOG 已更新
- [ ] README 已更新

### 8.2 质量检查
- [ ] `ruff check` 通过
- [ ] `ruff format` 通过
- [ ] `pyright` 通过
- [ ] `uv build` 成功

### 8.3 Git 检查
- [ ] `git status` 干净（无未跟踪文件）
- [ ] `git diff --stat` 显示预期修改
- [ ] 提交信息符合规范
- [ ] 所有修改已添加（git add -A）

### 8.4 文档检查
- [ ] CHANGELOG.md 有新条目
- [ ] README.md 已更新
- [ ] 相关文档已更新
- [ ] 无 TODO 或 FIXME 遗留

---

## 九、错误处理和回滚

### 9.1 发现问题立即停止
- 发现版本不一致 → 停止提交
- 发现文档缺失 → 停止提交
- 发现测试失败 → 停止提交

### 9.2 回滚流程
```bash
# 撤销工作区修改
git restore .

# 撤销暂存区
git reset HEAD

# 撤销上一次提交
git reset --soft HEAD~1

# 强制回滚到某个版本
git reset --hard <commit-hash>
```

### 9.3 记录问题
- 在提交信息中说明回滚原因
- 更新项目问题记录
- 避免重复错误

---

## 十、工具配置

### 10.1 推荐的 Git 配置
```bash
# 提交信息模板
git config commit.template .gitmessage

# 自动格式化
git config core.autocrlf input

# 推送前运行测试
git config hook.prettush "uv run pytest"
```

### 10.2 VS Code 设置
```json
{
  "editor.formatOnSave": true,
  "python.linting.ruffEnabled": true,
  "python.linting.pyrightEnabled": true,
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true
  }
}
```

---

## 总结

**AI 提交黄金法则**：

1. **先检查，后修改** - 永远不要假设
2. **先确认，后执行** - 重大修改必须用户确认
3. **要完整，不要部分** - 原子提交，拒绝零散
4. **要统一，不要混乱** - 版本号、文档、代码同步
5. **要质量，不要凑合** - 检查不通过不提交

**违反后果**：
- 版本混乱
- 文档过期
- 难以维护
- 用户困惑

**遵守好处**：
- 清晰的历史记录
- 可靠的版本管理
- 易于协作
- 用户信任
