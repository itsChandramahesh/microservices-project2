from fastapi.testclient import TestClient

from app import main


async def _noop():
    return None


def test_health():
    main.redis.ping = _noop
    client = TestClient(main.app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
