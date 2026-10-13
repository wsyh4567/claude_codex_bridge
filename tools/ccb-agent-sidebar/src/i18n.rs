//! Presentation-only translations. Protocol values and user text stay unchanged.
pub fn is_chinese() -> bool {
    language_is_chinese(std::env::var("CCB_LANG").ok().as_deref())
}

pub fn language_is_chinese(language: Option<&str>) -> bool {
    match language.unwrap_or("zh").trim().to_lowercase().as_str() {
        "en" | "english" => false,
        "auto" => std::env::var("LC_ALL").or_else(|_| std::env::var("LC_MESSAGES"))
            .or_else(|_| std::env::var("LANG"))
            .map(|v| v.to_lowercase().starts_with("zh")).unwrap_or(true),
        value => !value.starts_with("en"),
    }
}

pub fn tr(text: &str) -> &str { translate(text, is_chinese()) }

pub fn translate(text: &str, chinese: bool) -> &str {
    if !chinese { return text; }
    match text {
        "Comms" => "通信",
        "Tips" => "快捷键",
        "ccbd unavailable" => "无法连接 CCB 后台",
        "waiting for ProjectView" => "正在加载项目状态",
        "stale ProjectView" => "项目状态已过期，正在重连",
        "no comms" => "暂无通信记录",
        "no tips" => "暂无快捷键提示",
        "ccbd ✕" => "后台未连接",
        "config ✕" => "配置错误",
        "config ui ✕" => "配置页面错误",
        "config ui !" => "请打开配置页面",
        "config error" => "配置错误",
        "config ui" => "配置页面",
        "config ui: opening..." => "正在打开配置页面…",
        "config ui open manually" => "请手动打开配置页面",
        "config ui failed" => "配置页面启动失败",
        "status unavailable; click to retry" => "无法获取状态，点击重试",
        "session closed; click to reopen" => "配置会话已关闭，点击重新打开",
        "exited before reporting a URL" => "配置服务提前退出，未返回地址",
        " [login]" => " [请登录]",
        "focus" => "当前窗口",
        "focus warn" => "窗口异常",
        "warn" => "异常",
        "drain" => "等待重载",
        "waiting" => "等待中",
        "ready" => "就绪",
        "que" => "排队",
        "inj" => "发送中",
        "run" => "执行中",
        "idle" => "空闲",
        "r-q" => "回复排队",
        "back" | "rep" => "回复中",
        "orph" => "失联",
        "ok" => "完成",
        "snd" => "发送中",
        "err" => "失败",
        "cnl" => "已取消",
        "C-b d  detach" => "C-b d  断开界面连接",
        "C-b h/j/k/l pane" => "C-b h/j/k/l  切换面板",
        "C-b H/J/K/L resize" => "C-b H/J/K/L  调整大小",
        "C-b o  next pane" => "C-b o  下一个面板",
        "C-b z  zoom" => "C-b z  最大化 / 还原",
        "C-b w  tree" => "C-b w  窗口列表",
        "C-b n/p next/prev" => "C-b n/p  下一个 / 上一个",
        "C-b 0-9 jump win" => "C-b 0-9  切换窗口",
        "C-b [  copy mode" => "C-b [  进入复制模式",
        "copy: PgUp/PgDn" => "复制模式：PgUp/PgDn 翻页",
        "copy: v select" => "复制模式：v 选择",
        "copy: y yank" => "复制模式：y 复制",
        "copy: q exit" => "复制模式：q 退出",
        "C-b ]  paste" => "C-b ]  粘贴",
        "C-b c  new win" => "C-b c  新建窗口",
        "C-b ,  rename" => "C-b ,  重命名",
        "C-b ?  keys" => "C-b ?  快捷键说明",
        _ => text,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn defaults_to_chinese_and_allows_english() {
        assert!(language_is_chinese(None));
        assert!(language_is_chinese(Some("zh-CN")));
        assert!(!language_is_chinese(Some("en")));
    }
    #[test]
    fn translates_labels_and_preserves_custom_text() {
        assert_eq!(translate("Comms", true), "通信");
        assert_eq!(translate("no comms", true), "暂无通信记录");
        assert_eq!(translate("Comms", false), "Comms");
        assert_eq!(translate("My custom tip", true), "My custom tip");
    }
}
