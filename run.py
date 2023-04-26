import logging

from slackbot.bot import Bot


def main():
    # TODO: SSLエラーの暫定回避策、根本対処をしたい(https://github.com/yamamo-i/attendance-slack/issues/33)
    ssl._create_default_https_context = ssl._create_unverified_context
    bot = Bot()
    bot.run()


if __name__ == "__main__":
    # TODO: configのクラスを作って最初にコールできるようにする
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s]: %(message)s", level=logging.INFO
    )
    logging.info("starting....")
    main()
