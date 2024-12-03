# streamlit_app3.py

import streamlit as st
from streamlit_chat import message
import requests
from datetime import datetime

API_BASE_URL = "http://127.0.0.1:8000/chatbot/api/"

# 스타일 정의
button_css = """
<style>
.st-emotion-cache-ocqkz7 {
    margin-left: 60px;
}

.stHorizontalBlock {
    display: flex;
    gap: 1;
}

.st-emotion-cache-12w0qpk {
    flex: none;
}

.stColumn {
    margin: 0;
    padding: 0;
    width: auto;
    flex: none;
}

.stButton {
    margin: 0;
}
</style>
"""

products_css = """
<style>
.stHorizontalBlock {
    display: block;
    flex-direction: row;
    overflow-x: scroll;
    /* overflow-y: hidden; 세로 스크롤을 숨기기 */
    white-space: nowrap;
    height: 500px;
}

.stColumn {
    display: inline-block;
    width: 300px;
    flex: none;
    margin-right: 1rem;
}

.stExpander {
    text-align: center;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    word-wrap: break-word; /* 줄바꿈 */
}

.stExpander img {
    width: 250px; /* 이미지 가로 폭 맞춤 */
    height: 150px; /* 이미지 세로 크기 고정 */
    object-fit: cover; /* 이미지 비율 유지 */
    border-radius: 8px; /* 이미지 테두리 둥글게 */
    margin-bottom: 10px;
}

.st-emotion-cache-1h9usn1 {
    border: none; 
}

.st-emotion-cache-1puwf6r p {
    white-space: normal;
    text-align: left;
}

</style>
"""

# 현재 시간 기반 고유 ID 생성
def generate_short_id():
    return datetime.now().strftime('%Y%m%d%H%M%S%f')

def on_click_buy_btn(**product):
    st.session_state["selected_product"] = product
    st.session_state["messages"].append({"role": "assistant", "content": f"{product['name']} 구매 페이지로 이동합니다."})
    scroll_to_bottom()

def scroll_to_bottom():
    scroll_script = """
    <script>
        var body = window.parent.document.getElementById("root");
        body.scrollTop += 9999999999;
    </script>
    """
    st.components.v1.html(scroll_script)

# 안전한 API 요청 함수
def safe_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API 호출 에러: {e}")
        return []

def get_main_categories():
    return safe_request(f"{API_BASE_URL}main-categories/")

def get_sub_categories(main_category_id):
    return safe_request(f"{API_BASE_URL}main-categories/{main_category_id}/sub-categories/") #.get('sub_categories', [])

def fetch_aspect_ratios(product_id):
    try:
        response = requests.get(f"{API_BASE_URL}products/{product_id}/aspect-ratio/")
        response.raise_for_status()
        return response.json()  # JSON 데이터 반환
    except requests.exceptions.RequestException as e:
        st.error(f"API 호출 실패: {e}")
        return {"aspects": []}  # 기본값 반환

def render_main_categories():
    main_categories = get_main_categories()
    columns = st.columns(len(main_categories))
    for i, main_category in enumerate(main_categories):
        with columns[i]:
            st.button(main_category['name'], on_click=on_click_main_category_btn, args=(main_category,))

def render_sub_categories():
    selected_main_category = st.session_state["selected_main_category"]
    sub_categories = get_sub_categories(selected_main_category['id'])
    sub_columns = st.columns(len(sub_categories))
    for i, sub_category in enumerate(sub_categories):
        with sub_columns[i]:
            st.button(sub_category['name'], on_click=on_click_sub_category_btn, args=(sub_category,))

