import pandas as pd
import numpy as np


class FeatureImportance:
    """
    특성 중요도 분석 관련 코드
    """

    @staticmethod
    def display_feature_importance(model):
        if hasattr(model, "feature_importances_"):
            df_import = pd.DataFrame(
                [np.round((model.feature_importances_) * 100, 2)],
                columns=[
                    "txFrequencyHz",
                    "focusRangeCm",
                    "numTxElements",
                    "txpgWaveformStyle",
                    "numTxCycles",
                    "elevAperIndex",
                    "IsTxAperModulationEn",
                    "probePitchCm",
                    "probeRadiusCm",
                    "probeElevAperCm0",
                    "probeElevFocusRangCm",
                ],
            )
            print(df_import)
