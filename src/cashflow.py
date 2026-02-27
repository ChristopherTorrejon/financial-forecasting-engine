from controllers import *

def compute_initial_cash_balance(final_statement, annual_dates):
    data = final_statement.loc[['Ventas de Activos', 'Saldo Inicial de Caja']]

    initial_cash = []

    for i in range(len(annual_dates)):
        initial_cash.append(data[pd.Timestamp(annual_dates[i])].sum())

    return initial_cash

def build_annual_cash_flow(final_df):
    df = final_df.copy()

    annual_dates = np.arange('2025-01-01', '2031-01-01', dtype = 'datetime64[Y]')

    data = df.drop(['Ventas de Activos', 'Saldo Inicial de Caja', 'Inversión Financiera', 'Saldo Final de Caja'])

    date_labels = pd.to_datetime(data.columns, errors = 'coerce')
    years = date_labels.year.unique()

    annual_income = []
    annual_expenses = []

    for i in range(len(years)):
        lower_bound = i * 12
        upper_bound = i * 12 + 12

        yearly_segment = data.iloc[: , lower_bound : upper_bound]

        annual_income.append(yearly_segment.loc['Servicios Mecánicos' : 'Otros Ingresos'].sum(axis = 1).sum())
        annual_expenses.append(yearly_segment.loc['Sueldos Personal' : 'Otros Egresos'].sum(axis = 1).sum())

    initial_cash = compute_initial_cash_balance(df, annual_dates)

    annual_cash_flow = pd.DataFrame({
        'Saldo Inicial de Caja': initial_cash,
        'Ingresos': annual_income,
        'Egresos': annual_expenses}
    )

    annual_cash_flow['Saldo Final de Caja'] = (
            annual_cash_flow['Saldo Inicial de Caja']
            + annual_cash_flow['Ingresos']
            - annual_cash_flow['Egresos']
    )

    annual_cash_flow = annual_cash_flow.set_index(annual_dates)

    return annual_cash_flow.T