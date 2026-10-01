from app.config import Settings


def test_x_token_is_optional_in_settings():
    settings = Settings(_env_file=None)
    assert settings.x_bearer_token is None
