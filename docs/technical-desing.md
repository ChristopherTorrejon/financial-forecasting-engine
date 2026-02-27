# Technical Design Document
## Financial Forecasting Engine

---

# 1. System Overview

The Financial Forecasting Engine is a modular system designed to:

- Automate the construction of econometric models  
- Select the best-performing methodology per time series  
- Generate monthly financial projections (2025–2030)  
- Reconstruct consolidated financial statements  
- Produce annual cash flow projections  
- Integrate seamlessly with Power BI for executive-level visualization  

The system is structured into independent modules with clearly defined responsibilities.

---

# 2. Modular Architecture

The project is organized into the following core modules:

 - controllers.py
- data_builder.py  
- forecasting.py  
- financials.py  
- cashflow.py  
- main.py


Each file serves a specific function within the overall forecasting pipeline.

---

# 3. Technical Module Description

---

## 3.1 controllers.py

Centralizes the global configuration of the system.

Defines:

- File paths (`file_paths`)
- Financial categories
- Lists of income and expense items to be modeled
- Excluded items (`excluded_projects`)
- Final financial statement column structure
- Structural project parameters

This module acts as the system’s configuration and hyperparameter control layer.

---

## 3.2 data_builder.py

Responsible for the ETL process and data structuring required for modeling.

### Function: build_general_dataset(...)

- Removes unnecessary rows and columns.
- Groups relevant income and expense items.
- Aggregates non-relevant items into:
  - "Other Income"
  - "Other Expenses"
- Creates "Other Projects" category excluding predefined items.
- Transforms the dataset into the required format for `pmdarima`.

### Function: build_detailed_dataset(...)

- Takes the processed general dataset.
- Extracts each individual financial item.
- Generates structure compatible with `statsforecast`.

This module ensures structural compatibility with the forecasting libraries.

---

## 3.3 forecasting.py

Responsible for econometric model construction and selection.

Two modeling levels are implemented:

---

### 3.3.1 General Model

Function: build_general_model(...)

- Uses `pm.auto_arima`.
- Automatic selection based on AIC/BIC.
- Fits optimal ARIMA/SARIMA model.
- Generates 72-month forecast (2025–2030).

Function: generate_general_forecast(...)

- Produces forecast with 95% confidence intervals.
- Generates visualization comparing:
  - Historical data
  - Forecasted values
  - Confidence intervals

---

### 3.3.2 Item-Level Models (18 Models)

Function: generate_detailed_forecast(...)

- Performs time-series cross-validation.
- Evaluates multiple methodologies:
  - Holt-Winters
  - AutoCES
  - AutoARIMA
  - AutoTheta
  - SeasonalNaive
- Uses MSE as evaluation metric.
- Automatically selects best-performing model per item.
- Generates individual forecasts.
- Produces comparative historical vs forecast visualizations.

Auxiliary functions:

- evaluate_cv()
- get_best_model_forecast()

This module implements performance-driven automated model selection.

---

## 3.4 financials.py

Responsible for reconstructing the consolidated financial statement.

Function: build_final_financial_statement(...)

- Integrates:
  - General forecast
  - Detailed forecasts
- Rebuilds the original financial statement structure.
- Incorporates specific business logic for:
  - "Asset Sales"
  - "Financial Investment"

Function: compute_annual_asset_sales(...)

- Computes asset sales as accumulated annual financial investment.
- Registers asset sales in January of each year.

This module transforms econometric outputs into financially coherent structures.

---

## 3.5 cashflow.py

Responsible for constructing the annual cash flow statement.

Function: build_annual_cash_flow(...)

Process:

1. Consolidates income and expenses excluding special items.
2. Computes Initial Cash Balance using:
   - Asset Sales
   - Existing Initial Cash
3. Applies financial formula:

Final Cash Balance = Initial Cash + Income − Expenses

Auxiliary function:
- compute_initial_cash_balance(...)

Generates projected annual cash flow for 2025–2030.

---

## 3.6 main.py

Orchestrates the full pipeline:

1. Executes ETL
2. Builds models
3. Generates general and detailed forecasts
4. Reconstructs financial statements
5. Builds annual cash flow
6. Exports results to Excel

Acts as the system entry point.

---

# 4. Model Evaluation Framework

The system implements:

- Automatic model selection via AIC/BIC (general model)
- Cross-validation using MSE (detailed models)
- 95% confidence intervals
- Visual validation of model fit

---

# 5. Business Intelligence Integration

Generated outputs feed an interactive Power BI dashboard including:

- Revenue projections
- Expense projections
- Item-level analysis
- General vs detailed model comparison
- Projected cash flow

The visualization layer remains independent from the forecasting engine.

---

# 6. Scalability Design

The system allows:

- Addition of new financial items
- Temporal frequency adjustments
- Integration of new modeling methodologies
- Full pipeline automation
- Migration to scheduled batch execution

---
