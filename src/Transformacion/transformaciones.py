import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.preprocessing import RobustScaler, MinMaxScaler, OneHotEncoder

class SensoresDataTransformer:
    """Clase modular para la transformación, codificación y escalado de datos del proyecto MIMETIC."""

    def __init__(self, ruta_fuente=None):
        from pathlib import Path
        if ruta_fuente is None:
            raiz = Path(__file__).resolve().parent.parent.parent
            self.ruta_fuente = raiz / "Datacrude" / "02IntermediateData" / "Sensores_limpio.csv"
        else:
            self.ruta_fuente = Path(ruta_fuente)

        self.df = None
        self.df_transformed = None
        
        # Definición de grupos de variables según sus propiedades estadísticas
        self.cols_robust = ["TotalSteps", "Calories", "VeryActiveMinutes"]
        self.cols_minmax = ["TotalMinutesAsleep", "TotalTimeInBed", "SedentaryMinutes", "Eficiencia_Sueño"]
        self.cols_categoricas = ["Nivel_Pasos", "Nivel_Sedentarismo"]
        self.cols_passthrough = ["Id", "ActivityDate"]

    def cargar_datos(self):
        """Carga el dataset intermedio limpio."""
        print("=== PASO 1: CARGA DE DATOS INTERMEDIOS ===")
        self.df = pd.read_csv(self.ruta_fuente)
        print(f"Dataset cargado desde: {self.ruta_fuente}")
        print(f"Dimensiones iniciales: {self.df.shape}")
        return self

    def escalar_numéricas(self):
        """Aplica escalado robusto a variables con outliers residuales y MinMaxScaler a rangos acotados."""
        print("\n=== PASO 2: ESCALADO NUMÉRICO SELECTIVO ===")
        self.df_transformed = self.df.copy()

        # 1. RobustScaler para variables con distribución con sesgo/outliers
        cols_robust_presentes = [c for c in self.cols_robust if c in self.df.columns]
        if cols_robust_presentes:
            robust_scaler = RobustScaler()
            self.df_transformed[cols_robust_presentes] = robust_scaler.fit_transform(self.df[cols_robust_presentes])
            print(f"RobustScaler aplicado a: {cols_robust_presentes}")

        # 2. MinMaxScaler para variables de tiempo acotado o eficiencias (0 a 1)
        cols_minmax_presentes = [c for c in self.cols_minmax if c in self.df.columns]
        if cols_minmax_presentes:
            minmax_scaler = MinMaxScaler()
            self.df_transformed[cols_minmax_presentes] = minmax_scaler.fit_transform(self.df[cols_minmax_presentes])
            print(f"MinMaxScaler aplicado a: {cols_minmax_presentes}")

        return self

    def codificar_categoricas(self):
        """Aplica One-Hot Encoding (Dummies) a las variables categóricas ordenadas."""
        print("\n=== PASO 3: CODIFICACIÓN CATEGÓRICA (ONE-HOT ENCODING) ===")
        cols_cat_presentes = [c for c in self.cols_categoricas if c in self.df.columns]

        if cols_cat_presentes:
            # Creamos dummies dejando valores 0 y 1 enteros
            df_dummies = pd.get_dummies(self.df_transformed[cols_cat_presentes], drop_first=True, dtype=int)
            
            # Eliminamos las columnas categóricas originales e integramos las codificadas
            self.df_transformed = self.df_transformed.drop(columns=cols_cat_presentes)
            self.df_transformed = pd.concat([self.df_transformed, df_dummies], axis=1)
            print(f"Variables codificadas mediante One-Hot Encoding: {cols_cat_presentes}")
            print(f"Nuevas columnas generadas: {list(df_dummies.columns)}")

        return self

    def exportar_matriz(self, ruta_destino=None):
        """Exporta la matriz procesada y vectorizada final."""
        print("\n=== PASO 4: EXPORTACIÓN DE LA MATRIZ PROCESADA ===")
        if ruta_destino is None:
            raiz = Path(__file__).resolve().parent.parent.parent
            ruta_destino = raiz / "Datacrude" / "03DatafinalProcessed" / "Sensores_transformado.csv"
        else:
            ruta_destino = Path(ruta_destino)

        # Crear directorio si no existe
        ruta_destino.parent.mkdir(parents=True, exist_ok=True)
        
        self.df_transformed.to_csv(ruta_destino, index=False)
        print(f"Matriz procesada exportada exitosamente a: {ruta_destino}")
        print(f"Dimensiones finales para modelado: {self.df_transformed.shape}")
        return self

    def ejecutar_transformacion(self):
        """Ejecuta el pipeline completo de transformación de datos."""
        self.cargar_datos()
        self.escalar_numéricas()
        self.codificar_categoricas()
        return self.df_transformed