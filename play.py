from views.view_controller import ViewController
from views.view_functions import MainMenuView


def main():
    controller = ViewController()
    controller.push(MainMenuView)

    try:
        while True:
            controller.current.loop()
    finally:
        controller.cleanup()


if __name__ == "__main__":
    main()
