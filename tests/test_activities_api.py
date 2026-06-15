"""Backend API tests for activities endpoints using AAA structure."""


def test_get_activities_returns_all_activities_with_expected_shape(client):
    # Arrange
    required_keys = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(data, dict)
    assert len(data) == 9
    assert "Chess Club" in data

    for activity_details in data.values():
        assert required_keys.issubset(activity_details.keys())


def test_signup_successfully_adds_new_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    data = response.json()
    activities_response = client.get("/activities")
    activities_data = activities_response.json()

    # Assert
    assert response.status_code == 200
    assert data["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities_data[activity_name]["participants"]


def test_signup_returns_400_when_student_already_signed_up(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup", params={"email": existing_email}
    )
    data = response.json()

    # Assert
    assert response.status_code == 400
    assert data["detail"] == "Student already signed up for this activity"


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Activity"
    email = "someone@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    data = response.json()

    # Assert
    assert response.status_code == 404
    assert data["detail"] == "Activity not found"


def test_unregister_successfully_removes_participant(client):
    # Arrange
    activity_name = "Tennis Club"
    email = "james@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants", params={"email": email}
    )
    data = response.json()
    activities_response = client.get("/activities")
    activities_data = activities_response.json()

    # Assert
    assert response.status_code == 200
    assert data["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in activities_data[activity_name]["participants"]


def test_unregister_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Activity"
    email = "someone@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants", params={"email": email}
    )
    data = response.json()

    # Assert
    assert response.status_code == 404
    assert data["detail"] == "Activity not found"


def test_unregister_returns_404_for_missing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    missing_email = "absent@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants", params={"email": missing_email}
    )
    data = response.json()

    # Assert
    assert response.status_code == 404
    assert data["detail"] == "Participant not found for this activity"


def test_signup_then_unregister_flow_for_same_participant(client):
    # Arrange
    activity_name = "Drama Club"
    email = "flow.student@mergington.edu"

    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup", params={"email": email}
    )
    mid_state = client.get("/activities").json()
    unregister_response = client.delete(
        f"/activities/{activity_name}/participants", params={"email": email}
    )
    final_state = client.get("/activities").json()

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    assert email in mid_state[activity_name]["participants"]
    assert email not in final_state[activity_name]["participants"]
