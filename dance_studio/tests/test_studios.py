def test_studios_crud(client):
    created = client.post("/studios", json={"name": "Test Studio"})
    assert created.status_code == 201
    studio_id = created.get_json()["id"]

    assert client.get("/studios").status_code == 200
    assert client.get(f"/studios/{studio_id}").status_code == 200
    assert client.put(f"/studios/{studio_id}", json={"name": "New Studio"}).status_code == 200
    assert client.delete(f"/studios/{studio_id}").status_code == 200
