"""Chinese human-readable CLI help; command names remain stable."""
from textwrap import dedent

START_HELP = dedent("""
用法：ccb [-s] [-n]

日常操作：
  ccb                     按 `.ccb/ccb.config` 启动项目代理。
  ccb -s                  安全启动，保留 CLI 权限确认。
  ccb -n                  重建运行状态，保留配置和托管代理历史。
  ccb clear [agent...]     使用代理原生命令清空对话上下文。
  ccb compact [agent...]   使用代理原生命令压缩上下文。
  ccb restart <agent>     重启一个空闲代理。
  ccb reload              应用支持的配置变更；不支持的变更会返回诊断。
  ccb reload --dry-run    检查并预览配置变更，不修改运行状态。
  ccb config ui           打开项目配置页面。
  ccb kill                停止当前项目的后台和代理。
  ccb kill -f             强制清理当前项目残留的运行资源。
  ccb cleanup             后台停止后，清理可重建的缓存。
  ccb cleanup --legacy-provider-caches
                          同时清理对应项目目录已不存在的旧缓存。
  ccb theme [system|dark|light|+|-|PRESET]
                          查看或切换 CCB 界面主题。

通信与诊断：
  ccb ask <agent> [from <sender>] <message>  向代理提交任务。
  ccb followup <job_id> --message <text>    补充一个正在执行的任务。
  ccb doctor                              检查项目和运行环境。
  ccb screen <agent> [--lines 120] [--json] 查看代理面板。
  ccb ping <agent|ccbd>                    查看缓存的后台状态。
  ccb pend <agent|job_id> [N]              查看观察快照。
  ccb pend --watch <agent|job_id>          持续查看观察事件。
  ccb pend --inbox [--detail] <agent>      查看收件箱。
  ccb pend --queue [--detail] <agent|all>  查看等待队列。
  ccb queue [--detail] <agent|all>         查看任务积压。
  ccb trace <id>                          追踪任务、消息和回复。
  ccb repair <ack|retry|resubmit> ...      修复确认、重试或重新提交。
  ping / pend 是诊断视图；观察输出不代表任务已完成。

动态代理与工作流：
  ccb agent add NAME:PROVIDER --role ROLE [--window NAME|--window-class CLASS] --hidden --json
      添加运行时代理，不改写 ccb.config。
  ccb agent remove NAME|--agents a,b --policy park|unload --json
      暂停或卸载运行时代理。
  ccb agent park NAME|--agents a,b --json     暂停派发，保留面板。
  ccb agent resume NAME|--agents a,b --json   恢复派发。
  ccb agent release NAME --idle-only --json  按角色策略释放空闲代理。
  ccb loop capacity ensure --loop-id ID --profile worker=1 --profile code_reviewer=1 --json
      按 loop.role_profiles 规划动态代理容量。
  ccb loop topology propose|commit|reconcile|status|release --loop-id ID --json
      管理工作流拓扑。
  ccb loop run-once --loop-id ID --task TEXT --json
      执行一轮工作、评审、编排与检查，并保存结果。

维护与移动端：
  ccb maintenance status       查看维护心跳配置及状态。
  ccb maintenance tick         执行一次维护诊断。
  ccb mobile serve             启动当前项目的移动网关。
  ccb mobile devices           查看已配对设备。
  ccb mobile revoke <id>        撤销一个设备的配对。
  ccb install mobile           启动服务器级移动网关并显示配对二维码。

版本与工具：
  ccb version                  查看版本。
  ccb update [rich|mobile|VERSION] [--providers prompt|check|all|none] [--no-cache-cleanup]
  ccb uninstall [rich] | ccb reinstall
  ccb rich                     打开增强工作台。
  ccb rich uninstall           卸载增强工作台。
  ccb update rich              更新增强工作台。
  ccb update mobile            更新移动端组件。

角色：
  ccb roles list
  ccb roles install agentroles.ccb_self
  ccb roles update agentroles.ccb_self
  ccb roles add agentroles.ccb_self:codex
  ccb roles install agentroles.archi
  ccb roles update agentroles.archi
  ccb roles sync [path]
  ccb roles add agentroles.archi:codex
  ccb roles doctor agentroles.archi

语言：默认简体中文。设置 CCB_LANG=en 使用英文，CCB_LANG=auto 跟随系统语言。
""").strip()

