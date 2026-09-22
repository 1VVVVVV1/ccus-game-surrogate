# Source-backed scalar calibration: current audit summary

This is a representative multi-source investment-game calibration, not a reconstructed Qilu–Shengli project financial statement. Values remain in their stated source price bases; no inflation escalation has been invented.

| Model input | Value | Identity / interpretation |
|---|---:|---|
| Capture capacity |0.50 Mt/year|User model design; matches NETL Taizhou scale|
| Capture CAPEX |385 million CNY|NETL Tao2023 page9 project-reported investment|
| Capture OPEX |240 CNY/t|Carbon Neutrality2022 section3.2.4 expected operating-cost benchmark; MODEL_ASSUMPTION|
| Net-abatement proxy |0.70|Protocol10, approximately30% lifecycle emission offset; not ETS statutory crediting|
| Transport tariff |125 CNY/t|User MODEL_ASSUMPTION, internal transfer price|
| Transport resource cost |28.1656 CNY/t|0.2584×109; levelized equipment+maintenance+electricity benchmark, not pure observed OPEX|
| Integrated downstream CAPEX |759.2857142857143 million CNY|User-approved1063×0.50/0.70; PIPELINE_EXCLUDED|
| EOR gross revenue |1101.85965 CNY/t fresh CO2|90USD/bbl×7.1bbl/t×6.8974CNY/USD÷4; MODEL_ASSUMPTION|
| EOR operating cost |103.461 CNY/t fresh CO2|Guo15USD/t×6.8974; MODEL_ASSUMPTION|
| EOR-specific fixed cost |0|Explicit user simplification; Guo itself retains fixed F before optimizing|
| Dedicated storage injection proxy |55 CNY/t|Protocol13 midpoint50–60; not national full-chain cost|

The transport paper uses a20-year levelization scenario, while the investment game retains the user-fixed30-year horizon. Transferring its unit resource cost is a benchmark mapping, not a claim of identical project financing. No separate T capital charge is added. Storage55 is assigned to model flow expense; the source does not establish a detailed capital/operating split. No separate storage capital or reconstructed maintenance schedule is added.

Oil90USD/bbl is the higher-priority China onshore EOR literature benchmark. Its dollar magnitude is held constant and translated with2020 FX; this is not an inflation-adjusted2015 oil observation. Sinopec reports domestic7.1bbl/t, distinct from refinery7.35. Its2020 realized1902CNY/t segment price and2029CNY/t external-sales price have different scopes and are not substituted for the selected literature assumption. The2020 pandemic slump limits their use as general long-run benchmarks.

Official carbon completeness and source audit passed with1257daily closes over2021-07-16–2026-09-18. P0=95.63,mu=0.16886265073995846,sigma=0.3106155387941257. Source-backed config has been generated. Formal numerical results require the subsequent exact,surrogate,boundary and reproducibility Gates. The user2026-09-22 decision permits static accounting discrepancies<=100CNY (0.0001million CNY); actual errors remain recorded and other thresholds are unchanged.
