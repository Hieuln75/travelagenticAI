import requests

def call_agent(prompt):
    url = "http://127.0.0.1:8000/chat"
    resp = requests.post(url, json={"message": prompt})
    
    try:
        data = resp.json()
    except Exception as e:
        print("Lỗi khi decode JSON:", e)
        print("Server trả về:", resp.text)
        return
    
    if data.get("status") == "success":
        print("\n=== Kết quả cuối cùng từ itinerary_agent ===")
        print(data["final_result"])
        print("\n=== Tóm tắt plan_data ===")
        print(data["data_summary"])
    else:
        print("Server báo lỗi:", data.get("detail"))

if __name__ == "__main__":
    msg = input("Nhập kế hoạch du lịch của bạn: ")
    call_agent(msg)
