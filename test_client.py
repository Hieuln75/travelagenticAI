import requests
import json

API_URL = "http://127.0.0.1:8000/chat"

def call_agent(prompt: str):
    try:
        resp = requests.post(API_URL, json={"message": prompt}, timeout=30)
    except Exception as e:
        print("❌ Không kết nối được server:", e)
        return

    # ===============================
    # PARSE RESPONSE JSON AN TOÀN
    # ===============================
    try:
        data = resp.json()
    except Exception as e:
        print("❌ Lỗi decode JSON từ server")
        print("Exception:", e)
        print("Raw response:")
        print(resp.text)
        return

    # ===============================
    # KIỂM TRA STATUS
    # ===============================
    if data.get("status") != "success":
        print("❌ Server báo lỗi:")
        print(data.get("detail", "Không rõ lỗi"))
        return

    # ===============================
    # IN KẾT QUẢ
    # ===============================
    print("\n===============================")
    print("✅ KẾT QUẢ CUỐI (ITINERARY)")
    print("===============================\n")

    final_result = data.get("final_result", "")
    print(final_result if final_result else "(Không có itinerary)")

    print("\n===============================")
    print("📦 TÓM TẮT PLAN_DATA")
    print("===============================\n")

    data_summary = data.get("data_summary", {})
    plan_data = data_summary.get("plan_data", {})

    if not plan_data:
        print("(plan_data rỗng)")
        return

    # In đẹp từng phần
    print(f"📍 Điểm đến: {plan_data.get('destination', 'N/A')}")
    print(f"🕒 Số ngày: {plan_data.get('duration', 'N/A')}")

    flight = plan_data.get("flight")
    if isinstance(flight, dict):
        print("\n✈️ Chuyến bay:")
        for k, v in flight.items():
            print(f"  - {k}: {v}")

    hotel = plan_data.get("hotel")
    if isinstance(hotel, dict):
        print("\n🏨 Khách sạn:")
        for k, v in hotel.items():
            print(f"  - {k}: {v}")

# ===============================
# ENTRY POINT
# ===============================
if __name__ == "__main__":
    msg = input("Nhập kế hoạch du lịch của bạn: ")
    call_agent(msg)
