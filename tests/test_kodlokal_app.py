import pytest
from flask import Flask

from app.kodlokal_app import app

app.config.from_pyfile('tests/config.py')


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_app_name():
    """Test the app name."""
    assert app.name == 'kodlokal'


def test_config_from_pyfile():
    """Test that the app's config is loaded from the config file."""
    assert app.config['MODELS_FOLDER'] == './models/'


def test_index_route(client):
    """Test the index route."""
    expected = b'{"server":"kodlokal Server"}\n'
    response = client.get('/')
    assert response.status_code == 200
    assert expected in response.data
