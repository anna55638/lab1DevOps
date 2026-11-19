def test_classes_crud(client):
    author = client.post("/instructors", json={"name": "Instructor"}).get_json()["id"]
    genre = client.post("/styles", json={"name": "Hip-hop"}).get_json()["id"]
    publisher = client.post("/studios", json={"name": "Studio"}).get_json()["id"]

    payload = {
        "title": "Test Class",
        "instructor_id": author,
        "style_id": genre,
        "studio_id": publisher,
        "duration": 60,
    }

    created = client.post("/classes", json=payload)
    assert created.status_code == 201
    book_id = created.get_json()["id"]

    assert client.get("/classes").status_code == 200
    assert client.get(f"/classes/{book_id}").status_code == 200

    payload["title"] = "Updated Class"
    assert client.put(f"/classes/{book_id}", json=payload).status_code == 200

    assert client.delete(f"/classes/{book_id}").status_code == 200
    assert client.get(f"/classes/{book_id}").status_code == 404
