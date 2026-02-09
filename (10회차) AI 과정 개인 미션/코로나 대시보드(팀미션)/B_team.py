# b_team.py
# 👉 이 파일 이름이야. 팀 B가 쓰는 코드라는 뜻일 수도 있어

import pandas as pd
# 👉 pandas라는 라이브러리를 pd라는 짧은 이름으로 불러와
# 👉 표(DataFrame) 다룰 때 쓰는 도구야

import plotly.graph_objects as go
# 👉 plotly에서 그래프 만드는 도구를 가져와
# 👉 go는 그래프 객체(Graph Object)라는 뜻이야


def run_market_map_slider(df, selected_regions):
    """
    df: app.py에서 기간 필터까지 적용된 DataFrame(filtered_df)
    selected_regions: 사이드바에서 선택된 지역 리스트
    return: plotly Figure (Treemap + 날짜 슬라이더)
    """
    # 👉 이 함수는 "마켓맵 + 날짜 슬라이더 그래프"를 만들어서 돌려줘

    df = df.copy()
    # 👉 원본 df를 망가뜨리지 않으려고 복사본을 하나 만들어


    # 날짜 처리/정렬
    df["date"] = pd.to_datetime(df["date"])
    # 👉 date 컬럼을 "날짜 타입"으로 바꿔줘 (문자 → 날짜)

    df = df.sort_values("date")
    # 👉 날짜 순서대로 정렬해 (옛날 → 최신)


    # ✅ 선택 지역만 사용 (df에 존재하는 컬럼만)
    regions = [r for r in selected_regions if r in df.columns]
    # 👉 사용자가 고른 지역 중에서
    # 👉 실제 df에 존재하는 컬럼만 골라서 regions에 넣어

    if not regions:
        return None
        # 👉 만약 쓸 지역이 하나도 없으면
        # 👉 그래프 못 만드니까 그냥 None 반환하고 끝


    # 숫자 변환
    df[regions] = df[regions].apply(pd.to_numeric, errors="coerce").fillna(0)
    # 👉 지역 컬럼들을 숫자로 바꿔
    # 👉 숫자가 아닌 건 NaN으로 만들고
    # 👉 NaN은 전부 0으로 채워


    # ✅ 누적합 (이미 누적 데이터면 이 줄 주석처리)
    df_cum = df.copy()
    # 👉 누적값 계산용으로 df를 또 하나 복사해

    df_cum[regions] = df_cum[regions].cumsum()
    # 👉 날짜가 지날수록 값이 계속 더해지게 만들어 (누적합)


    dates = df_cum["date"].dt.strftime("%Y-%m-%d").tolist()
    # 👉 날짜를 "YYYY-MM-DD" 문자열로 바꿔서
    # 👉 리스트로 만들어 (슬라이더용)


    labels = regions
    # 👉 트리맵에 보여줄 이름들 (지역 이름)

    parents = [""] * len(regions)
    # 👉 트리맵에서 부모가 없다는 뜻
    # 👉 전부 최상위 박스야


    # 프레임 생성(날짜별)
    frames = []
    # 👉 날짜 하나당 하나의 화면(frame)을 만들 거야

    for i, d in enumerate(dates):
        # 👉 날짜 리스트를 하나씩 돌면서
        # 👉 i = 인덱스, d = 날짜 문자열

        row = df_cum.iloc[i]
        # 👉 i번째 날짜의 한 줄 데이터를 가져와

        values = [row[r] for r in regions]
        # 👉 각 지역의 누적값을 리스트로 만들어


        frames.append(
            go.Frame(
                name=d,
                # 👉 이 프레임의 이름은 날짜야 (슬라이더랑 연결됨)

                data=[go.Treemap(
                    labels=labels,
                    # 👉 박스 이름 = 지역 이름

                    parents=parents,
                    # 👉 부모 없음 (전부 루트)

                    values=values,
                    # 👉 박스 크기 = 누적값

                    marker=dict(
                        colors=values,
                        # 👉 값이 클수록 색이 진해져

                        colorscale="Reds"
                        # 👉 빨간색 계열로 색칠
                    ),

                    textinfo="label+value",
                    # 👉 박스 안에 이름 + 숫자 표시

                    hovertemplate="<b>%{label}</b><br>누적값: %{value:,}<extra></extra>",
                    # 👉 마우스 올리면 나오는 설명
                )],

                layout=go.Layout(
                    title_text=f"마켓맵 (기준일: {d})"
                    # 👉 위에 제목 표시 (현재 날짜)
                )
            )
        )


    # 초기 화면
    init_row = df_cum.iloc[0]
    # 👉 제일 첫 번째 날짜 데이터

    init_values = [init_row[r] for r in regions]
    # 👉 첫 날짜의 지역별 누적값


    fig = go.Figure(
        data=[go.Treemap(
            labels=labels,
            parents=parents,
            values=init_values,
            # 👉 처음 화면에 보여줄 값들

            marker=dict(
                colors=init_values,
                colorscale="Reds"
            ),

            textinfo="label+value",
            hovertemplate="<b>%{label}</b><br>누적값: %{value:,}<extra></extra>",
        )],

        frames=frames
        # 👉 아까 만든 날짜별 프레임들 연결
    )


    # 슬라이더
    steps = []
    # 👉 슬라이더의 한 칸 한 칸(step)을 만들 리스트

    for d in dates:
        # 👉 날짜 하나당 슬라이더 한 칸

        steps.append(dict(
            method="animate",
            # 👉 애니메이션 실행 방식

            args=[[d], {
                "mode": "immediate",
                # 👉 바로 바뀌게

                "frame": {"duration": 0, "redraw": True},
                # 👉 프레임 전환 시간 0초

                "transition": {"duration": 0}
                # 👉 부드러운 전환 없음
            }],

            label=""  
            # 👉 슬라이더 글자는 숨김 (막대만 보이게)
        ))


    fig.update_layout(
        height=700,
        # 👉 그래프 높이

        margin=dict(t=120, l=10, r=10, b=140),
        # 👉 위/아래/좌/우 여백 설정


        updatemenus=[dict(
            type="buttons",
            # 👉 버튼 메뉴 만들기

            direction="left",
            # 👉 버튼을 왼쪽부터 나열

            showactive=False,
            # 👉 눌린 상태 표시 안 함

            x=0.0,
            y=1.25,
            # 👉 버튼 위치 (그래프 위쪽)

            xanchor="left",
            yanchor="top",

            buttons=[
                dict(
                    label="▶ 재생",
                    # 👉 재생 버튼

                    method="animate",
                    args=[None, {
                        "frame": {"duration": 300, "redraw": True},
                        # 👉 0.3초마다 다음 날짜로

                        "transition": {"duration": 0},
                        "fromcurrent": True,
                        "mode": "immediate"
                    }]
                ),

                dict(
                    label="⏸ 정지",
                    # 👉 멈춤 버튼

                    method="animate",
                    args=[[None], {
                        "frame": {"duration": 0, "redraw": False},
                        "mode": "immediate"
                    }]
                ),
            ]
        )],

        sliders=[dict(
            active=0,
            # 👉 처음 선택된 슬라이더 위치

            x=0.05,
            len=0.90,
            # 👉 슬라이더 길이와 위치

            y=0.0,
            yanchor="bottom",
            # 👉 화면 맨 아래 고정

            pad={"t": 10, "b": 0},
            # 👉 슬라이더 여백

            currentvalue={"prefix": "기준일: "},
            # 👉 현재 날짜 앞에 붙는 글자

            steps=steps
            # 👉 아까 만든 날짜별 스텝들
        )],
    )

    return fig
    # 👉 완성된 그래프를 app.py로 돌려줘
