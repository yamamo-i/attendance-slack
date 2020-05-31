from slackbot.bot import Bot
import logging


def main():
    bot = Bot()
    bot.run()


if __name__ == "__main__":
    # TODO: configのクラスを作って最初にコールできるようにする
    logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', level=logging.INFO)
    logging.info("starting....")
    main()
