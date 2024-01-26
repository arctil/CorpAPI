from flask import Blueprint, render_template

oldpublic = Blueprint(
    'oldpublic', __name__,
    template_folder='template'
)

@oldpublic.route('/api/v1/public/documentation')
def old_public_documentation():
    return render_template("public_documentation.html")

@oldpublic.route('/api/v1/private/documentation')
def old_private_documentation():
    return render_template("private_documentation.html")