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
    
    prompt = f"Chọn 1 chuyến bay giả định đến {dest}. Trả về JSON: {{\"code\": \"string\", \"arrival\": \"string\"}}"
    
    response = llm.invoke(prompt)
    try:
        match = re.search(r"\{.*\}", response.content, re.DOTALL)
        flight_data = json.loads(match.group())
    except:
        flight_data = {"code": "VN-123", "arrival": "10:00 AM"}

    return {
        "plan_data": {"flight": flight_data}, # CHỈ gửi flight
        "next_step": "hotel",
        "messages": [AIMessage(content=f"✈️ Đã tìm chuyến bay {flight_data['code']} đến {dest}.")]
    }