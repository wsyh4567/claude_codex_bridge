# 简体中文版

基于上游 CCB 8.7.10。本分支默认使用简体中文。

## 汉化范围

- CCB 侧栏：通信、快捷键、连接状态、配置页面提示、任务状态和重载提示。
- 主命令帮助及常用子命令：启动、停止、配置、重载、诊断、清空和压缩上下文、重启、队列、追踪和主题。
- 配置网页默认显示已有的中文词库，仍可使用页面语言选择器切换英文。
- 中文预览按终端显示宽度截断，避免双宽字符挤出边框。

命令、配置键、JSON 字段、代理标识和用户自定义文本保持原值。高级子命令中尚未翻译的帮助保留英文。Herdr、WezTerm 和各提供者 CLI 属于独立项目，其界面不在本分支中。

## Windows 修复

侧栏读取后台端点描述，通过 `127.0.0.1` TCP 连接，并完成现有用户令牌认证后请求项目视图。禁止连接远程地址，拒绝过期令牌和无效认证回应。

侧栏启动脚本优先使用安装包自带的 `bin/ccb-agent-sidebar.exe`。

## 语言切换

PowerShell：

```powershell
$env:CCB_LANG = 'zh'  # 简体中文（默认）
$env:CCB_LANG = 'en'  # 英文
ccb --help
```

已启动的侧栏在重新启动后使用新语言。配置网页可通过语言选择器或 `?lang=en` 切换。

## 构建与验证

在 Windows x64 上准备 Python 3.10+、Rust 和 MSVC 构建工具，然后从仓库根目录执行：

```powershell
$env:CCB_LANG = 'en'
cargo test --locked --manifest-path tools/ccb-agent-sidebar/Cargo.toml
$env:CCB_LANG = 'zh'
cargo test --locked --manifest-path tools/ccb-agent-sidebar/Cargo.toml --test localized_ui
$env:PYTHONPATH = "$PWD/lib"
python -m pytest -q test/test_chinese_localization.py
python platforms/windows/packaging/build_release.py --git-ref HEAD --output-dir dist/windows/x86_64
```

构建要求工作区干净，产物包含当前提交的源码和 Windows 原生程序。解压 ZIP 后安装：

```powershell
.\install.ps1 install -Yes
```

运行环境还需要 Python、Git Bash、WezTerm 和 Herdr。不要使用上游二进制覆盖本分支的侧栏；更新时从此 fork 重新构建。
