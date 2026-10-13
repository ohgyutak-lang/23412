import json
import os
import urllib.request
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="AI 수업 도우미: 똑똑이 쌤",
    page_icon="🤖",
    layout="wide",
)

# API 키 가져오기
try:
  api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
  api_key = os.environ.get("GEMINI_API_KEY", "")


# 💡 외부 패키지 없이 순수 파이썬으로 Gemini API 호출하는 함수
def generate_with_gemini(prompt_text, key):
  url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"

  headers = {"Content-Type": "application/json"}
  data = {"contents": [{"parts": [{"text": prompt_text}]}]}

  req_data = json.dumps(data).encode("utf-8")
  req = urllib.request.Request(url, data=req_data, headers=headers, method="POST")

  try:
    with urllib.request.urlopen(req) as response:
      res_body = response.read().decode("utf-8")
      res_json = json.loads(res_body)
      return res_json["candidates"][0]["content"]["parts"][0]["text"]
  except Exception as e:
    return f"API 호출 중 오류 발생: {e}"


# 스타일링 (CSS)
st.markdown(
    """
    <style>
    .chat-bubble {
        background-color: #f0f2f6;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 5px solid #4f46e5;
    }
    .teacher-tip {
        background-color: #fef3c7;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #d97706;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 사이드바: 수업 설정
st.sidebar.header("⚙️ 수업 환경 설정")
subject = st.sidebar.selectbox("교과 선택", ["국어", "사회/역사", "도덕/윤리", "기타"])
target_grade = st.sidebar.selectbox(
    "대상 학년", ["중학교 1-2학년", "중학교 3학년", "고등학교 1-2학년", "고등학교 3학년"]
)
lesson_topic = st.sidebar.text_input(
    "오늘의 핵심 학습 주제 / 키워드",
    placeholder="예: 매체 자료의 비판적 수용, 광고 속 오류",
)

st.sidebar.markdown("---")
generate_btn = st.sidebar.button(
    "🚀 AI 도입부 자료 생성하기", type="primary", use_container_width=True
)

# 메인 화면 타이틀
st.title("🤖 AI 수업 도우미 캐릭터 '똑똑이'")
st.markdown(
    "수업 시작 전, 학생들이 흥미를 갖고 몰입할 수 있도록 AI 캐릭터가 질문과"
    " 시사 사례를 만들어 드립니다!"
)

# 세션 스테이트 초기화
if "ai_data" not in st.session_state:
  st.session_state.ai_data = None

# API 호출 및 데이터 생성
if generate_btn:
  if not lesson_topic:
    st.warning("⚠️ 학습 주제나 키워드를 입력해 주세요!")
  elif not api_key:
    st.error(
        "❌ Gemini API 키가 설정되지 않았습니다. Streamlit secrets에"
        " `GEMINI_API_KEY`를 등록해 주세요."
    )
  else:
    with st.spinner("✨ 똑똑이가 수업 도입 자료를 열심히 준비하고 있어요..."):
      prompt = f"""
            당신은 학교 수업에서 학생들의 흥미를 유발하고 동기를 부여하는 친근하고 재치 있는 AI 캐릭터 '똑똑이'입니다.
            현재 교과: {subject}
            대상 학년: {target_grade}
            오늘의 학습 주제: {lesson_topic}

            위 조건에 맞춰 수업 도입부(시작 5분)에 활용할 수 있는 다음 내용을 마크다운 구조로 명확하게 작성해 주세요:
            1. **캐릭터 오프닝 멘트**: 학생들에게 친근하게 건네며 오늘 주제에 대한 호기심을 유발하는 말 (구어체로 생동감 있게)
            2. **사전 지식 활성화 질문 3가지**: 학생들이 가볍게 대답할 수 있거나 일상과 연관된 흥미로운 질문
            3. **수업과 세상의 연결 (시사/사례)**: 이 주제가 실제 삶이나 최근 뉴스, 트렌드와 어떻게 연결되는지 알기 쉬운 예시 2가지
            4. **교사를 위한 티칭 팁**: 교사가 이 도입을 활용해 수업을 자연스럽게 전개할 수 있는 짧은 조언
            """

      st.session_state.ai_data = generate_with_gemini(prompt, api_key)

# 결과 화면 출력
if st.session_state.ai_data:
  tab1, tab2 = st.tabs(["📢 수업 도입 화면 (학생용)", "💬 실시간 학생 반응 시뮬레이터"])

  with tab1:
    st.markdown("### 📌 오늘의 도입 브리핑")
    st.markdown(
        f"""
        <div class="chat-bubble">
            <h3>🤖 똑똑이 쌤의 한마디</h3>
            {st.session_state.ai_data}
        </div>
        """,
        unsafe_allow_html=True,
    )

  with tab2:
    st.markdown("### 💬 학생들이 입력한 사전 답변 시뮬레이션")
    st.markdown(
        "수업 중 학생들이 웹앱 링크로 들어와 입력한 생각들을 AI가 실시간으로"
        " 정리해 준다고 가정해 보세요."
    )

    col1, col2 = st.columns(2)
    with col1:
      sample_input = st.text_input(
          "학생 입장에서 대답해보기",
          placeholder="예: 유튜브 광고에서 본 것 같아요!",
      )
      if st.button("의견 보내기"):
        if sample_input:
          st.success(f"전송 완료: '{sample_input}'")

    with col2:
      st.markdown(
          """
            <div class="teacher-tip">
                <b>💡 실시간 AI 리액션 예시:</b><br>
                "오! 방금 OO 학생이 유튜브 광고를 언급해 줬네요! 맞아요, 오늘 우리가 배울 내용이 바로..."
            </div>
            """,
          unsafe_allow_html=True,
      )

else:
  st.info(
      "👈 왼쪽 사이드바에서 교과와 학습 주제를 입력하고 **[AI 도입부 자료"
      " 생성하기]** 버튼을 눌러보세요!"
  )