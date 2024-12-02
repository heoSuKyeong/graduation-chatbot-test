import streamlit as st
from streamlit_chat import message
from datetime import datetime

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
    overflow-y: scroll;  /* 세로 스크롤을 숨기기 */
    white-space: nowrap; 
    height: 380px;
}

.stColumn {
    display: inline-block;
    width: 250px;
    flex: none;
    margin-right: 1rem;
}
</style>
"""

def get_main_categories():
    return ["영상/음향", "미용/욕실", "주방가전", "계절가전"]


def get_sub_categories():
    return ["에어컨", "온풍기", "제습기", "서큘레이터", "그 외"]


def get_products():
    return [
        {
            "no": 1,
            "main_category_id": 1,
            "main_category": "영상/음향",
            "sub_category_id": 6,
            "sub_category": "오디오/플레이어",
            "name": "에디파이어 MR4",
            "photo_url": "https://post-phinf.pstatic.net/MjAyNDA2MDZfMjE5/MDAxNzE3NjUwOTIwNDUz.q63mU5ehjNCLUaezPZalP3DHg6ygnCtLIwgpqECfUmcg.Y1Hk7ZJQMiPdEadk-0deXAWTaE-64BE0GvjsiXNG43sg.JPEG/TSG1_%282%29.jpg?type=w1200",
            "manufacturer": "캐리어",
            "release_date": "2024-11-14",
            "energy_efficiency": "3등급",
            "power_consumption_W": 150,
            "weight_kg": 0.1,
            "release_price": 210000
        },
        {
            "no": 2,
            "main_category_id": 1,
            "main_category": "영상/음향",
            "sub_category_id": 4,
            "sub_category": "무선 스피커",
            "name": "Creative PEBBLE PLUS 정품",
            "photo_url": "https://post-phinf.pstatic.net/MjAyNDA2MDZfMjc1/MDAxNzE3NjUwMzYwNDAw.eEPHbNWJtY9Tjzu5cgvC0O9In9b6RC0XNu9pW0h141Ig.Z_NeGnHBnN6ki0rH0lAybthPsu4ngO6G7mUx2Sd7cssg.JPEG/RS8C_%282%29.jpg?type=w1200",
            "manufacturer": "위니아",
            "release_date": "2021-08-06",
            "energy_efficiency": "3등급",
            "power_consumption_W": 300,
            "weight_kg": 0.15,
            "release_price": 110000
        },
        {
            "no": 3,
            "main_category_id": 1,
            "main_category": "영상/음향",
            "sub_category_id": 4,
            "sub_category": "무선 스피커",
            "name": "Creative PEBBLE V2 정품",
            "photo_url": "https://post-phinf.pstatic.net/MjAyNDA2MDZfMjk4/MDAxNzE3NjExMzE1MzI1.4P8wy_JezNtqNyuUYuU64524VKP5PwCLXkpNGibUCXUg.8NGpxq2-ndQ6xl73D9Rp9Ra0MoSvCGE6RmvsrFVMEoAg.PNG/20240606_031824.png?type=w1200",
            "manufacturer": "삼성전자",
            "release_date": "2022-09-08",
            "energy_efficiency": "4등급",
            "power_consumption_W": 150,
            "weight_kg": 3.5,
            "release_price": 310000
        },
        {
            "no": 4,
            "main_category_id": 1,
            "main_category": "영상/음향",
            "sub_category_id": 4,
            "sub_category": "무선 스피커",
            "name": "마샬 STANMORE II",
            "photo_url": "https://post-phinf.pstatic.net/MjAyNDA2MDZfOTgg/MDAxNzE3NjUzNjE0NTc2.6yfstdfWQDKtwTWbBQwjHmrJfz6d1Ya2h7o_GYJEjhsg.IQJyia3Ef1yYfl7_YZ3TPpVJtZLruIV4469rCDTJx8Ug.JPEG/SW67_%281%29.jpg?type=w1200",
            "manufacturer": "위닉스",
            "release_date": "2024-11-14",
            "energy_efficiency": "5등급",
            "power_consumption_W": 20,
            "weight_kg": 3.5,
            "release_price": 10000
        },
        {
            "no": 5,
            "main_category_id": 1,
            "main_category": "영상/음향",
            "sub_category_id": 4,
            "sub_category": "무선 스피커",
            "name": "캔스톤 NX301 ZENELEC 정품",
            "photo_url": "https://post-phinf.pstatic.net/MjAyNDA2MDZfMjE5/MDAxNzE3NjUwOTIwNDUz.q63mU5ehjNCLUaezPZalP3DHg6ygnCtLIwgpqECfUmcg.Y1Hk7ZJQMiPdEadk-0deXAWTaE-64BE0GvjsiXNG43sg.JPEG/TSG1_%282%29.jpg?type=w1200",
            "manufacturer": "삼성전자",
            "release_date": "2023-10-09",
            "energy_efficiency": "2등급",
            "power_consumption_W": 300,
            "weight_kg": 3.5,
            "release_price": 310000
        }
    ]


def scroll_to_bottom():
    scroll_script = """
    <script>
        var body = window.parent.document.getElementById("root");
        body.scrollTop += 9999999999;
    </script>
    """
    st.components.v1.html(scroll_script)


# 현재 시간 기반 고유 ID 생성
def generate_short_id():
    return datetime.now().strftime('%Y%m%d%H%M%S%f')


def render_chat_ui():
    # 기존 메시지 표시
    for i, msg in enumerate(st.session_state["messages"]):
        # default, reloading 버벅임 없음
        # with st.chat_message(msg["role"]):
            # st.write(msg["content"])
        
        # stream-chat, reloading 버벅임
        message(msg["content"], is_user=(msg["role"] == "user"), key=f"message_{i}")

        if "callback" in msg and msg["callback"]:
            msg["callback"]()

    # 상태에 따라 다른 UI 요소 표시
    if not st.session_state["selected_main_category"]:
        render_main_categories()
    elif not st.session_state["selected_sub_category"]:
        render_sub_categories()
    elif not st.session_state["search_filters"] or not st.session_state["selected_product"]:
        render_search_filters()


def on_click_main_category_btn(main_category):
    st.session_state["selected_main_category"] = main_category
    st.session_state["messages"].append({"role": "user", "content": main_category})
    st.session_state["messages"].append({"role": "assistant", "content": f"{main_category}을 찾으시는군요! 어떤 제품을 찾으시나요?"})


def on_click_sub_category_btn(sub_category):
    st.session_state["selected_sub_category"] = sub_category
    st.session_state["messages"].append({"role": "user", "content": sub_category})
    st.session_state["messages"].append({"role": "assistant", "content": "원하는 조건이 있으신가요?"})


def on_submit_search_filters():
    user_input = st.session_state["current_input"]
    st.session_state["search_filters"] = user_input
    st.session_state["messages"].append({"role": "user", "content":user_input})
    st.session_state["messages"].append({"role": "assistant", "content": f"{st.session_state['search_filters']} 기준으로 가장 만족도가 높은 5개 제품을 골라봤어요!\n\n마음에 드는 제품이 없다면 조건을 다시 입력해주세요.", "callback": display_recommanded_products})


def on_click_buy_btn(**product):
    st.session_state["selected_product"] = product
    st.session_state["messages"].append({"role": "assistant", "content": f"{product['name']} 구매 페이지로 이동합니다."})
    scroll_to_bottom()


def render_main_categories():   
    main_categories = get_main_categories()
    columns = st.columns(len(main_categories))
    for i, main_category in enumerate(main_categories):
        with columns[i]:
            st.button(main_category, on_click=on_click_main_category_btn, args=(main_category,))


def render_sub_categories():
    sub_categories = get_sub_categories()
    sub_columns = st.columns(len(sub_categories))
    for i, sub_category in enumerate(sub_categories):
        with sub_columns[i]:
            st.button(sub_category, on_click=on_click_sub_category_btn, args=(sub_category,))


def render_search_filters():
    st.chat_input("조건을 입력해주세요..", key="current_input", on_submit=on_submit_search_filters)


def display_recommanded_products():
    st.markdown(products_css, unsafe_allow_html=True)

    products = get_products()
    columns = st.columns(len(products))
    for i, product in enumerate(products):
        with columns[i]:
            with st.expander(label=f"**{i+1}. {product['name']}**", expanded=True):
                st.image("https://img.hankyung.com/photo/202406/01.36942977.1.jpg")
                st.text(f"가격: {product['release_price']:,}원")
                st.text(f"{product['manufacturer']} / {product['release_date']}")
                st.text(f"{product['energy_efficiency']} ({product['power_consumption_W']}W)")
                st.button("최저가 사러가기", key=f"buy_{i}_{generate_short_id()}", on_click=on_click_buy_btn, kwargs=product)

    
def main():
    # Streamlit 페이지 설정
    st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="wide")
    st.title("🤖 Chatbot")
    st.caption("💬 Review-Based Home Appliance Recommendation Chatbot")
    st.markdown(button_css, unsafe_allow_html=True)

    # 세션 상태 초기화
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "안녕하세요. 사용자 리뷰 기반으로 가전제품을 추천해드리는 챗봇 \"CHATBOT\" 입니다.\n\n어떤 가전제품을 찾고 계신가요? 😊"}
        ]
        st.session_state["selected_main_category"] = None
        st.session_state["selected_sub_category"] = None
        st.session_state["search_filters"] = None
        st.session_state["selected_product"] = None
        
    # 채팅 UI 렌더링
    render_chat_ui()


if __name__ == "__main__":
    main()
