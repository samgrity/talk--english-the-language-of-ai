import pytest
from pydantic import ValidationError

from app.core.enums import UpdateType
from app.services.ai_reviewer import AIReviewOutput


def test_ai_review_output_accepts_non_empty_fields():
    output = AIReviewOutput(
        update_type=UpdateType.RECOMMEND_ADVANCE,
        internal_notes="[✓] Experience fit: confirmed.\n\nRecommendation: recommend_advance",
        correspondence="Hi Greg, thanks for applying. We'd like to move you forward.",
    )

    assert output.internal_notes.startswith("[✓]")
    assert len(output.correspondence) > 0


@pytest.mark.parametrize("value", ["", "   ", "\n\t  "])
def test_ai_review_output_rejects_blank_internal_notes(value: str):
    with pytest.raises(ValidationError):
        AIReviewOutput(
            update_type=UpdateType.RECOMMEND_FOLLOW_UP,
            internal_notes=value,
            correspondence="We need more info.",
        )


@pytest.mark.parametrize("value", ["", "   ", "\n\t  "])
def test_ai_review_output_rejects_blank_correspondence(value: str):
    with pytest.raises(ValidationError):
        AIReviewOutput(
            update_type=UpdateType.RECOMMEND_ADVANCE,
            internal_notes="[✓] Looks good.\n\nRecommendation: recommend_advance",
            correspondence=value,
        )
