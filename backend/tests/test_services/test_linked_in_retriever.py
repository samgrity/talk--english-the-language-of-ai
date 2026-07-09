import pytest

from app.services.linked_in_retriever import get_linkedin_profile


@pytest.mark.asyncio
async def test_get_linkedin_profile_returns_local_profile_for_known_name():
    profile = await get_linkedin_profile("GrEg", "  Ceccarelli ")

    assert profile.startswith("# Greg Ceccarelli")
    assert "SpecStory" in profile


@pytest.mark.asyncio
async def test_get_linkedin_profile_returns_no_result_for_john_berryman():
    profile = await get_linkedin_profile("John", "Berryman")

    assert profile.startswith("ERROR:")
    assert "Could not find a LinkedIn profile for 'John Berryman'" in profile
