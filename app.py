from flask import Flask
from config import Config
from extensions import db, migrate  # Import from extensions
from routes import teams, players, coaches

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(teams.bp)
    app.register_blueprint(players.bp)
    app.register_blueprint(coaches.bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
