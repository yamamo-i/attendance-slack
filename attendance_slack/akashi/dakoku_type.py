from enum import Enum


class DakokuType(Enum):
    """
    [ref] https://akashi.zendesk.com/hc/ja/articles/115000475854-AKASHI-%E5%85%AC%E9%96%8BAPI-%E4%BB%95%E6%A7%98#stamp
        11 : 出勤
        12 : 退勤
        TODO: 21以降は今使ってない
        21 : 直行
        22 : 直帰
        31 : 休憩入
        32 : 休憩戻
    """
    SHUKKIN = 11
    TAIKIN = 12
