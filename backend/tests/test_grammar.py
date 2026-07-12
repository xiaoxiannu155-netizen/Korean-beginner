import uuid
import pytest
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_list_grammar(client, db_session: AsyncSession):
    from app.models.grammar import GrammarPoint
    gp = GrammarPoint(
        title="N + 입니다", level=1,
        structure_formula="N + 입니다", explanation="正式陈述",
        order_index=1,
    )
    db_session.add(gp)
    await db_session.commit()

    resp = await client.get("/api/v1/grammar")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1


@pytest.mark.asyncio
async def test_get_grammar_404(client):
    resp = await client.get(f"/api/v1/grammar/{uuid.uuid4()}")
    assert resp.status_code == 404
