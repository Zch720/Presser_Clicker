from ui.ui import ParserClickerUI
from presser_clicker import PresserClicker

def main():
    try:
        controller = PresserClicker()
        ParserClickerUI(controller).run()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
