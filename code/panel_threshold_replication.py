from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm


# ==========================
# REPRODUCIBILITY
# ==========================

# Ensures that bootstrap resampling gives reproducible results
np.random.seed(42)


# ==========================
# LOAD DATA
# ==========================

# Locate the root directory of the GitHub repository
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Dataset stored inside the data folder
file_path = PROJECT_ROOT / "data" / "replication_data.csv"

# Load dataset
df = pd.read_csv(file_path)


# Rename columns to simple names
df = df.rename(columns={
    'Δlog(CPI_all_items)': 'y',
    'Δlog(NEER)': 'x',
    'Δlog(EUI)': 'z',
    'Δlog(Forign prices)': 'fp',
    'Δlog(output/GDP)': 'gdp'
})

# Remove observations containing missing values
df = df.dropna().copy()


# ==========================
# THRESHOLD ESTIMATION
# ==========================

def estimate_threshold_model(
    data,
    y_var,
    x_var,
    threshold_var,
    control_vars=None
):

    y = data[y_var]
    Z = data[threshold_var]

    # Candidate threshold values
    possible_gammas = np.percentile(
        Z,
        np.linspace(50, 85, 100)
    )

    best_gamma = None
    min_sse = np.inf
    best_model = None

    for gamma in possible_gammas:

        regime1 = (Z <= gamma).astype(int)
        regime2 = (Z > gamma).astype(int)

        data['regime1_x'] = data[x_var] * regime1
        data['regime2_x'] = data[x_var] * regime2

        X_vars = ['regime1_x', 'regime2_x']

        if control_vars is not None:
            X_vars += control_vars

        X = sm.add_constant(data[X_vars])

        model = sm.OLS(y, X).fit()

        if model.ssr < min_sse:
            min_sse = model.ssr
            best_gamma = gamma
            best_model = model

    return best_gamma, best_model


# ==========================
# BOOTSTRAP THRESHOLD TEST
# ==========================

def bootstrap_threshold_test(
    data,
    y_var,
    x_var,
    threshold_var,
    control_vars=None,
    B=1000
):

    y = data[y_var]

    # --------------------------
    # Linear model (no threshold)
    # --------------------------

    X_linear_vars = [x_var]

    if control_vars is not None:
        X_linear_vars += control_vars

    X_linear = sm.add_constant(
        data[X_linear_vars]
    )

    linear_model = sm.OLS(
        y,
        X_linear
    ).fit()

    SSE_linear = linear_model.ssr


    # --------------------------
    # Threshold model
    # --------------------------

    gamma_hat, threshold_model = estimate_threshold_model(
        data,
        y_var,
        x_var,
        threshold_var,
        control_vars
    )

    SSE_threshold = threshold_model.ssr

    sigma2 = SSE_threshold / len(y)

    F_stat = (
        SSE_linear - SSE_threshold
    ) / sigma2


    # --------------------------
    # Bootstrap
    # --------------------------

    F_bootstrap = []

    residuals = threshold_model.resid
    y_fitted = threshold_model.fittedvalues

    for i in range(B):

        resampled_resid = np.random.choice(
            residuals,
            size=len(residuals),
            replace=True
        )

        y_boot = y_fitted + resampled_resid

        data_boot = data.copy()

        data_boot[y_var] = y_boot

        _, model_boot = estimate_threshold_model(
            data_boot,
            y_var,
            x_var,
            threshold_var,
            control_vars
        )

        SSE_boot = model_boot.ssr

        F_boot = (
            SSE_linear - SSE_boot
        ) / sigma2

        F_bootstrap.append(F_boot)


    p_value = np.mean(
        np.array(F_bootstrap) > F_stat
    )

    return F_stat, p_value


# ==========================
# CONFIDENCE INTERVAL
# FOR THRESHOLD GAMMA
# ==========================

def threshold_confidence_interval(
    data,
    y_var,
    x_var,
    threshold_var,
    control_vars=None
):

    Z = data[threshold_var]

    gammas = np.percentile(
        Z,
        np.linspace(50, 85, 100)
    )

    _, best_model = estimate_threshold_model(
        data,
        y_var,
        x_var,
        threshold_var,
        control_vars
    )

    SSE_min = best_model.ssr

    lr_stats = []

    for gamma in gammas:

        regime1 = (Z <= gamma).astype(int)
        regime2 = (Z > gamma).astype(int)

        data['regime1_x'] = (
            data[x_var] * regime1
        )

        data['regime2_x'] = (
            data[x_var] * regime2
        )

        X_vars = [
            'regime1_x',
            'regime2_x'
        ]

        if control_vars is not None:
            X_vars += control_vars

        X = sm.add_constant(
            data[X_vars]
        )

        model = sm.OLS(
            data[y_var],
            X
        ).fit()

        lr = model.ssr - SSE_min

        lr_stats.append(lr)


    critical_value = np.percentile(
        lr_stats,
        95
    )

    ci = [
        g
        for g, lr in zip(gammas, lr_stats)
        if lr <= critical_value
    ]

    return min(ci), max(ci)


# ==========================
# RUN ESTIMATION
# ==========================

gamma_hat, results = estimate_threshold_model(
    df,
    'y',
    'x',
    'z',
    ['fp', 'gdp']
)


# ==========================
# BOOTSTRAP TEST
# ==========================

F_stat, p_value = bootstrap_threshold_test(
    df,
    'y',
    'x',
    'z',
    ['fp', 'gdp'],
    B=1000
)


# ==========================
# THRESHOLD CONFIDENCE
# INTERVAL
# ==========================

ci_low, ci_high = threshold_confidence_interval(
    df,
    'y',
    'x',
    'z',
    ['fp', 'gdp']
)


# ==========================
# PRINT FINAL RESULTS
# ==========================

print("\n=========== FINAL RESULTS ===========")

print(
    "Estimated Threshold (Gamma):",
    gamma_hat
)

print(
    "95% Confidence Interval:",
    ci_low,
    "to",
    ci_high
)

print(
    "\nAlpha (Constant):",
    results.params['const']
)

print(
    "Phi 1 (Low Regime):",
    results.params['regime1_x']
)

print(
    "Phi 2 (High Regime):",
    results.params['regime2_x']
)

print(
    "Psi (Foreign Prices):",
    results.params['fp']
)

print(
    "Psi (GDP):",
    results.params['gdp']
)

print(
    "\nThreshold Effect Test "
    "(Hansen Bootstrap)"
)

print(
    "F-stat:",
    F_stat
)

print(
    "p-value:",
    p_value
)

print("\n=========== OLS SUMMARY ===========")

print(
    results.summary()
)
