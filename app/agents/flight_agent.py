from langchain_core.messages import AIMessage
from langchain_groq import ChatGroq
import json
import re
import os
llm = ChatGroq(
     temperature=0,
     model_name="llama-3.1-8b-instant",
      groq_api_key=os.environ["GROQ_API_KEY"]
)

def flight_agent(state):
    plan = state.get("plan_data", {})
    dest = plan.get("destination", "Hồ Chí Minh")
    user_context = state.get("user_context", {})
    user_city = user_context.get("city", "Hà nội")

    
    prompt = f"""
Bạn là trợ lý du lịch.

Ngữ cảnh người dùng:
- Thành phố hiện tại: {user_city}

Thông tin chuyến đi:
- Điểm đến: {dest}

Nhiệm vụ:
- Chọn 1 chuyến bay giả định từ {user_city} đến {dest}.
- CHỈ trả về dữ liệu chuyến bay.
- KHÔNG tự bịa thêm thông tin ngoài nhiệm vụ.

Trả về JSON hợp lệ theo đúng schema:
{{
  "code": "string",
  "from": "string",
  "to": "string",
  "arrival": "string"
}}

KHÔNG markdown.
KHÔNG giải thích.
KHÔNG text ngoài JSON.
"""
    response = llm.invoke(prompt)
    try:
        match = re.search(r"\{.*\}", response.content, re.DOTALL)
        flight_data = json.loads(match.group())
    except:
        flight_data = {"code": "VN-123", "arrival": "10:00 AM"}

    return {
       "plan_data": {**state.get("plan_data", {}), "flight": flight_data},
        "next_step": "hotel",
        "messages": [AIMessage(content=f"✈️ Đã tìm chuyến bay {flight_data['code']} đến {dest}.")]
    }