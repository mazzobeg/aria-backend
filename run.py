from app import Application

if __name__ == '__main__':
    application = Application("sqlite:///articles.db", False)
    application.init()
    application.app.run(debug=True)

