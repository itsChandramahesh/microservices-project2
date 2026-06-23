from contextlib import contextmanager

from fastapi.testclient import TestClient

from app import main


main.Base.metadata.create_all = lambda *args, **kwargs: None
main.by_email = lambda *args, **kwargs: None
main.create = lambda *args, **kwargs: None


@contextmanager
def _session():
    class Dummy:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    yield Dummy()


main.SessionLocal = _session


def test_health():
    client = TestClient(main.app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
