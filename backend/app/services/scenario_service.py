"""AI scenario conversation service - pre-built scenarios for Korean practice"""
import random

# 10 predefined conversation scenarios
SCENARIOS = [
    {
        "id": "cafe",
        "title": "☕ 买咖啡",
        "title_ko": "카페에서 커피 주문하기",
        "description": "在咖啡厅点咖啡的对话练习",
        "difficulty": 1,
        "context": "你在首尔的一家咖啡厅。你想点一杯美式咖啡和一块蛋糕。",
        "starter": "어서 오세요, 주문하시겠어요?",
        "starter_zh": "欢迎光临，要点餐吗？",
        "tips": ["아이스 = 冰的", "뜨거운 = 热的", "사이즈 업 = 加大"],
        "expected_phrases": ["아메리카노 한 잔", "주세요", "얼마예요"],
    },
    {
        "id": "restaurant",
        "title": "🍽️ 餐厅点餐",
        "title_ko": "식당에서 주문하기",
        "description": "在韩国餐厅点餐的对话练习",
        "difficulty": 1,
        "context": "你在首尔的一家韩餐厅。你想点一份拌饭和一瓶水。",
        "starter": "주문하시겠어요? 메뉴는 여기 있습니다.",
        "starter_zh": "要点餐吗？菜单在这里。",
        "tips": ["비빔밥 = 拌饭", "물 = 水", "김치 더 주세요 = 请多加泡菜"],
        "expected_phrases": ["비빔밥 하나", "물 한 병", "주세요", "감사합니다"],
    },
    {
        "id": "self_intro",
        "title": "👋 自我介绍",
        "title_ko": "자기소개하기",
        "description": "用韩语介绍自己",
        "difficulty": 1,
        "context": "你第一次见韩国朋友。你想介绍自己：名字、国籍、爱好。",
        "starter": "안녕하세요! 처음 뵙겠습니다. 이름이 뭐예요?",
        "starter_zh": "你好！初次见面。你叫什么名字？",
        "tips": ["저는 ___입니다 = 我是___", "중국에서 왔어요 = 来自中国", "취미는 ___입니다 = 爱好是___"],
        "expected_phrases": ["안녕하세요", "저는", "입니다", "취미는"],
    },
    {
        "id": "shopping",
        "title": "🛍️ 购物",
        "title_ko": "쇼핑하기",
        "description": "在韩国商场购物的对话练习",
        "difficulty": 2,
        "context": "你在明洞的服装店看中了一件衣服。你想试穿并问价格。",
        "starter": "어서 오세요! 뭐 찾으시는 거 있어요?",
        "starter_zh": "欢迎光临！您在找什么？",
        "tips": ["입어 봐도 돼요? = 可以试穿吗？", "얼마예요? = 多少钱？", "깎아 주세요 = 请便宜点"],
        "expected_phrases": ["이거", "얼마예요", "입어", "주세요"],
    },
    {
        "id": "direction",
        "title": "🗺️ 问路",
        "title_ko": "길 묻기",
        "description": "在韩国街头问路的对话练习",
        "difficulty": 2,
        "context": "你在首尔想去景福宫，但迷路了。你需要向路人问路。",
        "starter": "길을 잃으셨나요? 어디 가세요?",
        "starter_zh": "迷路了吗？要去哪里？",
        "tips": ["___에 어떻게 가요? = 怎么去___？", "여기서 멀어요? = 离这里远吗？", "왼쪽/오른쪽 = 左/右"],
        "expected_phrases": ["어떻게", "가요", "여기", "감사합니다"],
    },
    {
        "id": "hotel",
        "title": "🏨 酒店入住",
        "title_ko": "호텔 체크인",
        "description": "在韩国酒店办理入住的对话练习",
        "difficulty": 2,
        "context": "你抵达首尔的酒店，需要办理入住。你已经提前预订了。",
        "starter": "안녕하세요, 체크인하시겠어요?",
        "starter_zh": "你好，要办理入住吗？",
        "tips": ["예약했어요 = 我预订了", "며칠 = 几天", "와이파이 비밀번호 = WiFi密码"],
        "expected_phrases": ["체크인", "예약", "방", "며칠"],
    },
    {
        "id": "taxi",
        "title": "🚕 打车",
        "title_ko": "택시 타기",
        "description": "在韩国打车的对话练习",
        "difficulty": 1,
        "context": "你从首尔站出来，需要打车去明洞。",
        "starter": "어디로 가세요?",
        "starter_zh": "去哪里？",
        "tips": ["___로 가 주세요 = 请去___", "여기서 내려 주세요 = 请在这里停", "얼마예요? = 多少钱？"],
        "expected_phrases": ["가", "주세요", "여기", "얼마예요"],
    },
    {
        "id": "phone",
        "title": "📱 打电话",
        "title_ko": "전화하기",
        "description": "用韩语打电话的对话练习",
        "difficulty": 2,
        "context": "你打电话给韩国朋友约见面。",
        "starter": "여보세요?",
        "starter_zh": "喂？",
        "tips": ["___ 씨 계세요? = ___在吗？", "언제 만날까요? = 什么时候见？"],
        "expected_phrases": ["여보세요", "만나", "언제", "시간"],
    },
    {
        "id": "hospital",
        "title": "🏥 看病",
        "title_ko": "병원에서",
        "description": "在韩国医院看病的对话练习",
        "difficulty": 3,
        "context": "你感觉不舒服，去韩国医院看病。你头疼并且发烧了。",
        "starter": "어디가 불편하세요?",
        "starter_zh": "哪里不舒服？",
        "tips": ["머리가 아파요 = 头疼", "열이 나요 = 发烧了", "약 = 药"],
        "expected_phrases": ["아파요", "열", "약", "처방"],
    },
    {
        "id": "interview",
        "title": "💼 面试",
        "title_ko": "면접 보기",
        "description": "用韩语进行工作面试的对话练习",
        "difficulty": 3,
        "context": "你在参加一家韩国公司的面试。你需要介绍自己的经历和优势。",
        "starter": "자기소개 부탁드립니다.",
        "starter_zh": "请做一下自我介绍。",
        "tips": ["저는 ___입니다 = 我是___", "경력 = 经验/经历", "열심히 하겠습니다 = 我会努力的"],
        "expected_phrases": ["저는", "입니다", "경험", "열심히"],
    },
]


