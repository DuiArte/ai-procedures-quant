# Procedure · Backtest

**Goal:** run a historical simulation of a strategy and produce a defensible report.

**Inputs:** `<price_data>`, `<strategy_config>` (placeholders).

**Preconditions / gates:**
- [ ] data window covers at least one stress episode (e.g. 2008, 2020)
- [ ] costs and slippage modeled, not assumed zero

## Steps

1. Load `<price_data>` for the `<universe>`.
2. Run the simulation with `<risk_per_trade>`, `<timeframe>` — *values are private;
   keep placeholders here.*
3. Validate out-of-sample on `<oos_window>`; compute deflated Sharpe + probability of
   backtest overfitting.
4. Render the report as ratios (no notional).

## Outputs

- backtest summary → `<reports/...>` (ratios + stress verdicts only)

## Failure handling

| Failure | Detection | Action |
|---|---|---|
| overfit | high PBO / deflated Sharpe ≪ raw | reject; do not publish |
| look-ahead | implausibly smooth curve | re-check data alignment |

> Terse one-liner for this procedure: `BT r:<x>% tf:<x> wf pcv dsr pbo >md`
