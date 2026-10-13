#![cfg(windows)]
use ccb_agent_sidebar::client::CcbdClient;
use serde_json::{json, Value};
use std::io::{BufRead, BufReader, Write};
use std::net::TcpListener;
use std::path::PathBuf;
use std::time::{SystemTime, UNIX_EPOCH};

fn fixture(address: &str) -> PathBuf {
    let dir = std::env::temp_dir().join(format!("ccb-sidebar-test-{}-{}", std::process::id(),
        SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos()));
    std::fs::create_dir(&dir).unwrap();
    let token = dir.join("test-token.json");
    std::fs::write(&token, json!({"schema":"ccbd-control-plane-token-v1",
        "generation":"test", "token":"test-only"}).to_string()).unwrap();
    std::fs::write(dir.join("control-plane-endpoint.json"), json!({"kind":"tcp_loopback",
        "address":address,"token_ref":token,"generation":"test"}).to_string()).unwrap();
    dir
}

#[test]
fn authenticates_before_request_and_reads_framed_project_view() {
    let listener = TcpListener::bind("127.0.0.1:0").unwrap();
    let dir = fixture(&listener.local_addr().unwrap().to_string());
    let server = std::thread::spawn(move || {
        let (mut socket, _) = listener.accept().unwrap();
        let mut reader = BufReader::new(socket.try_clone().unwrap());
        let mut line = String::new();
        reader.read_line(&mut line).unwrap();
        let auth: Value = serde_json::from_str(&line).unwrap();
        assert_eq!(auth["schema"], "ccbd-control-plane-token-v1");
        assert_eq!(auth["token"], "test-only");
        writeln!(socket, "{}", json!({"schema":"ccbd-control-plane-token-ack-v1","ok":true})).unwrap();
        line.clear();
        reader.read_line(&mut line).unwrap();
        let request: Value = serde_json::from_str(&line).unwrap();
        assert_eq!(request["op"], "project_view");
        assert_eq!(request["api_version"], 2);
        writeln!(socket, "{}", json!({"api_version":2,"ok":true,"view":{
            "project":{"display_name":"test"},"namespace":{"epoch":1},
            "windows":[],"agents":[],"comms":[]},"cache":{"sequence":7,"ttl_ms":1000}})).unwrap();
    });
    let view = CcbdClient::new(dir.join("ccbd.sock")).project_view().unwrap();
    assert_eq!(view.cache.sequence, 7);
    server.join().unwrap();
    std::fs::remove_dir_all(dir).unwrap();
}

#[test]
fn rejects_remote_endpoint() {
    let dir = fixture("192.0.2.1:1234");
    let error = CcbdClient::new(dir.join("ccbd.sock")).project_view().unwrap_err();
    assert!(error.contains("loopback"));
    std::fs::remove_dir_all(dir).unwrap();
}

#[test]
fn rejects_authentication_ack_without_sending_rpc() {
    let listener = TcpListener::bind("127.0.0.1:0").unwrap();
    let dir = fixture(&listener.local_addr().unwrap().to_string());
    let server = std::thread::spawn(move || {
        let (mut socket, _) = listener.accept().unwrap();
        let mut reader = BufReader::new(socket.try_clone().unwrap());
        let mut line = String::new();
        reader.read_line(&mut line).unwrap();
        writeln!(socket, "{}", json!({"schema":"wrong","ok":true})).unwrap();
        line.clear();
        assert_eq!(reader.read_line(&mut line).unwrap(), 0);
    });
    let error = CcbdClient::new(dir.join("ccbd.sock")).project_view().unwrap_err();
    assert!(error.contains("authentication rejected"));
    server.join().unwrap();
    std::fs::remove_dir_all(dir).unwrap();
}
