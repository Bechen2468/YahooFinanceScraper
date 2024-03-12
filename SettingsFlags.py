from enum import Enum, auto

class SettingsFlags(Enum):
    EARNINGS_EST = auto()       # Analysis
    REVENUE_EST = auto()
    EARNINGS_HIST = auto()
    EPS_TREND = auto()
    GROWTH_EST = auto()
    RECOMMEND_RATING = auto()
    PRICE_TARGET_EST = auto()
    INCOME_STATEMENT = auto()   # Financials
    BALANCE_SHEET = auto()
    CASH_FLOW = auto()
    VALUATION = auto()          # Statistics
    PROFITABILITY = auto()      
    MANAGEMENT_EFF = auto()
    EARNINGS_DATE = auto()      # Sumary