import streamlit as st
import google.generativeai as genai
import re

# ✅ API 키 예외 처리
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("❌ API 키가 설정되지 않았어요. Streamlit Secrets에 GOOGLE_API_KEY를 추가해 주세요.")
    st.stop()

# ✅ Gemini API 설정
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 🌿 불필요한 표현 리스트
unnecessary_phrases = [
    "안녕하세요", "부탁드려요", "감사합니다", "좋은 하루 되세요", "혹시", "좀", "실 수 있을까요",
    "해주실 수 있나요?", "고맙습니다", "고마워", "맞을까요?", "항상 수고 많으세요", "잘 부탁 드립니다",
    "해주시면 감사하겠습니다", "확인 부탁드립니다", "왠지", "웬만하면", "왠지 모르게", "괜찮을까요?",
    "틀린 건 아니죠?", "제가 이해한 게 맞나요?", "대충", "뭐랄까", "그냥요", "그런 거 같아요",
    "느낌상", "그런 식으로요", "이 정도면 될까요?", "너무 길었네요", "괜히 질문 드려 죄송합니다",
    "일단", "또"
]

# ✅ 정중 표현 간소화 함수 (정규표현식 사용)
def simplify(sentence):
    patterns = {
        r"알려주[실줄]\s*수\s*있.*?[요]?\??": "알려줘",
        r"추천해주[실줄]\s*수\s*있.*?[요]?\??": "추천해줘",
        r"도와주[실줄]\s*수\s*있.*?[요]?\??": "도와줘",
        r"해주[실줄]\s*수\s*있.*?[요]?\??": "해줘",
        r"주시겠.*?[요]?\??": "줘"
    }
    for pattern, replacement in patterns.items():
        sentence = re.sub(pattern, replacement, sentence)
    return sentence

# ✅ 앱 UI 구성
st.title("🌿 AI 친환경 질문 도우미 (Gemini API)")
st.markdown("AI에게 질문할 때, 짧고 간결한 표현으로 물 사용을 줄여보세요 💧")

user_input = st.text_area("✍️ AI에게 할 질문을 입력해보세요:")

if user_input:
    simplified_input = simplify(user_input)
    found_phrases = list(set(phrase for phrase in unnecessary_phrases if phrase in simplified_input))

    # ✅ 점수 계산
    base_score = 100
    length_penalty = len(user_input) // 25
    phrase_penalty = len(found_phrases) * 5
    final_score = max(0, base_score - length_penalty - phrase_penalty)

    # ✅ 표현 제거
    improved_question = simplified_input
    for phrase in found_phrases:
        improved_question = improved_question.replace(phrase, "")
    improved_question = improved_question.strip()

    # ✅ 결과 출력
    st.subheader("🧹 불필요한 표현 제거 결과")
    st.write(f"✏️ 글자 수: {len(user_input)}자")
    st.write(f"🗑️ 제거된 표현: {', '.join(found_phrases) if found_phrases else '없어요!'}")
    st.write(f"🌱 친환경 점수: **{final_score} / 100점**")
    st.progress(final_score / 100)

    st.subheader("✅ 정제된 질문")
    st.success(improved_question if improved_question else "⚠️ 질문이 너무 짧아졌어요!")

    # ✅ Gemini 응답
    st.subheader("🤖 Gemini AI 응답")
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(improved_question)

        if hasattr(response, "text") and response.text.strip():
            st.info(response.text.strip())
        else:
            st.warning("Gemini가 유효한 응답을 반환하지 않았어요. 질문을 다시 확인해 주세요.")
    except Exception as e:
        st.error(f"⚠️ Gemini API 오류: {e}")

