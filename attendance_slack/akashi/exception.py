class UserNotFoundException(Exception):
    """登録されていないユーザが利用した場合のエラー. """
    pass


class BadShukkinStateException(Exception):
    """出勤の条件が整っていない場合のエラーエラー. """
    pass


class BadTaikinStateException(Exception):
    """退勤の条件が整っていない場合のエラーエラー. """
    pass
