from bitstomach2.signals._comparison import Comparison
from bitstomach2.signals._trend import Trend
from utils.namespace import PSDO

__all__ = ["Comparison"]

signal_map = {
    PSDO.performance_gap_content: Comparison,
    PSDO.negative_performance_trend_content: Trend
}

