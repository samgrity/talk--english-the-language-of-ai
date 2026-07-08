def test_candidate_message_hook_triggers_ai_screen(client):
    from pydantic_ai.models.test import TestModel
    from app.services.application_service import ai_reviewer
    from tests.conftest import override_no_capabilities

    listing = client.get("/api/applications?filter=all")
    app_id = listing.json()[0]["id"]

    with ai_reviewer.override(model=TestModel(call_tools=[])), override_no_capabilities(ai_reviewer):
        response = client.post(
            "/api/hooks/email/candidate-message",
            json={
                "application_id": app_id,
                "correspondence": "Sharing additional documents from candidate.",
            },
        )
    assert response.status_code == 200

    updated = client.get(f"/api/applications/{app_id}").json()
    assert updated["screeningStatus"] == "waiting_for_recruiter"
    assert updated["updates"][-1]["actor"] == "ai_agent"


def test_trigger_ai_screen_hook_triggers_ai_screen(client):
    from pydantic_ai.models.test import TestModel
    from app.services.application_service import ai_reviewer
    from tests.conftest import override_no_capabilities

    listing = client.get("/api/applications?filter=all")
    app_id = listing.json()[0]["id"]

    with ai_reviewer.override(model=TestModel(call_tools=[])), override_no_capabilities(ai_reviewer):
        response = client.post(
            "/api/hooks/applications/trigger-ai-screen",
            json={"application_id": app_id},
        )
    assert response.status_code == 200

    updated = client.get(f"/api/applications/{app_id}").json()
    assert updated["screeningStatus"] == "waiting_for_recruiter"
    assert updated["updates"][-1]["actor"] == "ai_agent"


def test_hooks_return_404_for_unknown_application(client):
    response = client.post(
        "/api/hooks/email/candidate-message",
        json={"application_id": "missing", "correspondence": "Hello"},
    )
    assert response.status_code == 404

    response = client.post(
        "/api/hooks/applications/trigger-ai-screen",
        json={"application_id": "missing"},
    )
    assert response.status_code == 404
