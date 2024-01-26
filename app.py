from flask import Flask, Blueprint
from v2.private import routes as private
from v2.public import routes as public
from v1.public import routes as old


app = Flask(__name__, template_folder='template', static_folder='template/static')

# Registering blueprints
app.register_blueprint(private.private)
app.register_blueprint(public.public)
app.register_blueprint(old.oldpublic)


if __name__ == '__main__':
    app.run(debug=True)
