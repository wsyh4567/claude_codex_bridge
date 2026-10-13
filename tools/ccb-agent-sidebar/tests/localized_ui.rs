use ccb_agent_sidebar::i18n::is_chinese;
use ccb_agent_sidebar::model::ProjectViewResponse;
use ccb_agent_sidebar::tui::{SidebarApp, draw};
use ratatui::{Terminal, backend::TestBackend};

#[test]
fn renders_localized_panels_and_preserves_agent_identity() {
    let response: ProjectViewResponse = serde_json::from_value(serde_json::json!({
        "view": {
            "namespace": {"active_window": "main"},
            "windows": [{"name":"main", "active":true}],
            "agents": [{"name":"demo", "display_name":"我的代理", "window":"main", "provider":"Codex"}],
            "comms": []
        }
    })).unwrap();
    let mut app = SidebarApp::new("main".into());
    app.apply_response(response);
    for width in [24, 54] {
        let mut terminal = Terminal::new(TestBackend::new(width, 38)).unwrap();
        terminal.draw(|frame| draw(frame, &app)).unwrap();
        let rendered = terminal.backend().to_string();
        assert!(rendered.contains("main"));
        assert!(rendered.contains("我的代理"));
        assert!(rendered.contains(if is_chinese() { "通信" } else { "Comms" }));
        assert!(rendered.contains(if is_chinese() { "快捷键" } else { "Tips" }));
        assert!(rendered.contains(if is_chinese() { "暂无通信记录" } else { "no comms" }));
    }
}
