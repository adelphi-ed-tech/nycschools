from nycschools import config


def test_get_config():
    """Get the current/default configuration."""
    assert config.data_dir is not None
    assert config.urls is not None
