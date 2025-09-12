import altair as alt
import pandas as pd
import pydeck
import streamlit as st


def _chart_st_wrapper(chart, st_wrapper):
    if st_wrapper:
        return st.altair_chart(chart, use_container_width=True)
    else:
        return chart


class Altair:
    @staticmethod
    def time_series(df: pd.DataFrame, ylabel: str, color: str, st_wrapper: bool):

        df["label"] = ylabel
        band = (
            alt.Chart(df)
            .mark_errorband()
            .encode(
                alt.Y(
                    "max:Q",
                    axis=alt.Axis(title=ylabel, titleColor=color, titleFontSize=18),
                ).scale(zero=False),
                alt.Y2("min:Q"),
                alt.X("datetime:T").title(None),
                tooltip=alt.value(None),  # tooltip for error band plot is buggy
                color=alt.value(color),
            )
        )

        line = (
            alt.Chart(df)
            .mark_line(stroke=color)
            .encode(
                alt.Y("avg:Q"),
                alt.X("datetime:T"),
                tooltip=[
                    alt.Tooltip(field="label", title="label"),
                    "min",
                    "max",
                    "avg",
                    alt.Tooltip(
                        "yearmonthdatehoursminutesseconds(datetime)", title="datetime"
                    ),
                ],
            )
        )

        chart = alt.layer(band, line).interactive()

        return _chart_st_wrapper(chart, st_wrapper)

    @staticmethod
    def time_series_two_sensors(
        df1,
        ylabel1,
        sensor_type1,
        color1,
        df2,
        ylabel2,
        sensor_type2,
        color2,
        st_wrapper,
    ):
        if sensor_type1 == sensor_type2:
            df1["label"] = ylabel1
            df2["label"] = ylabel2
            df = pd.concat([df1, df2])
            band = (
                alt.Chart(df)
                .mark_errorband()
                .encode(
                    alt.Y("max:Q").scale(zero=False).title(None),
                    alt.Y2("min:Q"),
                    alt.X("datetime:T").title(None),
                    alt.Color("label:N")
                    .scale(domain=[ylabel1, ylabel2], range=[color1, color2])
                    .legend(orient="top", labelLimit=1000)
                    .title(None),
                    tooltip=alt.value(None),  # tooltip for error band plot is buggy
                )
            )

            line = (
                alt.Chart(df)
                .mark_line()
                .encode(
                    alt.Y("avg:Q"),
                    alt.X("datetime:T"),
                    alt.Color("label:N"),
                    tooltip=[
                        alt.Tooltip(field="label", title="label"),
                        "min",
                        "max",
                        "avg",
                        alt.Tooltip(
                            "yearmonthdatehoursminutesseconds(datetime)",
                            title="datetime",
                        ),
                    ],
                )
            )

            chart = alt.layer(band, line).interactive()
        else:
            chart1 = Altair.time_series(df1, ylabel1, color1, st_wrapper=False)
            chart2 = Altair.time_series(df2, ylabel2, color2, st_wrapper=False)
            chart = (
                alt.layer(chart1, chart2).resolve_scale(y="independent").interactive()
            )

        return _chart_st_wrapper(chart, st_wrapper)

    @staticmethod
    def table_archive_files(df, st_wrapper):
        if st_wrapper:
            return st.dataframe(
                df,
                column_config={
                    "dataProductCode": "DP Code",
                    "filename": st.column_config.LinkColumn(
                        "Filename",
                        display_text="https://.*filename=(.*?)&token=.*",
                    ),
                    "dateFrom": "From",
                    "dateTo": "To",
                    "uncompressedFileSize": "File Size",
                },
                width="stretch",
                hide_index=True,
            )
        else:
            return df

    @staticmethod
    def scatter_plot(df, st_wrapper):
        col1, col2 = df.columns[0], df.columns[1]

        chart = (
            alt.Chart(df)
            .mark_circle()
            .encode(
                alt.X(col1).scale(zero=False),
                alt.Y(col2).scale(zero=False),
                tooltip=[
                    col1,
                    col2,
                    alt.Tooltip(
                        "yearmonthdatehoursminutesseconds(sampleTimes)",
                        title="sampleTimes",
                    ),
                ],
            )
            .interactive()
        )

        return _chart_st_wrapper(chart, st_wrapper)

    @staticmethod
    def heatmap_archive_files(df, st_wrapper, marker_width=3, height_per_row=120):
        chart = (
            alt.Chart(df)
            .mark_rect(width=marker_width)
            .encode(
                x=alt.X("hoursminutes(dateFrom):T").title(None),
                y=alt.Y("monthdate(dateFrom):O").title(None),
                yOffset=alt.Row("dataProductCode:N").title(None),
                color="dataProductCode:N",
                href="filename:N",
                tooltip=[
                    alt.Tooltip(
                        "yearmonthdatehoursminutesseconds(dateFrom)", title="dateFrom"
                    ),
                    "dataProductCode",
                ],
            )
            .properties(height=height_per_row * df["dataProductCode"].nunique())
            .resolve_scale(x="independent")
            .interactive()
        )
        return _chart_st_wrapper(chart, st_wrapper)

    @staticmethod
    def map(df, initial_view_state, st_wrapper):
        point_layer = pydeck.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["lon", "lat"],
            get_color="[255, 0, 0]",
            radius_min_pixels=3,
            auto_highlight=True,
            pickable=True,
        )

        tooltip = []
        for key in [
            "locationCode",
            "location_code",
            "locationName",
            "location_name",
            "deviceCode",
            "device_code",
            "deviceName",
            "device_name",
        ]:
            if key in df.columns:
                tooltip.append(f"{key}: {{{key}}}")

        chart = pydeck.Deck(
            map_style=None,
            layers=point_layer,
            initial_view_state=initial_view_state,
            tooltip={
                "text": "\n".join(tooltip),
            },
        )
        if st_wrapper:
            return st.pydeck_chart(chart)
        else:
            return chart
