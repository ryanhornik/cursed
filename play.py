import traceback

from game.scenes import MainMenuScene
from engine.controllers import SceneController


def main():
    controller = SceneController()
    controller.push(MainMenuScene)

    try:
        while True:
            controller.loop()
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
    finally:
        controller.cleanup()


if __name__ == "__main__":
    main()
