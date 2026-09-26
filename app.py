import gradio as gr
from liquefaction_potential_index_calculator import compute_lpi

def run_calculation(N, depth, FC, unit_weight, dw, Mw, amax):
    if N <= 0 or depth <= 0 or FC < 0 or unit_weight <= 0 or dw < 0 or Mw <= 0 or amax <= 0:
        return "All inputs must be positive. Depth and unit weight must be > 0.", "", ""
    try:
        fs, lpi, severity = compute_lpi(N, depth, FC, unit_weight, dw, Mw, amax)
    except ZeroDivisionError:
        return "Error: effective vertical stress is zero (check depth and water table).", "", ""
    except Exception as e:
        return f"Error: {str(e)}", "", ""

    # Determine colour for severity
    if severity == "None":
        color = "#4CAF50"
    elif severity == "Low":
        color = "#FFEB3B"
    elif severity == "Moderate":
        color = "#FF9800"
    elif severity == "High":
        color = "#F44336"
    else:  # Very High
        color = "#880E4F"

    html_block = f"""
    <div style="padding:12px; border-radius:8px; background-color:{color}; color:white; font-weight:bold; text-align:center;">
    {severity}
    </div>
    """
    result_text = f"Factor of Safety (FS): {fs:.3f}\nLiquefaction Potential Index (LPI): {lpi:.3f}"
    return result_text, html_block, severity

with gr.Blocks(title="Liquefaction Potential Index Calculator") as demo:
    gr.Markdown("# Liquefaction Potential Index Calculator")
    gr.Markdown("Simplified Seed-Idriss procedure with Idriss & Boulanger (2008) updates.")

    with gr.Row():
        with gr.Column():
            N_input = gr.Number(label="SPT Blow Count N (uncorrected)", value=15, minimum=0.1)
            depth_input = gr.Number(label="Depth of layer (m)", value=6, minimum=0.1)
            fc_input = gr.Number(label="Fines content FC (%)", value=25, minimum=0, maximum=100)
            unit_wt_input = gr.Number(label="Total unit weight (kN/m³)", value=18.5, minimum=0.1)
            dw_input = gr.Number(label="Depth to groundwater table (m)", value=3, minimum=0)
            Mw_input = gr.Number(label="Earthquake magnitude Mw", value=6.5, minimum=0.1, maximum=10)
            amax_input = gr.Number(label="Peak ground acceleration amax (g)", value=0.2, minimum=0.001)
            calc_btn = gr.Button("Calculate")
        with gr.Column():
            result_text = gr.Textbox(label="Results", lines=4)
            severity_html = gr.HTML(label="Severity")
            severity_label = gr.Label(visible=False)  # hidden, used for reference

    calc_btn.click(
        fn=run_calculation,
        inputs=[N_input, depth_input, fc_input, unit_wt_input, dw_input, Mw_input, amax_input],
        outputs=[result_text, severity_html, severity_label]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
