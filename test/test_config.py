from nycschools import config


def test_get_config():
    """Get the current/default configuration."""

    print("got config", config)
    print("data dir", config.data_dir)

    assert config.config_file is not None
    assert config.data_dir is not None
