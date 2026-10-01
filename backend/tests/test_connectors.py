import pytest

from app.connectors.base import ConnectorPost
from app.connectors.mock_connector import MockConnector


@pytest.mark.asyncio
async def test_mock_connector_filters_posts():
    connector = MockConnector([
        ConnectorPost(platform="mock", external_id="1", text="سرمایه گذاری در پروژه"),
        ConnectorPost(platform="mock", external_id="2", text="خبر ورزشی"),
    ])

    posts = await connector.search_posts("سرمایه")
    assert len(posts) == 1
    assert posts[0].external_id == "1"
