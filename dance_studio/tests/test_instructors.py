def test_instructors_crud(client):
    created = client.post("/instructors", json={"name": "Test Instructor"})
    assert created.status_code == 201
    instructor_id = created.get_json()["id"]

    assert client.get("/instructors").status_code == 200
    assert client.get(f"/instructors/{instructor_id}").status_code == 200

    updated = client.put(f"/instructors/{instructor_id}", json={"name": "Updated Instructor"})
    assert updated.status_code == 200

    deleted = client.delete(f"/instructors/{instructor_id}")
    assert deleted.status_code == 200
    assert client.get(f"/instructors/{instructor_id}").status_code == 404
