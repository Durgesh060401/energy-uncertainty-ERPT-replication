# Global Energy Market Uncertainty and Exchange Rate Pass-Through to Food Inflation

## Replication Study

This repository contains an academic replication of **Balcilar and Usman (2026), "Global Energy Market Uncertainty and Exchange Rate Pass-Through to Food Inflation," published in Energy Research Letters, Vol. 7, Issue 1.**

The study investigates whether exchange rate pass-through (ERPT) to food inflation changes depending on the level of global energy market uncertainty.

This replication was conducted as part of an academic course project.

---

## Research Question

The central research question is:

> Does exchange rate pass-through to food inflation change with the level of global energy market uncertainty?

More specifically, the study examines:

1. Whether ERPT is nonlinear.
2. Whether a threshold level of global energy market uncertainty exists.
3. Whether exchange rate pass-through differs between low- and high-uncertainty regimes.

---

## Original Study

**Authors:** Mehmet Balcilar and Ojonugwa Usman  
**Journal:** Energy Research Letters  
**Volume:** 7  
**Issue:** 1  
**Year:** 2026  
**DOI:** 10.46557/001c.125871

The original study considers a panel of **39 developed and developing countries** covering the period **2010Q1–2022Q2**.

---

## Replication Sample

Due to limited availability of country-level Food CPI data, the replication uses a reduced sample of:

- **15 countries**
- **Quarterly data**
- **2010Q1–2022Q2**
- **735 observations**

This difference in sample coverage is an important source of deviation between the original study and the replication results.

---

## Data and Variables

The empirical analysis uses the following variables:

| Variable | Measure | Source |
|---|---|---|
| Food Inflation | Food CPI Index | World Bank |
| Exchange Rate | Nominal Effective Exchange Rate (NEER) | IMF IFS |
| Energy Uncertainty | Global Energy-Related Uncertainty Index | EPU / Dang et al. (2023) |
| Output | GDP per capita, constant 2015 USD | World Bank WDI |
| Foreign Prices | U.S. Producer Price Index | World Bank |

---

## Methodology

The replication follows the nonlinear panel threshold methodology used by Balcilar and Usman (2026), based on the framework developed by Hansen (1999, 2000).

The empirical procedure involves:

1. Testing for threshold effects using a bootstrap likelihood-ratio test.
2. Searching for the optimal energy-uncertainty threshold.
3. Dividing observations into low- and high-uncertainty regimes.
4. Estimating regime-specific exchange rate pass-through coefficients.

First differences are used to address non-stationarity, while the Global Energy-Related Uncertainty Index serves as the threshold variable.

---

## Main Replication Results

The replication produces an estimated energy-uncertainty threshold of:

**γ = 0.3594 (35.94%)**

compared with:

**γ = 0.3851 (38.51%)**

in the original study.

### Exchange Rate Pass-Through

| Parameter | Original Paper | Replication |
|---|---:|---:|
| Threshold (γ) | 0.3851 | 0.3594 |
| Low-Regime ERPT | -0.0088 | +0.1024 |
| High-Regime ERPT | -0.2021 | approximately -0.29 |
| Foreign Prices | +0.3279 | +0.2320 |
| GDP / Output | -0.1428 | -0.0173 |

The low-regime exchange rate coefficient remains statistically insignificant in the replication.

In contrast, the high-regime coefficient is negative and statistically significant, broadly supporting the central finding of the original study.

---

## Key Finding

The replication provides evidence consistent with the central hypothesis of the original paper:

> Exchange rate pass-through to food inflation becomes substantially stronger when global energy market uncertainty is high.

The estimated threshold is also relatively close to that reported in the original study despite the smaller country sample.

---

## Why Do the Results Differ?

The most important limitation of the replication is data availability.

Food CPI data were unavailable for 24 of the 39 countries considered in the original study. Consequently, the replication contains only 15 countries.

The smaller sample can affect:

- statistical power,
- coefficient precision,
- threshold estimates,
- bootstrap inference, and
- the magnitude of estimated exchange rate pass-through.

The composition of the 15-country sample may also contribute to the stronger high-uncertainty ERPT coefficient observed in the replication.

---

## Economic Interpretation

During periods of relatively low energy uncertainty, firms may absorb exchange-rate fluctuations through their margins rather than immediately changing consumer prices.

When energy-market uncertainty becomes sufficiently high, cost uncertainty increases and firms may pass exchange-rate movements into prices more rapidly.

Food prices therefore become more responsive to exchange-rate movements during high-uncertainty periods.

---

## Policy Implications

The findings suggest that policymakers should account for the state of global energy markets when assessing inflationary risks from exchange-rate movements.

Exchange-rate movements may have relatively limited effects on food inflation during normal periods but become considerably more important when global energy-market uncertainty is elevated.

---

## Repository Structure

```text
energy-uncertainty-erpt-replication/
│
├── README.md
├── presentation/
├── data/
│   ├── raw/
│   └── processed/
├── code/
├── results/
│   ├── tables/
│   └── figures/
├── requirements.txt
└── LICENSE

## Reference

Balcilar, M., & Usman, O. (2026). Global Energy Market Uncertainty and Exchange Rate Pass-Through to Food Inflation. *Energy Research Letters, 7*(1).

DOI: 10.46557/001c.125871

---

## Disclaimer

This repository contains an independent academic replication conducted for educational purposes. The original research design and intellectual contributions belong to the authors of the original study.
