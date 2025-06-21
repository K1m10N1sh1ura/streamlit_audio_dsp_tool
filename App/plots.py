import streamlit as st
import plotly.graph_objects as go
import numpy as np
from scipy import signal as sp_signal

def render_plot():
    tab1, tab2, tab3 = st.tabs(["Signal (Time Domain)", "Spectrum (Frequency Domain)", "Spectrogram"])

    with tab1:
        fig_signal = go.Figure()
        for signal in st.session_state.signals:
            if signal["active"]:
                # Zeitvektor berechnen
                N = len(signal["data"])
                t = np.arange(N) / signal["fs"]
                fig_signal.add_trace(go.Scatter(
                    x=t,
                    y=signal["data"],
                    mode="lines",
                    name=signal["name"],
                    line=dict(color=signal["color"])
                ))
        fig_signal.update_layout(
            title="AudioLab Signalplot",
            xaxis_title="Time [s]",
            yaxis_title="Amplitude",
            template="plotly_dark",
            height=600
        )
        st.plotly_chart(fig_signal, use_container_width=True)

    with tab2:
        fig_spectrum = go.Figure()
        for signal in st.session_state.signals:
            if signal["active"]:
                N = len(signal["data"])
                freq = np.fft.rfftfreq(N, d=1.0/signal["fs"])
                fft_magnitude = np.abs(np.fft.rfft(signal["data"]))

                fig_spectrum.add_trace(go.Scatter(
                    x=freq,
                    y=20 * np.log10(fft_magnitude + 1e-12),
                    mode="lines",
                    name=signal["name"],
                    line=dict(color=signal["color"])
                ))
        fig_spectrum.update_layout(
            title="Spectrum (FFT Magnitude)",
            xaxis_title="Frequency [Hz]",
            yaxis_title="Amplitude [dB]",
            template="plotly_dark",
            height=600
        )
        st.plotly_chart(fig_spectrum, use_container_width=True)

    with tab3:
        st.markdown("### Spectrogram")
        active_signals = [s for s in st.session_state.get("signals", []) if s["active"]]

        if not active_signals:
            st.warning("No active signals to display.")
        else:
            signal_names = [s["name"] for s in active_signals]
            selected_signal_name = st.selectbox(
                "Select a signal for the spectrogram",
                options=signal_names
            )

            selected_signal = next((s for s in active_signals if s["name"] == selected_signal_name), None)

            if selected_signal:
                fs = selected_signal["fs"]
                data = selected_signal["data"]

                f, t, Sxx = sp_signal.spectrogram(data, fs)

                fig_spectrogram = go.Figure(data=go.Heatmap(
                    z=10 * np.log10(Sxx + 1e-9),
                    x=t,
                    y=f,
                    colorscale='Viridis',
                    colorbar={"title": "Power/Frequency [dB/Hz]"}
                ))

                fig_spectrogram.update_layout(
                    title=f'Spectrogram of "{selected_signal["name"]}"',
                    xaxis_title="Time [s]",
                    yaxis_title="Frequency [Hz]",
                    template="plotly_dark",
                    height=600
                )
                st.plotly_chart(fig_spectrogram, use_container_width=True)
