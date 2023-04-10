from PyQT import *


def run():
    pyqt_application()


if __name__ == '__main__':
    try:
        sys.exit(run())
    except Exception as e:
        print(e, file=sys.stderr)

