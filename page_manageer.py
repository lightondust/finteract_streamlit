from page.data_view import data_view
from page.statistics import statistics, code_selected
from page.explore import explore


PAGE_LIST = [
    '統計分布',
    '銘柄比較',
    '銘柄探索',
    'データをみる'
]

PAGE_MAP = {
    '統計分布': statistics,
    '銘柄比較': code_selected,
    '銘柄探索': explore,
    'データをみる': data_view
}
