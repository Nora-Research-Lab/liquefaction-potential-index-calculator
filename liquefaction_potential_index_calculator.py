import math

def compute_lpi(N, depth, FC, unit_weight, dw, Mw, amax):
    """
    Compute factor of safety and liquefaction potential index for a single soil layer.

    Parameters
    ----------
    N : float
        SPT blow count (uncorrected, blows per foot or 30 cm)
    depth : float
        Depth of the soil layer (m)
    FC : float
        Fines content (%)
    unit_weight : float
        Total unit weight of soil (kN/m³)
    dw : float
        Depth to groundwater table (m)
    Mw : float
        Earthquake moment magnitude
    amax : float
        Peak ground acceleration at surface (g)

    Returns
    -------
    fs : float
        Factor of safety (CRR/CSR)
    lpi : float
        Liquefaction Potential Index (see assumptions)
    severity : str
        Classification string: None, Low, Moderate, High, Very High
    """
    # Constants
    Pa = 100.0  # atmospheric pressure in kPa
    gamma_w = 9.81  # unit weight of water (kN/m³)

    # Total and effective vertical stresses
    sigma_v = unit_weight * depth  # kPa
    if depth <= dw:
        u = 0.0
    else:
        water_depth = depth - dw
        u = gamma_w * water_depth
    sigma_v_prime = sigma_v - u
    if sigma_v_prime <= 0:
        raise ZeroDivisionError("Effective vertical stress must be positive.")

    # Stress reduction coefficient rd (Liao & Whitman 1986)
    z = depth
    if z <= 20:
        alpha = -1.012 - 1.126 * math.sin(z / 11.73 + 5.133)
        beta = 0.106 + 0.118 * math.sin(z / 11.28 + 5.142)
        rd = math.exp(alpha + beta * Mw)
    else:
        # For depths >20 m, use the extrapolation or limit to 20 m? The problem states top 20 m.
        # We'll raise an error or cap depth at 20.
        raise ValueError("Depth exceeds 20 m; this calculator only supports depths up to 20 m.")

    # Cyclic Stress Ratio
    CSR = 0.65 * (amax) * (sigma_v / sigma_v_prime) * rd

    # Overburden correction factor CN
    CN = math.sqrt(Pa / sigma_v_prime)
    if CN > 1.7:
        CN = 1.7

    # Corrected blow count N1,60 (energy correction assumed to be already accounted for)
    N1_60 = N * CN

    # Fines content adjustment
    if FC < 35:
        delta_N = math.exp(1.63 + 9.7 / FC - 0.01 * (FC ** 2))
    else:
        delta_N = 0.0
    N1_60cs = N1_60 + delta_N

    # Cyclic Resistance Ratio (Idriss & Boulanger 2008)
    term1 = N1_60cs / 14.1
    term2 = (N1_60cs / 126.0) ** 2
    term3 = (N1_60cs / 23.6) ** 3
    term4 = (N1_60cs / 25.4) ** 4
    CRR = math.exp(term1 + term2 - term3 + term4 - 2.8)

    # Factor of Safety
    fs = CRR / CSR

    # Liquefaction Potential Index (Iwasaki et al. 1978) – for a single 1 m thick layer
    w = 10 - 0.5 * depth
    if w < 0:
        w = 0  # weight cannot be negative; depth>20 would give negative but depth limited to 20.
    if fs <= 1:
        lpi = (1 - fs) * w * 1.0  # assuming 1 m layer thickness
    else:
        lpi = 0.0

    # Severity classification
    if lpi == 0:
        severity = "None"
    elif lpi <= 5:
        severity = "Low"
    elif lpi <= 15:
        severity = "Moderate"
    elif lpi <= 85:
        severity = "High"
    else:
        severity = "Very High"

    return fs, lpi, severity
