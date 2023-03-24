mod utils;

fn main() {
    let config = utils::configreader::read_config("swish.toml");
    if config.is_err() {
        let err = config.unwrap_err();
        panic!("Could not read the config:\n{}", err);
    } else {
        println!("config: {:?}", config.unwrap());
    }

    
}
