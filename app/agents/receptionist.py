from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage
import json
import re

llm = ChatGroq(
     temperature=0,
     model_name="llama-3.1-8b-instant",
     groq_api_key="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"
)

def receptionist_agent(state):
    user_msg = state["messages"][-1].content
    
    prompt = f"""
    Dựa trên yêu cầu: "{user_msg}"
    Hãy trích xuất thông tin du lịch sang JSON.
    - destination: Tên thành phố (Ví dụ: Hồ Chí Minh, Hà Nội, Đà Nẵng)
    - duration: Số ngày (chỉ lấy số nguyên)

    Chỉ trả về JSON thuần túy, không giải thích.
    """
    
    response = llm.invoke(prompt)
    content = response.content.strip()
    
    try:
        match = re.search(r"\{.*\}", content, re.DOTALL)
        data = json.loads(match.group()) if match else {}
        dest = data.get("destination", "Hồ Chí Minh")
        # Chuẩn hóa tên nếu model viết tắt
        if dest.lower() in ["hcm", "tp hcm", "saigon"]: dest = "Hồ Chí Minh"
        dur = int(data.get("duration", 5))
    except:
        dest = "Hồ Chí Minh"
        dur = 5

    return {
        "plan_data": {"destination": dest, "duration": dur},
        "next_step": "flight",
        "messages": [AIMessage(content=f"📍 Đã xác nhận điểm đến: {dest} trong {dur} ngày.")]
    }