def display_recommanded_products():
    st.markdown(products_css, unsafe_allow_html=True)
    
    products = st.session_state.get("recommended_products", [])
    if not products:
        st.write("추천된 제품이 없습니다.")
        return
    print(products)
    
    columns = st.columns(len(products))
    for i, product in enumerate(products):
        with columns[i]:
            with st.expander(label=f"**{i+1}. {product['product']['name']}**", expanded=True):
                st.image(product["product"].get("photo", ""), caption=product["product"]["name"])
                st.text(f"출시가격: {product['product'].get('price', 0):,}원")
                st.text(f"제조사: {product['product'].get('manufacturer', '정보 없음')} / 출시년도: {product['product'].get('release_year', '정보 없음')}")
                st.write("### 주요 성능별 비율")
                # API에서 데이터 가져오기
                data = fetch_aspect_ratios(product["product"]["id"])
                aspect_ratios = data.get("aspect_ratios", [])

                if not aspect_ratios:
                    st.write("분석 결과가 없습니다.")
                    return

                if aspect_ratios:
                    # 긍정 비율 기준으로 정렬
                    sorted_aspects = sorted(
                        aspect_ratios,
                        key=lambda x: float(x["positive_ratio"]),
                        reverse=True
                    )
                    for aspect in sorted_aspects:
                        # 문자열을 숫자로 변환 후 포맷
                        positive_ratio = float(aspect["positive_ratio"])
                        negative_ratio = float(aspect["negative_ratio"])
                        st.text(f"{aspect['aspect']} - 긍정: {positive_ratio:.0f}%, 부정: {negative_ratio:.0f}%")
                        
                else:
                    st.text("속성 비율 정보를 가져올 수 없습니다.")

                st.button("최저가 사러가기", key=f"buy_{i}_{generate_short_id()}", on_click=on_click_buy_btn, kwargs=product["product"])

def render_chat_ui():
    # 기존 메시지 표시
    for i, msg in enumerate(st.session_state["messages"]):
        message(msg["content"], is_user=(msg["role"] == "user"), key=f"message_{i}")
    
    if not st.session_state["selected_main_category"]:
        render_main_categories()
    elif not st.session_state["selected_sub_category"]:
        render_sub_categories()
    elif not st.session_state["search_filters"]:
        st.chat_input("조건을 입력해주세요", key="current_input", on_submit=on_submit_search_filters)

    # 제품 추천 표시
    if st.session_state.get("display_products"):
        display_recommanded_products()

def on_click_main_category_btn(main_category):
    st.session_state["selected_main_category"] = main_category
    st.session_state["messages"].append({"role": "user", "content": main_category['name']})
    st.session_state["messages"].append({"role": "assistant", "content": f"{main_category['name']}을 찾으시는군요! 세부 카테고리를 선택해주세요."})

def on_click_sub_category_btn(sub_category):
    st.session_state["selected_sub_category"] = sub_category
    st.session_state["messages"].append({"role": "user", "content": sub_category['name']})
    st.session_state["messages"].append({"role": "assistant", "content": "원하는 조건을 입력해주세요!"})
 
def on_submit_search_filters():
    

    # 로딩 스피너 적용
    with st.spinner("로딩 중... 잠시만 기다려 주세요."):

        user_input = st.session_state["current_input"]
        st.session_state["search_filters"] = user_input

        # 사용자 입력을 API에 전달
        selected_sub_category = st.session_state.get("selected_sub_category")
        if not selected_sub_category:
            st.error("세부 카테고리를 먼저 선택해주세요.")
            return

        try:
            response = requests.post(
                f"{API_BASE_URL}sub-categories/{selected_sub_category['id']}/recommend-products/",
                json={"condition": user_input},
            )
            response.raise_for_status()
            data = response.json()

            # 성공적으로 데이터를 받아온 경우
            products = data.get("products", [])
            if not products:
                st.session_state["messages"].append(
                    {"role": "assistant", "content": "추천할 제품이 없습니다. 조건을 다시 입력해주세요!"}
                )
            else:
                st.session_state["messages"].append({"role": "user", "content": user_input})
                st.session_state["messages"].append(
                    {"role": "assistant", "content": f"'{user_input}' 기준으로 추천된 제품입니다. 아래 목록을 확인해주세요!"}
                )
                st.session_state["recommended_products"] = products
                st.session_state["display_products"] = True

        except requests.exceptions.RequestException as e:
            st.error(f"제품 추천 API 호출 중 오류가 발생했습니다: {e}")
            st.session_state["messages"].append(
                {"role": "assistant", "content": "조건 처리 중 오류가 발생했습니다. 다시 시도해주세요."}
            )

# 메인 함수
def main():
     # Streamlit 페이지 설정
    st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="wide")
    st.title("🤖 Chatbot")
    st.caption("💬 Review-Based Home Appliance Recommendation Chatbot")
    st.markdown(button_css, unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "안녕하세요. 사용자 리뷰 기반으로 가전제품을 추천해드리는 챗봇 \"CHATBOT\" 입니다.\n\n어떤 가전제품을 찾고 계신가요? 😊"}
        ]
        st.session_state["selected_main_category"] = None
        st.session_state["selected_sub_category"] = None
        st.session_state["search_filters"] = None
    
    render_chat_ui()

if __name__ == "__main__":
    main()