def get_all_scenarios() -> list[dict]:
    """Get all scenario metadata (without full context)"""
    return [
        {"id": s["id"], "title": s["title"], "title_ko": s["title_ko"],
         "description": s["description"], "difficulty": s["difficulty"]}
        for s in SCENARIOS
    ]


def get_scenario(scenario_id: str) -> dict | None:
    """Get full scenario by ID"""
    for s in SCENARIOS:
        if s["id"] == scenario_id:
            return s
    return None


def generate_ai_response(scenario_id: str, user_message: str) -> dict:
    """Generate an AI response for a scenario conversation.

    In production, this calls an LLM (Claude/GPT) with the scenario context and user message.
    For MVP, returns template-based responses.
    """
    scenario = get_scenario(scenario_id)
    if not scenario:
        return {"reply": "죄송합니다, 이해하지 못했어요.", "reply_zh": "抱歉，我没理解。"}

    msg_lower = user_message.lower()

    # Template-based response patterns
    if scenario_id == "cafe":
        if any(w in msg_lower for w in ["아메리카노", "커피", "라떼"]):
            return {"reply": "네, 어떤 사이즈로 드릴까요?", "reply_zh": "好的，要什么大小？", "pronunciation": "ne, eo-tteon sa-i-jeu-ro deu-ril-kka-yo?"}
        if any(w in msg_lower for w in ["얼마", "가격"]):
            return {"reply": "총 5,500원입니다.", "reply_zh": "总共5500韩元。", "pronunciation": "chong o-cheon-o-baek-won-im-ni-da"}
        if any(w in msg_lower for w in ["감사", "고마"]):
            return {"reply": "맛있게 드세요! 다음에 또 오세요~", "reply_zh": "请享用！欢迎下次再来~", "pronunciation": None}

    if scenario_id == "restaurant":
        if any(w in msg_lower for w in ["비빔밥", "불고기", "김치"]):
            return {"reply": "네, 알겠습니다. 더 필요한 거 있으세요?", "reply_zh": "好的，还需要什么吗？", "pronunciation": None}
        if any(w in msg_lower for w in ["계산", "얼마"]):
            return {"reply": "15,000원입니다. 카드로 계산하시겠어요?", "reply_zh": "15000韩元。刷卡吗？", "pronunciation": None}

    if scenario_id == "self_intro":
        if any(w in msg_lower for w in ["이름", "저는"]):
            return {"reply": "반갑습니다! 취미는 뭐예요?", "reply_zh": "很高兴认识你！爱好是什么？", "pronunciation": None}
        if any(w in msg_lower for w in ["취미", "좋아"]):
            return {"reply": "아, 정말요? 저도 좋아해요!", "reply_zh": "啊，真的吗？我也喜欢！", "pronunciation": None}

    if scenario_id == "shopping":
        if any(w in msg_lower for w in ["얼마", "가격"]):
            return {"reply": "이 옷은 50,000원이에요.", "reply_zh": "这件衣服50000韩元。", "pronunciation": None}
        if any(w in msg_lower for w in ["입어", "입을"]):
            return {"reply": "네, 탈의실은 저쪽이에요~", "reply_zh": "好的，试衣间在那边~", "pronunciation": None}

    # Default response
    responses = [
        {"reply": "네, 알겠습니다!", "reply_zh": "好的，明白了！"},
        {"reply": "아, 그렇군요. 더 필요한 거 있으세요?", "reply_zh": "啊，这样啊。还需要什么吗？"},
        {"reply": "좋아요! 계속 말씀해 주세요.", "reply_zh": "好的！请继续说。"},
        {"reply": "잘하고 있어요! 조금만 더 연습해요~", "reply_zh": "做得很好！再练习一下吧~"},
    ]
    return random.choice(responses)
