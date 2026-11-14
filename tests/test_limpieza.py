# tests/test_limpieza.py
import pandas as pd
from pathlib import Path
from src.Limpieza.Sensores_limpios import SensoresDataCleaner

RUTA_CRUDA = Path("Datacrude/01NoProcessData/SENSORES(sucio).xlsx")
RUTA_LIMPIA = Path("Datacrude/02IntermediateData/Sensores_limpio.csv")

def test_pipeline_reduces_rows():
    """El pipeline debe reducir de 940 a 868 filas (elimina dias de 'no uso')."""
    limpiador = SensoresDataCleaner(str(RUTA_CRUDA), factorIqr=1.5)
    df = limpiador.ejecutarPipeline()
    assert df.shape[0] == 868

def test_pipeline_columns():
    """El dataset limpio debe tener 18 columnas (sin fantasma + 3 de sueno)."""
    limpiador = SensoresDataCleaner(str(RUTA_CRUDA), factorIqr=1.5)
    df = limpiador.ejecutarPipeline()
    assert df.shape[1] == 18

def test_no_duplicates():
    """No debe haber duplicados exactos despues de la limpieza."""
    limpiador = SensoresDataCleaner(str(RUTA_CRUDA), factorIqr=1.5)
    df = limpiador.ejecutarPipeline()
    assert df.duplicated().sum() == 0

def test_no_ghost_columns():
    """No deben quedar columnas 'Unnamed'."""
    limpiador = SensoresDataCleaner(str(RUTA_CRUDA), factorIqr=1.5)
    df = limpiador.ejecutarPipeline()
    assert not any("Unnamed" in c for c in df.columns)

def test_activity_date_is_datetime():
    """ActivityDate debe ser datetime."""
    limpiador = SensoresDataCleaner(str(RUTA_CRUDA), factorIqr=1.5)
    df = limpiador.ejecutarPipeline()
    assert pd.api.types.is_datetime64_any_dtype(df["ActivityDate"])

def test_exported_csv_matches():
    """El CSV exportado debe tener las mismas dimensiones que el DataFrame."""
    limpiador = SensoresDataCleaner(str(RUTA_CRUDA), factorIqr=1.5)
    df = limpiador.ejecutarPipeline()
    limpiador.exportarCsv(str(RUTA_LIMPIA))
    df_csv = pd.read_csv(RUTA_LIMPIA)
    assert df_csv.shape == df.shape
