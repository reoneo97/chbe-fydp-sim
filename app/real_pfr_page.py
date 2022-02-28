from matplotlib.pyplot import plot
import streamlit as st
from simulator.reaction import ptsa_reaction, ReactionModel
import simulator.const as const
from simulator.reactor import RealPFR
from loguru import logger
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def conversion_mean_plot(conversion_slc, vol_weights, z_axis, r_axis, time):
    normalised = conversion_slc@vol_weights
    df = pd.DataFrame([z_axis, normalised]).T
    # norm_temp = temp_slc*vol_weights
    df.columns = ["Length/Z-Axis (m)", "Conversion"]
    fig = px.line(
        df, x=df.columns[0], y=df.columns[1],
        title=f"Mean Conversion Plot for t={time} min")
    final_x, final_y = df.iloc[-1]
    fig.add_annotation(x=final_x, y=final_y,
                       text=f"Output Conversion={final_y:.4f}",
                       showarrow=True,
                       arrowhead=3,
                       xshift=-15)
    st.plotly_chart(fig)


def temperature_mean_plot(temp_slc, vol_weights, z_axis, r_axis, time):
    norm_T = temp_slc@vol_weights
    df = pd.DataFrame([z_axis, norm_T]).T
    # norm_temp = temp_slc*vol_weights
    df.columns = ["Length/Z-Axis (m)", "Temperature"]
    fig = px.line(
        df, x=df.columns[0], y=df.columns[1],
        title=f"Mean Temperature Plot for t={time} min")
    final_x, final_y = df.iloc[-1]
    fig.add_annotation(x=final_x, y=final_y,
                       text=f"Output Temperature={final_y:.4f}",
                       showarrow=True,
                       arrowhead=3,
                       xshift=-15)
    st.plotly_chart(fig)


def conversion_contour(conversion_slc, z_axis, r_axis):
    # Plotting is X x Y x Z which will translate to L x R x T
    contour_obj = go.Contour(
        z=conversion_slc.T, x=z_axis, y=r_axis
    )
    fig = go.Figure(contour_obj)
    fig.layout.xaxis.title = "Length/Z-axis Profile (m)"
    fig.layout.yaxis.title = "Radius Profile (m)"
    st.plotly_chart(fig)


def temperature_contour(temp_slc, z_axis, r_axis):
    # Plotting is X x Y x Z which will translate to L x R x T
    contour_obj = go.Contour(
        z=temp_slc.T, x=z_axis, y=r_axis
    )
    fig = go.Figure(contour_obj)
    fig.layout.xaxis.title = "Length/Z-axis Profile (m)"
    fig.layout.yaxis.title = "Radius Profile (m)"
    st.plotly_chart(fig)


def real_pfr():

    # Session State Variables
    if 'simulation_done' not in st.session_state:
        st.session_state['simulation_done'] = False
        st.session_state["simulation_data"] = None
        st.session_state["vol_intervals"] = None

    st.header("Real PFR Design")
    st.subheader("[WIP] ⚠️ Not Completed!")
    st.markdown(
        """Real PFR design makes several assumptions:

            1. Concentration profile within the PFR is radially uniform
            2. There is no back-mixing within the reactor
            3. Heat transfer is radial

            """
    )

    st.subheader("Choosing Design Parameters:")

    col1, _, col2 = st.columns([8, 1, 8])
    with col1:
        st.markdown("#### Reactor Conditions:")
        pa_feed_hr = st.slider("Palmitic Acid Feed (kmol//hr)",
                               min_value=1., max_value=100., value=80.31)
        pa_feed = pa_feed_hr/60
        M = st.slider("Molar Ratio (Isopropyl Alcohol/Palmitic Acid)",
                      min_value=1, max_value=25, value=5)
        feed_temp = st.slider("Feed Temperature (K)",
                              min_value=293., max_value=480., value=393.)
        heat_temp = st.slider("Heater Temperature (K)",
                              min_value=373., max_value=523., value=420.)
    with col2:
        st.markdown("#### Reactor Dimensions")
        L = st.slider("Reactor Length", min_value=0.1,
                      max_value=20., step=0.1, value=4.)
        R = st.slider("Reactor Radius", min_value=0.05,
                      max_value=10., step=0.05, value=1.25)
        space_interval = st.slider(
            "Space Interval", min_value=51, max_value=101, step=50,)
        time_end = st.slider(
            "Simulation Time End", min_value=100., max_value=300., step=50.
        )

    time_interval = 0.1
    # time_end = 100.
    sim_btn = st.button("Run Simulation")
    if sim_btn:
        model = RealPFR(pa_feed, M, L, R, feed_temp, heat_temp, space_interval)
        with st.spinner("Running Simulation"):
            sim_data = model.run(time_interval, time_end)

            st.session_state["simulation_done"] = True
            st.session_state["simulation_data"] = sim_data
            ls, rs = model.get_dimensions()
            vol_weights = model.get_radial_volumes()
            st.session_state["z_axis"] = ls
            st.session_state["r_axis"] = rs
            st.session_state["vol_weights"] = vol_weights

    st.markdown("---")
    st.write(st.session_state["simulation_done"])

    plot_container = st.container()

    with plot_container:
        st.header("Conversion Visualization 📈")
        if st.session_state["simulation_done"]:
            simulation_data = st.session_state["simulation_data"]
            time_slider = st.slider(
                "Time Slider", 0., time_end, value=0., step=time_interval,)

            time_index = min(int(time_slider/time_interval),
                             len(simulation_data)-1)

            data_slc = simulation_data[time_index, :]
            plot_col1, _, plot_col2 = st.columns([8, 1, 8])
            z_axis = st.session_state["z_axis"]
            r_axis = st.session_state["r_axis"]
            vol_weights = st.session_state["vol_weights"]
            with plot_col1:
                st.markdown("### **<ins>Temperature Plots</ins>**",
                            unsafe_allow_html=True)
                temp_slc = data_slc[:, :, 0]
                st.markdown("#### Temperature Contour")
                temperature_contour(
                    temp_slc, z_axis, r_axis
                )
                st.markdown("#### Average Temperature Line Plot")
                temperature_mean_plot(
                    temp_slc, vol_weights, z_axis, r_axis, time_slider)
            with plot_col2:
                st.markdown("### **<ins>Conversion Plots</ins>**",
                            unsafe_allow_html=True)
                conv_slc = data_slc[:, :, -1]
                st.markdown("#### Conversion Contour")
                conversion_contour(
                    conv_slc,
                    st.session_state["z_axis"], st.session_state["r_axis"]
                )
                st.markdown("#### Average Conversion Line Plot")
                conversion_mean_plot(
                    conv_slc, vol_weights, z_axis, r_axis, time_slider)
            vol_weights = st.session_state["vol_weights"]

            st.markdown("---")
            st.subheader("Reactor Output Information")

            output_slc = simulation_data[len(simulation_data)-1, -1, :, :]
            output_temp_slc = output_slc[:, 0]
            output_conc_slc = output_slc[:, 1:6]

            output_temp = output_temp_slc@vol_weights
            output_concs = output_conc_slc.T@vol_weights
            output_conversion = output_slc[:, -1]@vol_weights
            output_df = pd.DataFrame(
                [output_concs],
                columns=[
                    "Palmitic Acid Concentration", "IPA Concentration",
                    "IPP Concentration", "Water Concentration",
                    "Linoleic Acid Concentration"])
            st.write(output_df)
            st.write(f"Output Temperature: {output_temp:.2f}K")
            st.write(f"Output Conversion: {output_conversion:.3f}")
