import database
import gui

def main():
    database.create_tables()
    gui.create_gui()

if __name__ == "__main__":
    main()
