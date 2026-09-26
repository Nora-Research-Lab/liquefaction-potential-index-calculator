![NORA logo](https://i.ibb.co/0VJCC9Gf/IMG-20260114-WA0008.jpg)
 
# Liquefaction Potential Index Calculator
 
*For earthquake hazard analysts and geotechnical engineers: enter SPT blow counts, fines content, and ground motion parameters to instantly compute the factor of safety against liquefaction and the Liquefaction Potential Index (LPI) with a severity classification.*
 
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
 

## Overview
 
**Industry:** Earthquake / Hazard Analysis
 
This tool implements the simplified liquefaction evaluation procedure (Seed & Idriss 1971, updated Idriss & Boulanger 2008). The user provides the following inputs: (1) SPT blow count N (uncorrected, blows/ft or blows/30cm), (2) depth of the soil layer (m), (3) fines content FC (%), (4) total unit weight of soil (kN/m³), (5) depth to groundwater table (m), (6) earthquake moment magnitude Mw, (7) peak ground acceleration at surface amax (g). The tool computes: total vertical stress σv, effective vertical stress σv', stress reduction coefficient rd using the depth-dependent formula (rd = exp(α(z) + β(z) * Mw) with α and β given by Liao & Whitman), cyclic stress ratio CSR = 0.65 * (amax/g) * (σv/σv') * rd. Corrected blow count N1,60 is calculated using energy and overburden correction factors (CN = (Pa/σv')^0.5, capped at 1.7). A fines content adjustment adds ΔN1,60 = exp(1.63 + 9.7/FC - 0.01*(FC)^2) for FC<35% so that clean-sand equivalent N1,60cs = N1,60 + ΔN1,60. Cyclic resistance ratio CRR is computed from N1,60cs using Idriss & Boulanger's equation: CRR = exp((N1,60cs/14.1) + (N1,60cs/126)^2 - (N1,60cs/23.6)^3 + (N1,60cs/25.4)^4 - 2.8). Factor of safety FS = CRR/CSR. If FS ≤ 1, layer is liquefiable. LPI is then computed as the depth-weighted integral of (1-FS) for liquefiable layers over the top 20 m, with weighting function w(z)=10-0.5z (z in m). The output displays: FS for the layer, LPI value, and a severity classification: LPI=0 (none), 0<LPI≤5 (low), 5<LPI≤15 (moderate), 15<LPI≤85 (high), LPI>85 (very high). The Gradio UI uses number inputs with sliders (or numerical entry) for each parameter, a 'Calculate' button, and output components: a text box showing FS and LPI, and a color-coded severity indicator (e.g., an HTML/CSS block). No AI/ML component is used; all calculations are deterministic engineering equations.
 
## Run it
 
```bash
docker build -t liquefaction-potential-index-calculator .
docker run -p 7860:7860 liquefaction-potential-index-calculator
```
 
Then open http://localhost:7860 in your browser.
 
## About
 
This tool was generated and published automatically by the **NORA Earth Intelligence**
tool factory, an autonomous pipeline maintained by **NORA Research Lab** that turns
one idea per run into a small, working geoscience tool — end to end, with an
LLM writing and Docker-testing the code, and another model generating the
banner above.
 
- Platform: [https://noraearth.xyz](https://noraearth.xyz)
- Parent lab: [https://noraresearchlab.site](https://noraresearchlab.site)
 
Built 2026-09-26.
 
---
 
### Maintainer
 
**NORA Research Lab**
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
