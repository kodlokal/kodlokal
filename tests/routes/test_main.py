import pytest
from app.kodlokal_app import app, APP_NAME

app.config.from_pyfile('tests/config.py')


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


def test_main_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'server' in response.json
    assert response.json['server'] == f"{APP_NAME} Server"
