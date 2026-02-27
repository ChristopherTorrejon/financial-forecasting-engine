from controllers import *

def compute_annual_asset_sales(detailed_forecast, general_df, final_dates):
    financial_investment_forecast = detailed_forecast[detailed_forecast.unique_id == 'Inversión Financiera']
    years = pd.unique(financial_investment_forecast.ds.dt.year)

    total_months = (len(years) - 1) * 12
    asset_sales = [0] * total_months

    investment_2024 = general_df[['Fecha', 'Inversión Financiera']]
    investment_2024 = investment_2024[investment_2024['Fecha'].dt.year == 2024]
    investment_2024 = investment_2024['Inversión Financiera'].sum()

    asset_sales[0] = investment_2024

    for i in range(len(years) - 1):
        lower_bound = i * 12
        upper_bound = i * 12 + 12

        annual_investment = financial_investment_forecast.iloc[lower_bound : upper_bound].best_model.sum()

        if upper_bound < total_months:
            asset_sales[upper_bound] = annual_investment

    asset_sales_df = pd.DataFrame({'Fecha': final_dates})
    asset_sales_df = asset_sales_df.set_index('Fecha')
    asset_sales_df['Ventas de Activos'] = asset_sales

    return asset_sales_df

def build_final_financial_statement(general_forecast, detailed_forecast, final_dates, asset_sales_forecast, final_columns):
    df = detailed_forecast[['unique_id', 'ds', 'best_model']]

    temp_df = pd.DataFrame({'Fecha': final_dates})
    temp_df = temp_df.set_index('Fecha')

    final_df = pd.DataFrame({'Fecha': final_dates})
    final_df = final_df.set_index('Fecha')

    for i in range(len(final_columns)):
        series_data = df[df.unique_id == final_columns[i]]

        temp_df[final_columns[i]] = series_data['best_model'].to_list()

    final_df['Ingresos'] = (temp_df[final_columns[:8]].sum(axis = 1) + asset_sales_forecast['Ventas de Activos']).to_list()
    final_df['Ventas de Activos'] = asset_sales_forecast['Ventas de Activos'].to_list()
    final_df = pd.concat([final_df, temp_df[final_columns[:8]]], axis = 1)

    final_df['Egresos'] = temp_df[final_columns[8:]].sum(axis = 1).to_list()
    final_df = pd.concat([final_df, temp_df[final_columns[8:]]], axis = 1)

    final_df['General Model'] = general_forecast.to_list()

    return final_df.T