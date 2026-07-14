import streamlit as st
import pandas as pd

# 1. 웹앱 제목 설정
st.title("🔥 소방청 전기차 화재 발생 현황 대시보드 (2024)")
st.markdown("업로드된 데이터를 바탕으로 **시도별** 및 **발화요인별** 화재 발생 현황을 분석합니다.")
st.write("---")

# 2. 데이터 불러오기 (한글 인코딩 반영)
# 파일명이 정확히 일치해야 합니다. (동일 디렉토리에 위치 권장)
file_name = "소방청_전기차 화재 발생 현황_20241231.csv"

@st.cache_data
def load_data(path):
    try:
        df = pd.read_csv(path, encoding="cp949")
        return df
    except FileNotFoundError:
        st.error(f"'{path}' 파일을 찾을 수 없습니다. 파일명을 확인해주세요.")
        return None
    except Exception as e:
        st.error(f"데이터를 읽어오는 중 오류가 발생했습니다: {e}")
        return None

df = load_data(file_name)

if df is not None:
    # 3. 사이드바 - 시도별 필터링 기능 추가 (선택 사항)
    st.sidebar.header("🔍 데이터 필터링")
    all_sido = ["전체"] + list(df["시도"].unique())
    selected_sido = st.sidebar.selectbox("조회할 시도를 선택하세요", all_sido)
    
    # 필터링 적용
    if selected_sido != "전체":
        filtered_df = df[df["시도"] == selected_sido]
    else:
        filtered_df = df

    # 4. 전체 데이터 요약 지표
    st.subheader("📊 화재 통계 요약")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="총 화재 발생 건수", value=f"{len(filtered_df)} 건")
    with col2:
        st.metric(label="분석 대상 시도 수", value=f"{filtered_df['시도'].nunique()} 개 지역")
        
    st.write("---")

    # 5. [그래프 1] 시도별 화재 발생 빈도
    st.subheader("📍 1) 시도별 화재 발생 빈도")
    # 시도별 빈도 계산 후 DataFrame으로 변환
    sido_counts = filtered_df["시도"].value_counts().reset_index()
    sido_counts.columns = ["시도", "화재건수"]
    # 차트 출력을 위해 인덱스 설정
    sido_chart_data = sido_counts.set_index("시도")
    
    st.bar_chart(sido_chart_data)
    
    # 6. [그래프 2] 발화 요인별 화재 발생량 (막대 그래프)
    st.subheader("⚡ 2) 발화 요인별 화재 발생량")
    # 발화요인대분류별 빈도 계산 후 DataFrame으로 변환
    factor_counts = filtered_df["발화요인대분류"].value_counts().reset_index()
    factor_counts.columns = ["발화요인대분류", "화재건수"]
    factor_chart_data = factor_counts.set_index("발화요인대분류")
    
    st.bar_chart(factor_chart_data)

    st.write("---")

    # 7. 상세 데이터 및 발화요인소분류 확인
    st.subheader("📋 화재 현황 데이터 목록")
    st.markdown(f"**선택된 지역:** {selected_sido}")
    
    # 주요 열만 보기 좋게 추출
    display_df = filtered_df[["화재발생년월일", "시도", "시군구", "발화요인대분류", "발화요인소분류", "차량장소", "차량상태"]]
    st.dataframe(display_df, use_container_width=True)
