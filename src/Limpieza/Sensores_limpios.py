from pathlib import Path

import pandas as pd
import requests


class SensoresDataCleaner:
    """Pipeline de limpieza de datos del proyecto Sensores colectivos (CRISP-DM)."""

    def __init__(self, fuente, factorIqr=1.5, colsOutlier=None, colsCategoricas=None):
        """Recibe el DataFrame original o la ruta del archivo."""
        self.project_root = Path(__file__).resolve().parents[2]
        if isinstance(fuente, pd.DataFrame):
            self.dfOriginal = fuente.copy()
        else:
            self.dfOriginal = pd.read_excel(self._resolverRuta(fuente))
        self.factorIqr = factorIqr
        self.colsOutlier = colsOutlier if colsOutlier is not None else \
            ["TotalSteps", "Calories", "VeryActiveMinutes"]
        self.colsCategoricas = colsCategoricas if colsCategoricas is not None else \
            ["Nivel_Pasos", "Nivel_Sedentarismo"]
        self.colFecha = "ActivityDate"
        self.dfClean = None

    def _resolverRuta(self, ruta):
        """Resuelve rutas relativas tanto desde la carpeta del proyecto como desde el cwd actual."""
        if isinstance(ruta, Path):
            camino = ruta
        else:
            camino = Path(ruta)

        if camino.is_absolute():
            return camino

        candidatos = [
            Path.cwd() / camino,
            self.project_root / camino,
        ]
        for candidato in candidatos:
            if candidato.exists():
                return candidato

        return candidatos[0]

    def diagnosticar(self):
        print("=== PASO 0: DIAGNÓSTICO INICIAL DE CALIDAD ===")
        print("Dimensiones:", self.dfOriginal.shape)
        print("Nulos explícitos (isna):", self.dfOriginal.isna().sum().sum())
        print("Duplicados exactos:", self.dfOriginal.duplicated().sum())
        colsFantasma = [c for c in self.dfOriginal.columns if "Unnamed" in c]
        print("\nColumnas fantasma (artefactos de Excel):", colsFantasma)
        diasSinUso = ((self.dfOriginal["TotalSteps"] == 0) &
                     (self.dfOriginal["SedentaryMinutes"] == 1440)).sum()
        print(f"\nDías de 'no uso' del tracker (0 pasos y 1440 min): {diasSinUso}")
        return self

    def eliminarColumnasFantasma(self):
        colsFantasma = [c for c in self.dfClean.columns if "Unnamed" in c]
        self.dfClean = self.dfClean.drop(columns=colsFantasma).copy()
        print(f"[PASO 1] Columnas fantasma eliminadas: {colsFantasma}")
        print(f"Nuevas dimensiones: {self.dfClean.shape}")
        return self

    def normalizarFechas(self):
        self.dfClean[self.colFecha] = pd.to_datetime(
            self.dfClean[self.colFecha], errors="coerce")
        fechasInvalidas = self.dfClean[self.colFecha].isna().sum()
        print(f"[PASO 2] '{self.colFecha}' convertida a datetime.")
        print(f"Fechas inválidas (NaT): {fechasInvalidas}")
        return self

    def integrarFuenteSueno(self, rutaSleep=None):
        """PASO INTEGRACIÓN: Carga, depura e integra la Fuente 3 (Sueño)."""
        if rutaSleep is None:
            rutaSleep = self.project_root / "Datacrude" / "01NoProcessData" / "sleepDay_merged.csv"
        else:
            rutaSleep = self._resolverRuta(rutaSleep)

        dfSleep = pd.read_csv(rutaSleep)
        filasIniciales = len(dfSleep)

        dfSleep = dfSleep.drop_duplicates(subset=["Id", "SleepDay"]).copy()
        duplicadosEliminados = filasIniciales - len(dfSleep)

        dfSleep["ActivityDate"] = pd.to_datetime(dfSleep["SleepDay"], format="mixed")

        dfSleep["Eficiencia_Sueño"] = (
            dfSleep["TotalMinutesAsleep"] / dfSleep["TotalTimeInBed"]
        ).round(2).clip(upper=1.0)

        self.dfClean = pd.merge(
            self.dfClean,
            dfSleep[["Id", "ActivityDate", "TotalMinutesAsleep", "TotalTimeInBed", "Eficiencia_Sueño"]],
            on=["Id", "ActivityDate"],
            how="left"
        )
        print(f"[PASO SUEÑO] Duplicados de sueño eliminados: {duplicadosEliminados}")
        print(f"[PASO INTEGRACIÓN] Columnas consolidadas: {self.dfClean.shape[1]}")
        return self

    def filtrarDiasSinUso(self):
        indicesNoUso = self.dfClean[
            (self.dfClean["TotalSteps"] == 0) &
            (self.dfClean["SedentaryMinutes"] == 1440)
        ].index
        self.dfClean = self.dfClean.drop(index=indicesNoUso).reset_index(drop=True)
        print(f"[PASO 3] Registros de 'No Uso' eliminados: {len(indicesNoUso)}")
        print(f"Filas restantes: {len(self.dfClean)}")
        return self

    def tratarOutliersIqr(self, columna):
        """Regla de Tukey: winsoriza una sola columna."""
        q1 = self.dfClean[columna].quantile(0.25)
        q3 = self.dfClean[columna].quantile(0.75)
        iqr = q3 - q1
        limInf = q1 - self.factorIqr * iqr
        limSup = q3 + self.factorIqr * iqr
        limInfReal = max(0, limInf)
        fuera = self.dfClean.loc[
            (self.dfClean[columna] < limInf) | (self.dfClean[columna] > limSup)
        ].shape[0]
        self.dfClean[columna] = self.dfClean[columna].clip(
            lower=limInfReal, upper=limSup)
        print(f"  -> '{columna}': IQR={iqr:.2f} | límites=[{limInfReal:.2f}, {limSup:.2f}] | recortados={fuera}")
        return self

    def aplicarOutliers(self, cols=None):
        colsAplicar = self.colsOutlier if cols is None else cols
        print("[PASO 5] Aplicando regla IQR (winsorización):")
        for col in colsAplicar:
            self.tratarOutliersIqr(col)
        return self

    def limpiarCategorias(self, cols=None):
        colsAplicar = self.colsCategoricas if cols is None else cols
        for col in colsAplicar:
            self.dfClean[col] = self.dfClean[col].str.strip()
            print(f"[PASO 6] '{col}' -> valores únicos: {sorted(self.dfClean[col].unique())}")
        return self

    def validar(self):
        print("=== VALIDACIÓN FINAL (dfClean) ===")
        print(f"Dimensiones: {self.dfClean.shape}")
        print(f"Nulos totales: {self.dfClean.isna().sum().sum()}")
        print(f"Duplicados exactos: {self.dfClean.duplicated().sum()}")
        return self

    def exportarCsv(self, ruta="Datacrude/02IntermediateData/Sensores_limpio.csv"):
        destino = self._resolverRuta(ruta)
        destino.parent.mkdir(parents=True, exist_ok=True)
        self.dfClean.to_csv(destino, index=False)
        print(f"Dataset limpio exportado exitosamente a: {destino} ({self.dfClean.shape[0]} filas)")
        return self

    def ejecutarPipeline(self):
        self.dfClean = self.dfOriginal.copy()
        self.diagnosticar()
        self.eliminarColumnasFantasma()
        self.normalizarFechas()
        self.integrarFuenteSueno()
        self.filtrarDiasSinUso()
        self.aplicarOutliers()
        self.limpiarCategorias()
        self.validar()
        return self.dfClean