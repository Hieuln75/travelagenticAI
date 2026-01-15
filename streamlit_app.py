import streamlit as st
import requests
import time

# Cấu hình trang
st.set_page_config(page_title="AI Travel Agent", page_icon="✈️", layout="centered")

st.title("✈️ AI Travel Planner")
st.markdown("Hệ thống Agentic AI tự động lập kế hoạch du lịch thông minh.")

# Khởi tạo lịch sử chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị các tin nhắn cũ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Ô nhập liệu của người dùng
if prompt := st.chat_input("Bạn muốn đi đâu? (Ví dụ: đi Hồ Chí Minh 5 ngày)"):
    # Thêm tin nhắn user vào giao diện
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gọi Backend (FastAPI)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🤖 *Đang suy nghĩ...*")
        
        try:
            # Gửi request đến FastAPI (Giả sử bạn đang chạy local ở port 8000)
            # Nếu đã host online, hãy thay url này bằng url Render/Railway của bạn
            response = requests.post("http://127.0.0.1:8000/chat", json={"message": prompt})
            
            if response.status_code == 200:
                result = response.json()
                final_itinerary = result.get("final_result", "")
                data_summary = result.get("data_summary", {})

                # Hiển thị tóm tắt thông tin bên trong một cái "Card"
                with st.expander("🔍 Chi tiết dữ liệu từ các Agent"):
                    st.json(data_summary)

                # Hiển thị lịch trình cuối cùng
                full_response = f"**Kế hoạch của bạn đã sẵn sàng!** \n\n {final_itinerary}"
                message_placeholder.markdown(full_response)
                
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error("Lỗi kết nối đến Backend!")
        except Exception as e:
            st.error(f"Đã xảy ra lỗi: {e}")