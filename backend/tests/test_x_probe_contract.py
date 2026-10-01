from app.config import Settings


def test_probe_can_run_without_secret_configured():
    settings = Settings(_env_file=None)
    assert settings.x_bearer_token is None
