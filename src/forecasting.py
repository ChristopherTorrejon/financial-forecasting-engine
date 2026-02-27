from controllers import *

def generate_general_forecast(general_model, test, figures_dir):
    forecast, forecast_ci = general_model.predict(n_periods = 72, return_conf_int = True)
    forecast_ci = pd.DataFrame(forecast_ci)
    forecast_ci = forecast_ci.set_index(forecast.index)

    plt.figure(figsize = (20, 8))
    ax = test.plot(label = 'Observed Data')
    forecast.plot(label = 'General AutoARIMA Model')

    ax.fill_between(
        forecast_ci.index,
        forecast_ci.iloc[:, 0],
        forecast_ci.iloc[:, 1],
        color = 'k',
        alpha = 0.2,
        label = 'Confidence Interval [95%]'
    )

    plt.title('General AutoARIMA Model vs Observed Data (2025)')
    plt.grid(True)
    plt.legend()

    save_path = figures_dir / "general_forecast.png"
    plt.savefig(save_path, dpi = 300, bbox_inches = "tight")
    plt.close()

    forecast.index.name = 'Fecha'
    forecast = forecast.rename('General Model')

    return forecast

def build_general_model(general_df, file_paths, figures_dir):
    split_index = len(file_paths) * 12 - 12

    data = general_df
    data = data.set_index('Fecha')

    train = data['Ingresos'][:split_index]
    test = data['Ingresos'][split_index:]

    model = pm.auto_arima(
        train,
        m = 12,
        seasonal = True,
        trace = False,
        stepwise = True,
        max_p = 3, max_q = 3
    )

    print(model.summary())

    forecast = generate_general_forecast(model, test, figures_dir)

    return model, forecast

#################################################################################################

def evaluate_cv(df, metric):
    models = df.columns.drop(['unique_id', 'ds', 'y', 'cutoff']).tolist()
    evals = metric(df, models = models)
    evals['best_model'] = evals[models].idxmin(axis=1)
    return evals

def get_best_model_forecast(forecasts_df, evaluation_df):
    with_best = forecasts_df.merge(evaluation_df[['unique_id', 'best_model']])
    res = with_best[['unique_id', 'ds']].copy()
    for suffix in ('', '-lo-95', '-hi-95'):
        res[f'best_model{suffix}'] = with_best.apply(lambda row: row[row['best_model'] + suffix], axis = 1)
    return res

def generate_detailed_forecast(detailed_df, models, figures_dir):
    train = detailed_df[detailed_df.ds < '2025-01-01']

    sf = StatsForecast(
        models = models,
        freq = 'ME',
        fallback_model = SeasonalNaive(season_length = 12),
        n_jobs = -1
    )

    forecasts_df = sf.forecast(df = train, h = 72, level = [95])

    cv_df = sf.cross_validation(
        df = train,
        h = 12,
        step_size = 12,
        n_windows = 1
    )

    evaluation_df = evaluate_cv(cv_df, mse)
    detailed_forecast = get_best_model_forecast(forecasts_df, evaluation_df)

    fig = sf.plot(train, detailed_forecast, level = [95])

    save_path = figures_dir / "detailed_forecasts.png"
    fig.savefig(save_path, dpi = 300)
    plt.close(fig)

    return detailed_forecast