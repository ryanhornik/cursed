from game.scenes import MainMenuScene
from engine.controllers import SceneController


def main():
    controller = SceneController(initial=MainMenuScene)
    controller.start()


if __name__ == "__main__":
    main()
