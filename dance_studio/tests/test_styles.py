def test_styles_crud(client):
    created = client.post("/styles", json={"name": "Hip-hop"})
    assert created.status_code == 201
    style_id = created.get_json()["id"]

    assert len(client.get("/styles").get_json()) == 1
    assert client.get(f"/styles/{style_id}").status_code == 200
    assert client.put(f"/styles/{style_id}", json={"name": "Contemporary"}).status_code == 200
    assert client.delete(f"/styles/{style_id}").status_code == 200
