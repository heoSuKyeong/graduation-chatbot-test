import streamlit as st
import requests

# 페이지 설정
st.set_page_config(page_title="추천 챗봇", page_icon="🤖")

# 초기 메시지 설정
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요. 저는 데이터 기반 추천 챗봇입니다. 아래 카테고리를 선택해주세요."}
    ]
    st.session_state.main_category_selected = False
    st.session_state.sub_category_selected = False
    st.session_state.selected_main_category = None
    st.session_state.selected_sub_category = None
    st.session_state.user_input_received = False
    st.session_state.image_path = "https://post-phinf.pstatic.net/MjAyNDA2MDZfMjE5/MDAxNzE3NjUwOTIwNDUz.q63mU5ehjNCLUaezPZalP3DHg6ygnCtLIwgpqECfUmcg.Y1Hk7ZJQMiPdEadk-0deXAWTaE-64BE0GvjsiXNG43sg.JPEG/TSG1_%282%29.jpg?type=w1200"
# 채팅 메시지 표시
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

# main_category 리스트 가져오기
main_category_response = requests.get("http://127.0.0.1:8000/chatbot/api/main-categories/")
main_categories = main_category_response.json() if main_category_response.status_code == 200 else []

# main_category 버튼 생성
if not st.session_state.main_category_selected:
    col1, col2, col3, col4 = st.columns(4)
    for index, main_category in enumerate(main_categories):
        with [col1, col2, col3, col4][index % 4]:
            if st.button(main_category['name']):
                st.session_state.selected_main_category = main_category
                st.session_state.main_category_selected = True
                # 사용자 선택에 따라 메시지 추가
                st.session_state.messages.append(
                    {"role": "user", "content": main_category['name']}
                )
                st.session_state.messages.append(
                    {"role": "assistant", "content": f"{main_category['name']}를 원하시군요. 아래 세부 카테고리를 선택해주세요."}
                )
                st.rerun()

# main_category 선택 시 sub_category 로직
if st.session_state.main_category_selected and not st.session_state.sub_category_selected:
    selected_main_category = st.session_state.selected_main_category
    print("id: " + str(selected_main_category['id']))

    sub_category_response = requests.get(f"http://127.0.0.1:8000/chatbot/get_sub_categories/{selected_main_category['id']}/")
    sub_categories = sub_category_response.json().get('sub_categories', []) if sub_category_response.status_code == 200 else []

    col1, col2, col3, col4 = st.columns(4)
    for index, sub_category in enumerate(sub_categories):
        with [col1, col2, col3, col4][index % 4]:
            if st.button(sub_category['name']):
                st.session_state.selected_sub_category = sub_category
                st.session_state.sub_category_selected = True
                # 사용자 선택에 따라 메시지 추가
                st.session_state.messages.append(
                    {"role": "user", "content": sub_category['name']}
                )
                st.session_state.messages.append(
                    {"role": "assistant", "content": f"{sub_category['name']}를 원하시군요. 원하시는 조건을 입력해주세요."}
                )
                st.rerun()

# 조건 입력 및 응답
if st.session_state.main_category_selected and st.session_state.sub_category_selected and not st.session_state.user_input_received:
    user_input = st.text_input("조건을 입력하세요:")
    if user_input:
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )
        st.session_state.messages.append(
            {"role": "assistant", "content": f"{user_input}에 대한 조건을 받았습니다."}
        )
        st.session_state.user_input_received = True  # 추가: 사용자 입력 상태 플래그 설정
        st.rerun()

if st.session_state.user_input_received:
    st.image(st.session_state.image_path, caption="여기 이미지입니다.")