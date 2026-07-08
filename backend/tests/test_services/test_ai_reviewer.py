import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.ai_reviewer import _try_algorithmic_handling
from app.core.enums import CompanyVerificationStatus, UpdateType

@pytest.mark.asyncio
async def test_algorithmic_company_flagged():
    mock_app = MagicMock()
    mock_app.firstName = "Test"
    mock_app.email = "test@example.com"
    mock_app.seniorityLevel = "Senior"
    mock_app.company.verificationStatus = CompanyVerificationStatus.FLAGGED
    mock_app.company.siteUrl = "example.com"
    
    mock_service = AsyncMock()
    
    result = await _try_algorithmic_handling("app_1", mock_app, mock_service)
    
    assert result is True
    mock_service.add_update.assert_called_once()
    assert mock_service.add_update.call_args.kwargs["update_type"] == UpdateType.RECOMMEND_DECLINE


@pytest.mark.asyncio
async def test_algorithmic_junior_not_edu():
    mock_app = MagicMock()
    mock_app.firstName = "Test"
    mock_app.email = "test@example.com"
    mock_app.seniorityLevel = "junior"
    mock_app.company.verificationStatus = CompanyVerificationStatus.UNVERIFIED
    mock_app.company.siteUrl = "example.com"
    
    mock_service = AsyncMock()
    
    result = await _try_algorithmic_handling("app_1", mock_app, mock_service)
    
    assert result is True
    mock_service.add_update.assert_called_once()
    assert mock_service.add_update.call_args.kwargs["update_type"] == UpdateType.RECOMMEND_DECLINE


@pytest.mark.asyncio
async def test_algorithmic_shared_email():
    mock_app = MagicMock()
    mock_app.firstName = "Test"
    mock_app.email = "info@example.com"
    mock_app.seniorityLevel = "Senior"
    mock_app.company.verificationStatus = CompanyVerificationStatus.UNVERIFIED
    mock_app.company.siteUrl = "example.com"
    
    mock_service = AsyncMock()
    
    result = await _try_algorithmic_handling("app_1", mock_app, mock_service)
    
    assert result is True
    mock_service.add_update.assert_called_once()
    assert mock_service.add_update.call_args.kwargs["update_type"] == UpdateType.RECOMMEND_FOLLOW_UP


@pytest.mark.asyncio
async def test_algorithmic_personal_email():
    mock_app = MagicMock()
    mock_app.firstName = "Test"
    mock_app.email = "test@gmail.com"
    mock_app.seniorityLevel = "Senior"
    mock_app.company.verificationStatus = CompanyVerificationStatus.UNVERIFIED
    mock_app.company.siteUrl = "example.com"
    
    mock_service = AsyncMock()
    
    result = await _try_algorithmic_handling("app_1", mock_app, mock_service)
    
    assert result is True
    mock_service.add_update.assert_called_once()
    assert mock_service.add_update.call_args.kwargs["update_type"] == UpdateType.RECOMMEND_FOLLOW_UP


@pytest.mark.asyncio
async def test_algorithmic_company_verified_domain_match():
    mock_app = MagicMock()
    mock_app.firstName = "Test"
    mock_app.email = "test@example.com"
    mock_app.seniorityLevel = "Senior"
    mock_app.company.verificationStatus = CompanyVerificationStatus.VERIFIED
    mock_app.company.siteUrl = "example.com"
    
    mock_service = AsyncMock()
    
    result = await _try_algorithmic_handling("app_1", mock_app, mock_service)
    
    assert result is True
    mock_service.add_update.assert_called_once()
    assert mock_service.add_update.call_args.kwargs["update_type"] == UpdateType.RECOMMEND_ADVANCE


@pytest.mark.asyncio
async def test_algorithmic_no_match():
    mock_app = MagicMock()
    mock_app.firstName = "Test"
    mock_app.email = "test@example.com"
    mock_app.seniorityLevel = "Senior"
    mock_app.company.verificationStatus = CompanyVerificationStatus.UNVERIFIED
    mock_app.company.siteUrl = "example.com"
    
    mock_service = AsyncMock()
    
    result = await _try_algorithmic_handling("app_1", mock_app, mock_service)
    
    assert result is False
    mock_service.add_update.assert_not_called()
