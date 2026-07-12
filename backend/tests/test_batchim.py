import uuid
import pytest
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_list_batchim(client, db_session: AsyncSession):
    from app.models.batchim import BatchimRule
    rule = BatchimRule(
        rule_type="basic", title="ㄱ 받침",
        description="音节末尾ㄱ发[k]音", order_index=1,
    )
    db_session.add(rule)
    await db_session.commit()

    resp = await client.get("/api/v1/batchim")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
