from fastapi import APIRouter, HTTPException
from app.services.scenario_service import get_all_scenarios, get_scenario, generate_ai_response

router = APIRouter(prefix="/scenarios", tags=["AI情景对话"])


@router.get("")
async def list_scenarios():
    """List all practice scenarios"""
    return get_all_scenarios()


@router.get("/{scenario_id}")
async def get_scenario_detail(scenario_id: str):
    """Get full scenario context and starter"""
    scenario = get_scenario(scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="场景不存在")
    return scenario


@router.post("/{scenario_id}/chat")
async def chat(scenario_id: str, body: dict):
    """Send a message in a scenario conversation"""
    user_message = body.get("message", "")
    if not user_message:
        raise HTTPException(status_code=400, detail="message is required")
    return generate_ai_response(scenario_id, user_message)
