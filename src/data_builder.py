from controllers import *

def build_general_dataset(file_paths, category_name, master_df):
    for i in range(len(file_paths)):

        data = pd.read_excel(file_paths[i])
        data = data.set_index('Unnamed: 0')
        data.index = data.index.str.strip()
        data = data.loc[: , 'Enero' : 'Diciembre']
        data = data.drop('Detalle').T

        lower_bound = i * 12
        upper_bound = i * 12 + 11

        if category_name == 'Ingresos (+)':
            master_df.loc[lower_bound : upper_bound, 'Ingresos'] = data[category_name].tolist()

            for j in range(len(income_details)):
                master_df.loc[lower_bound : upper_bound, income_detail_names[j]] = data[income_details[j]].tolist()

            other_income = data.loc[: , '001 - Ventas Servicios Industriales' : '030 - Saldo Inicial de Caja']
            other_income = other_income.drop(income_details, axis = 1)
            other_income = other_income.drop('029 - Ventas de Activos', axis = 1)

            master_df.loc[lower_bound : upper_bound, 'Otros Ingresos'] = other_income.sum(axis = 1).tolist()

        if category_name == 'Egresos (-)':
            master_df.loc[lower_bound : upper_bound, 'Egresos'] = data[category_name].tolist()

            for j in range(len(expense_details)):
                master_df.loc[lower_bound : upper_bound, expense_detail_names[j]] = data[expense_details[j]].tolist()

            other_projects = data.loc[: , '119 - Consultorías' : '128 - Provisiones']
            other_projects = other_projects.drop(excluded_projects, axis = 1)
            other_expenses = data.loc[: , '101 - Sueldos Personal' : '130 - Saldo Final de Caja']
            other_expenses = other_expenses.drop(expense_details, axis = 1).drop(other_projects.columns.tolist(), axis = 1)

            master_df.loc[lower_bound : upper_bound, 'Otros Proyectos'] = other_projects.sum(axis = 1).tolist()
            master_df.loc[lower_bound : upper_bound, 'Otros Egresos'] = other_expenses.sum(axis = 1).tolist()

def build_detailed_dataset(file_paths, general_df):
    data = general_df.drop(['Ingresos', 'Egresos'], axis = 1)

    series_names = data.drop('Fecha', axis = 1).columns.to_list()
    total_months = len(file_paths) * 12
    total_records = len(series_names) * total_months

    detailed_df = pd.DataFrame({'Numero': np.arange(0, total_records)})
    detailed_df = detailed_df.set_index('Numero')

    for i in range(len(series_names)):
        lim_inf = i * total_months
        lim_sup = i * total_months + total_months - 1

        detailed_df.loc[lim_inf : lim_sup, 'ds'] = data['Fecha'].to_list()
        detailed_df.loc[lim_inf : lim_sup, 'unique_id'] = series_names[i]
        detailed_df.loc[lim_inf : lim_sup, 'y'] = data[series_names[i]].to_list()

    return detailed_df