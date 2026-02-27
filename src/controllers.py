import warnings
warnings.filterwarnings('ignore')

from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import pmdarima as pm
from statsforecast import StatsForecast

from utilsforecast.losses import mse
from statsforecast.models import (
    HoltWinters,
    AutoCES,
    AutoARIMA,
    AutoTheta,
    SeasonalNaive
)

CURRENT_DIR = Path().resolve()

BASE_DIR = CURRENT_DIR.parents[0]

DATA_PROCESSED = BASE_DIR / "data" / "processed"

DATA_DIR = BASE_DIR / "data" / "raw"

FIGURES_DIR = BASE_DIR / "outputs" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

RESULTS_DIR = BASE_DIR / "outputs" / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

models = [
    HoltWinters(),
    AutoCES(season_length = 12),
    AutoARIMA(season_length = 12),
    AutoTheta(season_length = 12),
    SeasonalNaive(season_length = 12)
]

file_paths = sorted(DATA_DIR.glob("Presupuesto*.xlsx"))

categories = ['Ingresos (+)', 'Egresos (-)']

income_details = [
    '019 - Servicios Mecánicos',
    '020 - Servicios Eléctricos',
    '021 - Servicios Instrumentación',
    '022 - Transferencias Estado',
    '024 - Ingresos Financieros',
    '025 - Intereses',
    '030 - Saldo Inicial de Caja',
]

expense_details = [
    '101 - Sueldos Personal',
    '102 - Bonos Personal',
    '103 - Seguridad Social',
    '107 - Servicios Externos',
    '110 - Seguros',
    '117 - Servicios TI',
    '129 - Inversión Financiera',
    '130 - Saldo Final de Caja'
]

excluded_projects = [
    '120 - Marketing',
    '121 - Logística',
    '123 - Viáticos',
    '126 - Compras Activos'
]

final_columns = [
    'Servicios Mecánicos',
    'Servicios Eléctricos',
    'Servicios Instrumentación',
    'Transferencias Estado',
    'Ingresos Financieros',
    'Intereses',
    'Saldo Inicial de Caja',
    'Otros Ingresos',
    'Sueldos Personal',
    'Bonos Personal',
    'Seguridad Social',
    'Servicios Externos',
    'Seguros',
    'Servicios TI',
    'Otros Proyectos',
    'Inversión Financiera',
    'Saldo Final de Caja',
    'Otros Egresos'
]

income_detail_names = [x[6:] for x in income_details]

expense_detail_names = [x[6:] for x in expense_details]