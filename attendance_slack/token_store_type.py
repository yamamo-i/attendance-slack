import enum


class TokenStoreType(enum.Enum):
    """
    Tokenを取得できるところを可変にできるため、一覧を整理する
    """
    LOCAL = 'local'
    AWS_SSM = 'aws_ssm'

