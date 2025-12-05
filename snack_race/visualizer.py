import plotly.graph_objects as go
import plotly.colors as pc
import pandas as pd
import numpy as np
from .constants import FRAME_DURATION, GOAL, CHART_WIDTH



def visualize(df: pd.DataFrame):
    # -----------------------------
    # 설정 준비
    # -----------------------------
    names = df["name"].unique()
    palette = pc.qualitative.Alphabet

    # 이름 순서대로 색상을 하나씩 꺼내서 매핑
    # (혹시 26명이 넘어가면 % 연산자로 다시 첫 번째 색부터 순환)
    color_map = {name: palette[i % len(palette)] for i, name in enumerate(names)}
    times = df["time"].unique()
    init_t = times[0]
    init_df = df[df["time"] == init_t].sort_values("pos", ascending=True)

    BAR_GAP = 0.15
    num_ppl = len(names)
    BUFFER = 300
    ROW_HEIGHT = 100
    chart_height =(num_ppl * ROW_HEIGHT) + BUFFER
    # -----------------------------
    # Figure 생성
    # -----------------------------
    fig = go.Figure(
        data=[
            go.Bar(
                x=init_df["pos"].values,
                y=init_df["name"].values,
                ids=init_df["name"].values,  # 객체 일관성 유지 (부드러운 이동 핵심)
                orientation="h",
                marker_color=[color_map[n] for n in init_df["name"]],
                text=init_df["name"].values,
                texttemplate='<b>%{y}</b> (%{x:,.0f})',
                textposition="outside"
            )
        ],
        layout=go.Layout(
            width=CHART_WIDTH,
            height=chart_height,
            bargap=BAR_GAP,
            xaxis=dict(range=[0, df["pos"].max() * 1.1], title="Score"),
            yaxis=dict(title="", showticklabels=False, ticks=""),
            title={
                'text': f"Snack Race - Time: {init_t}",
                'y': 0.95,  # 타이틀 위치 조정
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            # 버튼이 잘리지 않도록 상단 여백(t)을 넉넉히 줍니다.
            margin=dict(l=20, r=20, t=100, b=20),

            # [수정됨] 버튼 설정
            updatemenus=[
                dict(
                    type="buttons",
                    direction="right",  # 버튼을 가로로 나열
                    x=0.0,  # 왼쪽 정렬
                    y=2,  # 차트 위쪽 공간 (1.0이 차트 끝선)
                    xanchor='left',
                    yanchor='top',
                    showactive=False,  # 버튼 눌림 상태 표시 끄기
                    buttons=[
                        dict(
                            label="Play",
                            method="animate",
                            args=[None, {
                                "frame": {"duration": FRAME_DURATION, "redraw": False},
                                "transition": {"duration": FRAME_DURATION, "easing": "cubic-in-out"}
                            }]
                        ),
                        dict(
                            label="Pause",
                            method="animate",
                            args=[[None], {
                                "frame": {"duration": 0, "redraw": False},
                                "mode": "immediate",
                                "transition": {"duration": 0}
                            }]
                        )
                    ],
                    pad={"r": 10, "t": 10}  # 버튼 내부 여백
                )
            ]
        )
    )

    fig.add_vline(
        x=GOAL,
        line_width=2,
        line_dash="dash",
        line_color="red",
        annotation_text=f"GOAL({GOAL})",  # (선택) 텍스트 주석
        annotation_position="top right"
    )


    # -----------------------------
    # 애니메이션 프레임 생성
    # -----------------------------
    frames = []
    for t in times:
        frame_df = df[df["time"] == t]
        ranked = frame_df.sort_values("pos", ascending=True)

        frames.append(
            go.Frame(
                name=str(t),
                data=[
                    go.Bar(
                        ids=ranked["name"].values,
                        x=ranked["pos"].values,
                        y=ranked["name"].values,
                        orientation="h",
                        marker_color=[color_map[n] for n in ranked["name"]],
                        text=ranked["name"].values,
                        texttemplate='<b>%{y}</b> (%{x:,.0f})',
                        textposition="outside"
                    )
                ],
                layout=go.Layout(title={'text': f"Snack Race - Time: {t}"})
            )
        )

    fig.frames = frames
    # -----------------------------
    # 슬라이더 설정
    # -----------------------------
    slider_steps = []
    for t in times:
        slider_steps.append(
            dict(
                args=[[str(t)], {
                    "frame": {"duration": 0, "redraw": False},
                    "mode": "immediate",
                    "transition": {"duration": 0, "easing": "cubic-in-out"}
                }],
                label=str(t),
                method="animate"
            )
        )

    sliders = [dict(
        active=0,
        currentvalue={"prefix": "Time: "},
        pad={"t": 50},
        steps=slider_steps
    )]

    fig.update_layout(sliders=sliders)

    fig.show()