COMMAND_HELP = {
    "kill": """用法：ccb kill [-f]
停止当前项目的 ccbd、代理及终端命名空间。
  ccb kill      正常停止项目。
  ccb kill -f   强制清理项目残留资源。
仅影响当前项目，不创建缺失的 .ccb。配置缺失或过期时仍可清理。
之后可用 ccb -n 重建运行状态，保留配置和托管历史。""",
    "ping": """用法：ccb ping <agent|all|ccbd>
查看缓存的代理或项目后台状态，仅供诊断。
  ccb ping demo   查看指定代理。
  ccb ping all    查看已挂载的全部代理。
  ccb ping ccbd   查看项目后台。""",
    "clear": """用法：ccb clear [agent_name|all]...
向指定代理发送原生 /clear 命令；不指定名称时处理所有已挂载的配置代理。
支持多个名称。清空对话上下文，不删除 .ccb 状态、工作区、认证、会话文件或日志。
需要重启进程时使用 ccb restart <agent>。""",
    "compact": """用法：ccb compact [agent_name|all]...
使用代理的原生压缩命令压缩上下文；不指定名称时处理所有已挂载的配置代理。
支持多个名称，不删除项目状态、工作区、认证、会话或日志。
缺少已验证原生压缩命令的提供者会被报告为不支持。""",
    "restart": """用法：ccb restart <agent_name>
通过当前后台重启一个已挂载代理。
代理正在工作、排队、投递回复或等待结果链继续时拒绝重启。
不支持 restart all、整窗口重启或直接修改底层终端。""",
    "config": """用法：ccb config <validate|effective|migrate|approve-commands|ui> ...
  ccb config validate [--json]                 验证当前项目配置。
  ccb config effective --json                  查看脱敏后的生效配置。
  ccb config approve-commands                  审阅并批准项目命令字段。
  ccb config migrate --to 3 --dry-run [--json]  预览 V2 到 V3 迁移。
  ccb config ui                               打开本地项目配置页面。
  ccb config ui --no-open [--port PORT]         启动页面服务，不打开浏览器。""",
    "reload": """用法：ccb reload [--dry-run]
应用支持的变更：视图调整、添加代理或窗口、移除空闲代理、替换同槽位空闲代理。
--dry-run 只验证并返回变更计划。
忙碌代理的移除或替换会进入等待状态。移动代理和任意布局调整需使用对应受控命令。
不会启动配置监视；输出保留 stage、plan_class 等稳定诊断字段。""",
    "doctor": """用法：ccb doctor [ps|logs <agent>|storage] [--output [PATH]]
诊断项目后台、代理、终端、依赖和存储状态。
--output 可保存诊断材料。ps 查看代理状态，logs 查看指定代理日志，storage 查看存储占用。""",
    "screen": """用法：ccb screen <agent> [--lines 0..1000] [--json]
读取指定代理的终端输出。--lines 控制行数，--json 输出结构化数据。""",
    "trace": """用法：ccb trace <submission_id|message_id|attempt_id|reply_id|job_id>
查看指定任务、消息、执行尝试或回复的完整关联链。""",
    "queue": """用法：ccb queue [--detail] <agent_name|all>
查看代理等待队列；--detail 展开事件详情，all 查看全项目。
这是观察摘要，不是完成凭据。需要追踪执行链时使用 ccb trace <id>。""",
    "followup": """用法：ccb followup <job_id> --message <text>
向正在执行的确切任务轮次补充说明。
传输不支持或轮次已过期时拒绝操作，不自动新建任务、替换提供者或重试。""",
    "theme": """用法：ccb theme [system|dark|light|+|-|solarized|tokyo|gruvbox|rose-pine]
不带参数时查看主题；+ / - 切换主题，system 跟随系统，light 为浅色，dark 为深色。
只修改 CCB 管理的界面配色；增强工作台的 WezTerm 也使用此主题设置。""",
}

def command_help(name: str) -> str | None:
    return COMMAND_HELP.get(name)
