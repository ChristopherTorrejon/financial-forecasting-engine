from controllers import *
from data_builder import (
    build_general_dataset,
    build_detailed_dataset
)

from forecasting import (
    build_general_model,
    generate_detailed_forecast
)

from financials import (
    compute_annual_asset_sales,
    build_final_financial_statement
)

from cashflow import build_annual_cash_flow

# ======================
# Main Execution Pipeline
# ======================

if __name__ == "__main__":

    # -----------------------------
    # Date Ranges
    # -----------------------------
    historical_dates = np.arange(
        '2013-01',
        '2026-01',
        dtype='datetime64'
    )

    forecast_dates = np.arange(
        '2025-01',
        '2031-01',
        dtype='datetime64'
    )

    # -----------------------------
    # Build General Dataset
    # -----------------------------
    general_df = pd.DataFrame({'Fecha': historical_dates})

    for i in range(len(categories)):
        build_general_dataset(
            file_paths,
            categories[i],
            general_df
        )

    # -----------------------------
    # Build Detailed Dataset
    # -----------------------------
    detailed_df = build_detailed_dataset(
        file_paths,
        general_df
    )

    # -----------------------------
    # General Model Forecast
    # -----------------------------
    general_model, general_forecast = build_general_model(
        general_df,
        file_paths,
        FIGURES_DIR
    )

    # -----------------------------
    # Detailed Multi-Series Forecast
    # -----------------------------
    detailed_forecast = generate_detailed_forecast(
        detailed_df,
        models,
        FIGURES_DIR
    )

    # -----------------------------
    # Annual Asset Sales
    # -----------------------------
    asset_sales_forecast = compute_annual_asset_sales(
        detailed_forecast,
        general_df,
        forecast_dates
    )

    # -----------------------------
    # Final Financial Statement
    # -----------------------------
    final_statement = build_final_financial_statement(
        general_forecast,
        detailed_forecast,
        forecast_dates,
        asset_sales_forecast,
        final_columns
    )

    # -----------------------------
    # Annual Cash Flow Projection
    # -----------------------------
    annual_cash_flow = build_annual_cash_flow(
        final_statement
    )

    # -----------------------------
    # Export Results
    # -----------------------------
    general_df.to_excel(
        DATA_PROCESSED / "General_Format.xlsx",
    )

    detailed_df.to_excel(
        DATA_PROCESSED / "Details_Format.xlsx",
    )

    final_statement.to_excel(
        RESULTS_DIR / "Financial_Forecast_2025_2030.xlsx",
    )

    annual_cash_flow.to_excel(
        RESULTS_DIR / "Annual_Cash_Flow_2025_2030.xlsx",
    )