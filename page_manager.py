from page.data_view import data_view
from page.statistics import statistics
from page.explore import explore

PAGE_STATISTICS = ['データ可視化', statistics]
PAGE_EXPLORE = ['銘柄探索', explore]
PAGE_DATA_VIEW = ['データをみる', data_view]

_PAGE_ORDER = [
    PAGE_STATISTICS,
    PAGE_EXPLORE,
    PAGE_DATA_VIEW
]

PAGE_MAP = {p[0]: p[1] for p in _PAGE_ORDER}
PAGE_ORDER = [p[0] for p in _PAGE_ORDER]
