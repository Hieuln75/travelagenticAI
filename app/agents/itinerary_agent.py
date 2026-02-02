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

def itinerary_agent(state):
    plan = state.get("plan_data", {})
    dest = plan.get("destination", "Hồ Chí Minh")
    dur = plan.get("duration", 5)
    
    prompt = f"""
    Lập lịch trình chi tiết cho {dur} ngày tại {dest}.
    Mỗi ngày từ Ngày 1 đến Ngày {dur} phải có các hoạt động thực tế tại {dest}.
    Trả về JSON: {{"itinerary": "nội dung chi tiết"}}
    """
    
    response = llm.invoke(prompt)
    try:
        match = re.search(r"\{.*\}", response.content, re.DOTALL)
        data = json.loads(match.group())
        itinerary = data.get("itinerary", response.content)
    except:
        itinerary = response.content

    return {
    "plan_data": {
        **state.get("plan_data", {})
    },
    "messages": [
        AIMessage(
            content=f"✅ Lịch trình {dur} ngày tại {dest} hoàn tất:\n\n{itinerary}"
        )
    ]
    }
