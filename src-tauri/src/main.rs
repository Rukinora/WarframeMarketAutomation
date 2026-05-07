// #![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::{AppHandle, Manager};
use serde::{Serialize, Deserialize};
use std::fs;
use std::path::PathBuf;
use std::process::{Command, Child};
use std::sync::Mutex;
static mut CHILD: Option<Child> = None;

#[derive(Serialize, Deserialize)]
struct Config {
    min_plat_price: i32,
    time: f64,
    warframe_link: String,
    #[serde(default)]  // ✅ If field is missing, default = false
    is_setup_complete: bool, // 👈 ADD THIS
}


#[tauri::command]
fn is_setup_complete(app: AppHandle) -> bool {
    let path = get_config_path(&app);
    let config = load_config(&path);
    config.is_setup_complete
}

fn get_config_path(app: &AppHandle) -> PathBuf {
    let mut path = app.path().app_config_dir().unwrap();
    std::fs::create_dir_all(&path).unwrap();
    path.push("config.json");
    path
}

fn load_config(path: &PathBuf) -> Config {
    if path.exists() {
        let contents = fs::read_to_string(path).unwrap();
        serde_json::from_str(&contents).unwrap()
    } else {
        let config = Config {
            min_plat_price: 0,
            time: 1.0,
            warframe_link: "https://warframe.market/".to_string(),
            is_setup_complete: false, // 👈 ADD THIS
        };

        // ✅ CREATE FILE immediately with defaults
        save_config(path, &config);

        println!("Created default config with Warframe link");

        config
    }
}

fn save_config(path: &PathBuf, config: &Config) {
    let json = serde_json::to_string_pretty(config).unwrap();
    fs::write(path, json).unwrap();
}

#[tauri::command]
fn get_min_plat_price(app: AppHandle) -> i32 {
    let path = get_config_path(&app);
    let config = load_config(&path);
    config.min_plat_price
}

#[tauri::command]
fn save_time(app: AppHandle, value: f64) {
    let path = get_config_path(&app);
    let mut config = load_config(&path);
    config.time = value;
    config.is_setup_complete;
    save_config(&path, &config);
}

#[tauri::command]
fn save_warframe_link(app: AppHandle, value: String) {
    let path = get_config_path(&app);
    let mut config = load_config(&path);
    config.warframe_link = value;
    config.is_setup_complete = true; // 👈 THIS IS THE KEY
    save_config(&path, &config);
}

#[tauri::command]
fn save_min_plat_price(app: AppHandle, value: i32) {
    let path = get_config_path(&app);
    let mut config = load_config(&path);
    config.min_plat_price = value;
    save_config(&path, &config);
}

#[tauri::command]
fn handle_button_click(app: tauri::AppHandle, item: String, action: String) -> Result<(), String> {

    unsafe {
        if let Some(child) = CHILD.as_mut() {
            println!("Killing old process...");
            let _ = child.kill();
            let _ = child.wait();

            // ✅ kill ONLY selenium-related stuff
            let _ = Command::new("taskkill")
                .args([
                    "/F",
                    "/FI",
                    "IMAGENAME eq chrome.exe",
                    "/FI",
                    "COMMANDLINE eq *ChromeAutomationProfile*"
                ])
                .output();
        }

        let exe_path = app
            .path()
            .resource_dir()
            .map_err(|e| e.to_string())?
            .join("bin")
            .join("main.exe");

        let child = Command::new(exe_path)
            .arg("--item")
            .arg(item)
            .arg("--action")
            .arg(action)
            .spawn()
            .map_err(|e| e.to_string())?;

        CHILD = Some(child);
    }

    Ok(())
}

fn main() {
    println!("APP STARTED");

    

    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            save_time,
            save_warframe_link,
            save_min_plat_price,
            handle_button_click,
            is_setup_complete
            
        ])
        .run(tauri::generate_context!())
        .expect("error running app");
}