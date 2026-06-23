from fastapi.testclient import TestClient

from app import main


main.Base.metadata.create_all = lambda *args, **kwargs: None
main.create = lambda *args, **kwargs: None


class _Session:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def query(self, *args, **kwargs):
        class _Query:
            def count(self):
                return 0

        return _Query()


main.SessionLocal = lambda: _Session()


def test_health():
    client = TestClient(main.app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
