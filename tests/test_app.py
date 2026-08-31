from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_from_activity():
    response = client.delete(
        "/activities/Chess%20Club/unregister?email=michael@mergington.edu"
    )

    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Unregistered michael@mergington.edu from Chess Club"

    activity_response = client.get("/activities")
    assert "michael@mergington.edu" not in activity_response.json()["Chess Club"]["participants"]
