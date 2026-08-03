import io
import os
import json
import pytest
from web_app import app

@pytest.fixture
def client(tmp_path):
    # create uploads in tmp_path and point app to it
    uploads = tmp_path / "uploads"
    uploads.mkdir()
    app.config['UPLOAD_FOLDER'] = str(uploads)
    with app.test_client() as client:
        yield client

def test_root_get(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Document Scanner' in rv.data

def test_process_and_downloads(client, tmp_path):
    # create two sample files
    f1 = tmp_path / 'a.txt'
    f2 = tmp_path / 'b.txt'
    f1.write_text('hello sample sample word')
    f2.write_text('sample word other')

    data = {
        'file1': (open(str(f1), 'rb'), 'a.txt'),
        'file2': (open(str(f2), 'rb'), 'b.txt'),
        'term': 'sample'
    }

    rv = client.post('/', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert rv.status_code == 200
    assert b'sample' in rv.data

    # test download_matches
    rv2 = client.get('/download_matches?f1=a.txt&f2=b.txt')
    assert rv2.status_code == 200
    text = rv2.data.decode('utf-8')
    assert 'sample' in text

    # test export_json
    rv3 = client.get('/export_json?f1=a.txt&f2=b.txt')
    assert rv3.status_code == 200
    payload = json.loads(rv3.data)
    assert payload['file1'] == 'a.txt'
    assert 'sample' in payload['matches']

    # test huffman_image returns PNG
    rv4 = client.get('/huffman_image?f=a.txt')
    assert rv4.status_code == 200
    assert rv4.content_type == 'image/png'