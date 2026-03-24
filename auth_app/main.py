from database.db_manager import DatabaseManager
from forms.login_form import LoginForm

def main():
    db_manager = DatabaseManager()

    app = LoginForm(db_manager)
    app.run()

if __name__ == "__main__":
    main()