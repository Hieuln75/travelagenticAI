from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from app.graph import build_graph
from app.state import TravelState

app = FastAPI()
graph = build_graph()  # Khởi tạo graph khi startup

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def healthcheck():
    return {"status": "ok"}

@app.post("/chat")
def chat(req: ChatRequest):
    try:
        # 1. Khởi tạo state ban đầu
        initial_state = {
            "messages": [HumanMessage(content=req.message)],
            "user_input": req.message,
            "next_step": "receptionist",
            "plan_data": {}
        }

        # 2. Sử dụng invoke() thay vì astream() để chạy toàn bộ luồng một lần
        final_state = graph.invoke(initial_state)
        
        # 3. CHỈ TRẢ VỀ DỮ LIỆU THUẦN (String, Dict) để FastAPI không bị lỗi
        # Chúng ta lấy nội dung từ message cuối cùng (từ itinerary_agent)
        last_message = final_state["messages"][-1].content
        
        return {
            "status": "success",
            "final_result": last_message,
            "data_summary": final_state["plan_data"]
        }
        
    except Exception as e:
        # Nếu có bất kỳ lỗi nào trong Graph, trả về JSON báo lỗi thay vì sập server
        return {"status": "error", "detail": str(e)}