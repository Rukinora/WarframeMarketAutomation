



// use tauri::{Manager, AppHandle};
// use serde::{Serialize, Deserialize};
// use std::fs;
// use std::path::PathBuf;

// #[derive(Serialize, Deserialize)]
// pub struct Config {
//     pub min_plat_price: i32,
//     pub time: f64,
//     pub warframe_link: String,
// }

// fn get_config_path(app: &AppHandle) -> PathBuf {
//     let mut path = app.path().app_config_dir().unwrap();
//     std::fs::create_dir_all(&path).unwrap();
//     path.push("config.json");
//     path
// }

// fn load_config(path: &PathBuf) -> Config {
//     if path.exists() {
//         serde_json::from_str(&fs::read_to_string(path).unwrap()).unwrap()
//     } else {
//         Config {
//             min_plat_price: 0,
//             time: 1.0,
//             warframe_link: String::new(),
//         }
//     }
// }

// #[tauri::command]
// fn save_time(app: AppHandle, value: f64) -> Result<(), String> {
//     println!("SAVE COMMAND CALLED");

//     let path = get_config_path(&app);
//     let mut config = load_config(&path);

//     config.time = value;

//     fs::write(path, serde_json::to_string_pretty(&config).unwrap())
//         .map_err(|e| e.to_string())?;

//     Ok(())
// }