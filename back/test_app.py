import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_api_status(client):
    """Vérifie que la route API racine répond correctement."""
    res = client.get('/api')
    assert res.status_code == 200
    assert res.json['status'] == 'ok'


def test_leaderboard_endpoint(client):
    """Vérifie que la route du classement répond avec une liste."""
    res = client.get('/api/leaderboard')
    assert res.status_code == 200
    assert 'leaderboard' in res.json
    assert isinstance(res.json['leaderboard'], list)
