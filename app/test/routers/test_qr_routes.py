from unittest.mock import patch

def test_generate_qr(test_client, auth_headers):
    mocked_uuid = "b9d9a2bf-a0c9-4642-b3d6-6587baad1e6d"
    with patch("uuid.uuid4", return_value=mocked_uuid):
        qr_data = {
            "url": "https://google.com/",
            "color": "#0000FF",
            "size": 400
        }
        response = test_client.post("/qr/", json=qr_data, headers=auth_headers)
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "image/png"
        assert response.headers["Content-Disposition"] == f'attachment; filename="qr_{mocked_uuid}.png"'

def test_get_all_qr_codes(test_client, test_user, auth_headers):
    response = test_client.get(
        f"/qr/", headers=auth_headers
    )
    assert response.status_code == 200

    qr_codes = response.json()
    qr_codes = qr_codes['qr_codes']

    assert isinstance(qr_codes, list)
    assert len(qr_codes) > 0

    qr_code = qr_codes[0]
    assert "uuid" in qr_code
    assert "url" in qr_code
    assert "color" in qr_code
    assert "size" in qr_code

def test_update_qr_code(test_client, auth_headers):
    qr_uuid = "b9d9a2bf-a0c9-4642-b3d6-6587baad1e6d"

    qr_data = {
        "url": "https://updated-qr-url.com",
        "color": "#33FF57",
        "size": 400,
    }
    response = test_client.patch(
        f"/qr/{qr_uuid}", json=qr_data, headers=auth_headers
    )

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/png"
    assert response.headers["Content-Disposition"] == f'attachment; filename="qr_{qr_uuid}.png"'
