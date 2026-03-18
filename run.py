import sys


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "auto":
        from core.scheduler import executar_rotina
        executar_rotina()
    else:
        from app.app import iniciar_interface
        iniciar_interface()


if __name__ == "__main__":
    main()