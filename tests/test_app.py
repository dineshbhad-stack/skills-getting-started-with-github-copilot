import copy

from fastapi.testclient import TestClient

from src import app as app_module

client = TestClient(app_module.app)

ORIGINAL_ACTIVITIES = copy.deepcopy(app_module.activities)


def reset_activities():
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))


def test_get_activities_returns_data():
    reset_activities()

    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert "participants" in payload["Chess Club"]


def test_signup_for_activity_success():
    reset_activities()
    email = "newstudent@mergington.edu"

    response = client.post("/activities/Chess%20Club/signup?email=" + email)

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"
    assert email in app_module.activities["Chess Club"]["participants"]


def test_duplicate_signup_is_rejected():
    reset_activities()
    email = "michael@mergington.edu"

    response = client.post("/activities/Chess%20Club/signup?email=" + email)

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_after_reaching_capacity_is_rejected():
    reset_activities()
    activity = app_module.activities["Chess Club"]
    activity["participants"] = [
        f"student{i}@mergington.edu" for i in range(activity["max_participants"])
    ]

    response = client.post("/activities/Chess%20Club/signup?email=overflow@mergington.edu")

    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"


def test_unregister_participant_from_activity():
    reset_activities()
    email = "michael@mergington.edu"

    response = client.delete("/activities/Chess%20Club/unregister?email=" + email)

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from Chess Club"
    assert email not in app_module.activities["Chess Club"]["participants"]
