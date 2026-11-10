"""Pure operator excerpt from Git blob c04751cbe5f92952e33328f6c04fcae6392e05e5.
Original source preserved under recovery/model_source_audit; no deployment map.
"""
import math
import numpy as np
EPS = 1e-9

def shannon(x, bins=None) -> float:
    x = np.asarray(x, float)
    if x.size < 2 or np.allclose(x, x[0]):
        return 0.0
    if bins is None:
        bins = max(3, int(round(math.sqrt(x.size))))
    h, _ = np.histogram(x, bins=bins)
    p = h[h > 0] / h.sum()
    return float(-(p * np.log(p)).sum())


def mutual_info(a, b, bins=None) -> float:
    a = np.asarray(a, float); b = np.asarray(b, float)
    if a.size < 2:
        return 0.0
    if bins is None:
        bins = max(3, int(round(math.sqrt(a.size))))
    Ha, Hb = shannon(a, bins), shannon(b, bins)
    hab, _, _ = np.histogram2d(a, b, bins=bins)
    p = hab[hab > 0] / hab.sum()
    Hab = float(-(p * np.log(p)).sum())
    return max(0.0, Ha + Hb - Hab)


def signed_flow_features(buy_vol, sell_vol) -> dict | None:
    """Signed information-dipole flow features from one order-flow window.

    buy_vol/sell_vol: equal-length per-bar taker buy/sell volume over the (pre-entry) window,
    time-ordered. Returns the FEATURES dict, or None if the window is too short / empty.
    """
    A = np.asarray(buy_vol, float); S = np.asarray(sell_vol, float)
    n = min(A.size, S.size)
    if n < 6:
        return None
    A, S = A[:n], S[:n]
    sB, sS = A.sum(), S.sum()
    if sB + sS <= 0:
        return None

    imb_level = (sB - sS) / (sB + sS)                 # static order-flow dipole (signed)
    sgn = 1.0 if imb_level >= 0 else -1.0             # option (a): direction from imbalance

    Ha, Hb = shannon(A), shannon(S)
    ent_dipole = (Ha - Hb) / (Ha + Hb + EPS)          # entropy-asymmetry dipole (signed)
    mi = mutual_info(A, S)
    C_signed = sgn * (0.5 * (Ha + Hb)) / (mi + EPS)    # signed C = H_self/H_cross

    mid = n // 2                                       # differential dMI/dt: early vs late half
    mi_e = mutual_info(A[:mid], S[:mid]); mi_l = mutual_info(A[mid:], S[mid:])
    mi_flow = sgn * (mi_l - mi_e)                      # PRIMARY: imbalance-signed MI flow
    def _imb(b, s):
        t = b.sum() + s.sum()
        return (b.sum() - s.sum()) / t if t > 0 else 0.0
    imb_flow = _imb(A[mid:], S[mid:]) - _imb(A[:mid], S[:mid])   # signed imbalance flow

    return {"imb_level": imb_level, "ent_dipole": ent_dipole, "C_signed": C_signed,
            "mi_flow": mi_flow, "imb_flow": imb_flow}


