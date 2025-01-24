import streamlit as st
from streamlit_echarts import st_pyecharts
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Pie
from pyecharts.charts import Line
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType
import pandas as pd

#按钮点击事件-数据展示
def load_show():
    df = pd.read_excel('./data/new_df.xlsx')
    return df

if __name__ == '__main__':
    #侧边栏布局
    st.sidebar.text('数据加载+展示:')
    #数据加载+展示
    isClick_btn2 = st.sidebar.button(label='一键启动')
    if isClick_btn2:
        df = load_show()
        # 折叠展示数据表格
        with st.expander("岗位信息", expanded=True):
            st.write(df)

    #侧边栏下拉框
    add_selectbox = st.sidebar.selectbox(
        label="数据分析:",
        options=('请选择','各区最低房价和最高房价可视化','各区小区数量占比图',"各区房价均值分析")
    )
    #获取下拉选项
    if add_selectbox == '各区最低房价和最高房价可视化':
        df = load_show()
        # 按区分组，展示分区后的房价最便宜的房价小区名
        data1 = df.groupby(by='所在区域')[["房屋单价/㎡", "小区名称"]].min()
        sheet1 = data1.reset_index()

        # 按区分组最高价
        data2 = df.groupby(by='所在区域')[["房屋单价/㎡", "小区名称"]].max()
        sheet2 = data2.reset_index()

        #绘制柱状图
        # 柱状图展示分区后的最值价格
        list2 = sheet1['房屋单价/㎡'].tolist()

        list3 = sheet2['房屋单价/㎡'].tolist()

        list4 = sheet1['所在区域'].tolist()

        c = (
            Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
            .add_xaxis(list4)
            .add_yaxis("各区最低房价", list2, stack="stack1", category_gap="50%")
            .add_yaxis("各区最高房价", list3, stack="stack1", category_gap="50%")
            .set_global_opts(
                title_opts=opts.TitleOpts(title="苏州各地区房屋最值", subtitle="最大值和最小值"),
            )
            .set_series_opts(
                label_opts=opts.LabelOpts(
                    position="center",
                    formatter=JsCode(
                        "function(x){return Number(x.data) + '元';}"
                    ),
                )
            )
        )
        st_pyecharts(c)

    if add_selectbox == '各区小区数量占比图':
        df = load_show()
    # 分析各区的房子占比数量
        bing = df.groupby(by='所在区域')['小区名称'].count().reset_index()
        bing_ = bing.rename(columns={"小区名称": "小区数量"})
        l_1 = bing_["所在区域"].tolist()
        l_2 = bing_['小区数量'].tolist()
        data_ = []
        for i in range(len(l_1)):
            data_.append((l_1[i], l_2[i]))

        #生成饼图
        b = (
            Pie()
            .add(
                "", data_,
                center=["40%", "50%"],
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(title="各区小区数量占比图"),
                legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"),
            )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            .set_colors(["blue", "green", "yellow", "red", "pink", "orange", "purple"])
        )
        st_pyecharts(b)

    if add_selectbox == "各区房价均值分析":
        df = load_show()
        sheet15 = df.groupby(by="所在区域")['房屋单价/㎡'].mean().reset_index()
        sheet15['房屋单价/㎡'] = sheet15['房屋单价/㎡'].astype(int)
        x_data = sheet15['所在区域'].tolist()
        y_data = sheet15['房屋单价/㎡'].tolist()

        d = (
            Line()
            .set_global_opts(
                title_opts=opts.TitleOpts(title="各区房价均值变化"),
                tooltip_opts=opts.TooltipOpts(is_show=False),
                xaxis_opts=opts.AxisOpts(type_="category"),
                yaxis_opts=opts.AxisOpts(
                    type_="value",
                    axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                ),
            )
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
                series_name="",
                y_axis=y_data,
                symbol="emptyCircle",
                is_symbol_show=True,
                label_opts=opts.LabelOpts(is_show=False),
            )
        )
        st_pyecharts(d)

