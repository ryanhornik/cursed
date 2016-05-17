from functools import partial
from views import OptionsView
from views.options_view import Option
from views.view_controller import ViewController


def cleanup_and_exit(view):
    view.cleanup()
    exit()


def main():
    controller = ViewController()

    settings_view = OptionsView('Settings', options=(
        Option('Hello', lambda: None),
        Option('Goodbye', lambda: None),
        Option('Back', controller.pop),
    ))

    main_menu_view = OptionsView(title="Main Menu")
    main_menu_view.set_options(
        (
            Option('Fuck', action=main_menu_view.flash_and_beep),
            Option('Settings', action=partial(controller.push, settings_view)),
            Option('Exit', action=partial(cleanup_and_exit, main_menu_view))
        )
    )

    controller.push(main_menu_view)

    try:
        while True:
            controller.current.loop()
    finally:
        controller.cleanup()


if __name__ == "__main__":
    main()
