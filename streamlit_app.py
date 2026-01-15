import streamlit as st
import requests
import json

# Cấu hình trang
st.set_page_config(page_title="AI Travel Planner", page_icon="✈️", layout="wide")

st.title("🌐 Hệ thống Multi-Agent Điều phối Du lịch")
st.markdown("---")

# Ô nhập liệu
user_input = st.chat_input("Bạn muốn đi đâu? (Ví dụ: Đi Hồ Chí Minh 4 ngày)")

if user_input:
    with st.spinner("🤖 Hệ thống đang điều phối các Agent..."):
        try:
            # Gọi API Backend (Đảm bảo FastAPI đang chạy ở port 8000)
            response = requests.post("http://127.0.0.1:8000/chat", json={"message": user_input})
            
            if response.status_code == 200:
                result = response.json()
                # Lấy dữ liệu từ Shared State [cite: 44, 181]
                data = result.get("data_summary", {})
                itinerary_raw = result.get("final_result", "")

                # --- PHẦN 1: RECEPTIONIST AGENT (ROUTER) ---
                st.subheader("📍 1. Tiếp nhận & Phân tích")
                col1, col2 = st.columns(2)
                col1.metric("Điểm đến", data.get("destination", "N/A"))
                col2.metric("Thời gian", f"{data.get('duration', 'N/A')} ngày")
                
                st.divider()

                # --- PHẦN 2: WORKER AGENTS (SPECIALISTS) ---
                st.subheader("⚙️ 2. Tra cứu dữ liệu chuyên biệt")
                c1, c2 = st.columns(2)
                
                with c1:
                    st.info("✈️ **Flight Agent**")
                    flight = data.get("flight", {})
                    if isinstance(flight, dict):
                        st.write(f"- **Mã hiệu:** `{flight.get('code', 'N/A')}`")
                        st.write(f"- **Giờ đến:** {flight.get('arrival', 'N/A')}")
                    else:
                        st.write(flight)
                
                with c2:
                    st.success("🏨 **Hotel Agent**")
                    hotel = data.get("hotel", {})
                    if isinstance(hotel, dict):
                        st.write(f"- **Tên:** {hotel.get('name', 'N/A')}")
                        st.write(f"- **Vị trí:** {hotel.get('location', 'N/A')}")
                    else:
                        st.write(hotel)

                st.divider()

                # --- PHẦN 3: RESPONSE AGENT (AGGREGATOR) ---
                st.subheader("🗓️ 3. Tổng hợp lịch trình")
                
                # Logic xử lý hiển thị đẹp thay vì JSON [cite: 47, 48]
                if isinstance(itinerary_raw, dict):
                    for day, sessions in itinerary_raw.items():
                        with st.expander(f"📅 {day}", expanded=True):
                            for session, activities in sessions.items():
                                st.markdown(f"**{session}**")
                                if isinstance(activities, dict):
                                    for time_range, detail in activities.items():
                                        st.write(f"- **{time_range}**: {detail}")
                                else:
                                    st.write(f"- {activities}")
                else:
                    # Nếu là chuỗi, hiển thị dạng Markdown
                    st.markdown(itinerary_raw)

            else:
                st.error("Lỗi: Không nhận được phản hồi từ Backend.")
        except Exception as e:
            st.error(f"Lỗi kết nối: {e}")