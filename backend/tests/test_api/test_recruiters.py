def test_list_recruiters(client):
    response = client.get("/api/recruiters")
    assert response.status_code == 200
    recruiters = response.json()
    assert isinstance(recruiters, list)
    assert len(recruiters) >= 3
    assert {"id", "name"}.issubset(recruiters[0].keys())
