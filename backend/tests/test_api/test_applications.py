def test_list_applications_returns_data(client):
    response = client.get("/api/applications")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_application_by_id(client):
    listing = client.get("/api/applications")
    app_id = listing.json()[0]["id"]

    response = client.get(f"/api/applications/{app_id}")
    assert response.status_code == 200
    app = response.json()
    assert app["id"] == app_id
    assert "updates" in app
    assert app["company"]["verificationStatus"] in ["unverified", "verified", "flagged"]


def test_update_application_can_change_company_verification_status(client):
    listing = client.get("/api/applications")
    app_id = listing.json()[0]["id"]

    response = client.put(
        f"/api/applications/{app_id}",
        json={"companyVerificationStatus": "verified"},
    )
    assert response.status_code == 200

    verify = client.get(f"/api/applications/{app_id}")
    assert verify.status_code == 200
    assert verify.json()["company"]["verificationStatus"] == "verified"


def test_get_application_not_found(client):
    response = client.get("/api/applications/nonexistent")
    assert response.status_code == 404


def test_update_status_changes_application(client):
    listing = client.get("/api/applications")
    app_id = listing.json()[0]["id"]

    response = client.put(f"/api/applications/{app_id}/status", json={"status": "advanced"})
    assert response.status_code == 200

    verify = client.get(f"/api/applications/{app_id}")
    assert verify.status_code == 200
    assert verify.json()["screeningStatus"] == "advanced"


def test_add_update_sets_recruiter_and_status(client):
    listing = client.get("/api/applications?filter=all")
    app_id = listing.json()[0]["id"]

    response = client.post(
        f"/api/applications/{app_id}/updates",
        json={
            "update_type": "withdraw",
            "internal_notes": "No response from candidate.",
            "recruiter_id": "rev1",
        },
    )
    assert response.status_code == 200

    verify = client.get(f"/api/applications/{app_id}")
    assert verify.status_code == 200
    app = verify.json()
    assert app["screeningStatus"] == "withdrawn"
    assert app["updates"][-1]["recruiter_id"] == "rev1"


def test_add_update_rejects_unknown_recruiter(client):
    listing = client.get("/api/applications?filter=all")
    app_id = listing.json()[0]["id"]

    response = client.post(
        f"/api/applications/{app_id}/updates",
        json={
            "update_type": "general_update",
            "internal_notes": "Testing invalid recruiter",
            "recruiter_id": "not-a-recruiter",
        },
    )
    assert response.status_code == 400


def test_add_follow_up_requires_correspondence(client):
    listing = client.get("/api/applications?filter=all")
    app_id = listing.json()[0]["id"]

    response = client.post(
        f"/api/applications/{app_id}/updates",
        json={
            "update_type": "follow_up",
            "internal_notes": "Need more details",
            "recruiter_id": "rev1",
        },
    )
    assert response.status_code == 400


def test_filters_status_assignee_and_search(client):
    completed = client.get("/api/applications?filter=completed")
    assert completed.status_code == 200
    assert all(app["screeningStatus"] in ["advanced", "declined", "withdrawn"] for app in completed.json())

    by_assignee = client.get("/api/applications?filter=all&assignee_id=rev1")
    assert by_assignee.status_code == 200

    by_search = client.get("/api/applications?search=john")
    assert by_search.status_code == 200
    assert any("john" in f"{app['firstName']} {app['lastName']}".lower() for app in by_search.json())

    specific_status = client.get("/api/applications?filter=waiting_for_ai")
    assert specific_status.status_code == 200
    assert all(app["screeningStatus"] == "waiting_for_ai" for app in specific_status.json())


def test_filter_validation_rejects_invalid_enum(client):
    response = client.get("/api/applications?filter=invalid")
    assert response.status_code == 422
