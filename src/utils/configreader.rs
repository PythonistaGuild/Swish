#![allow(dead_code)]
use serde::Deserialize;
use std::fs;


pub fn read_config(path: &str) -> Result<Config, toml::de::Error> {
    let data = fs::read_to_string(path).expect(format!("Unable to find config at {:}", path).as_str());
    let config: Config = toml::from_str(&data.as_str())?;
    Ok(config)
}


#[derive(Deserialize, Debug)]
pub struct Config {
    server: Server,
    rotation: Rotation,
    search: Search,
    logging: Logging
}

#[derive(Deserialize, Debug)]
struct Server {
    host: String,
    port: u16,
    password: String
}

#[derive(Deserialize, Debug)]
pub enum RotationMethod {
    Banned,
    Nanosecond
}

#[derive(Deserialize, Debug)]
struct Rotation {
    enabled: bool,
    method: RotationMethod,
    blocks: Vec<String>
}

#[derive(Deserialize, Debug)]
struct Search {
    max_results: u16
}

#[derive(Deserialize, Debug)]
struct Logging {
    path: String,
    backup_count: u8,
    max_bytes: u32,
    levels: LoggingLevel
}

#[derive(Deserialize, Debug)]
pub enum LoggingLevels {
    OFF,
    INFO,
    DEBUG,
    WARNING,
    ERROR
}

#[derive(Deserialize, Debug)]
struct LoggingLevel {
    swish: LoggingLevels,
    actix: LoggingLevels
}