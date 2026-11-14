# tests/test_transformacion.py
import pandas as pd
from pathlib import Path
from src.Transformacion.transformaciones import SensoresDataTransformer

RUTA_LIMPIA = Path("Datacrude/02IntermediateData/Sensores_limpio.csv")
RUTA_TRANSFORMADA = Path("Datacrude/03DatafinalProcessed/Sensores_transformado.csv")

def test_transformacion_dimensions():
    """La matriz transformada debe tener 868 filas y 18 columnas."""
    t = SensoresDataTransformer(str(RUTA_LIMPIA))
    df = t.ejecutar_transformacion()
    assert df.shape == (868, 18)

def test_one_hot_columns_exist():
    """Debe existir al menos una columna dummy de Nivel_Pasos y Nivel_Sedentarismo."""
    t = SensoresDataTransformer(str(RUTA_LIMPIA))
    df = t.ejecutar_transformacion()
    assert any("Nivel_Pasos" in c for c in df.columns)
    assert any("Nivel_Sedentarismo" in c for c in df.columns)

def test_dummies_are_binary():
    """Las columnas dummy deben contener solo 0 y 1."""
    t = SensoresDataTransformer(str(RUTA_LIMPIA))
    df = t.ejecutar_transformacion()
    for col in df.columns:
        if col.startswith("Nivel_"):
            assert set(df[col].dropna().unique()).issubset({0, 1})

def test_exported_matrix_matches():
    """El CSV exportado debe tener las mismas dimensiones que el DataFrame."""
    t = SensoresDataTransformer(str(RUTA_LIMPIA))
    df = t.ejecutar_transformacion()
    t.exportar_matriz(str(RUTA_TRANSFORMADA))
    df_csv = pd.read_csv(RUTA_TRANSFORMADA)
    assert df_csv.shape == df.shape
