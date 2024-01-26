from flask import Blueprint, render_template

oldprivate = Blueprint(
    'oldprivate', __name__,
    template_folder='template'
)

@oldprivate.route('/api/v1/private/documentation')
def old_private_documentation():
    return render_template("private_documentation.html")