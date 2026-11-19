import os
from collections import defaultdict
from flask import Flask, render_template, redirect, url_for, request, session, flash, abort, send_from_directory
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, PerfilForm
from models import consultar, Perfil, Estudio, Experiencia, Habilidad

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "cambiar-en-produccion")
CSRFProtect(app)  # Flask-WTF: protege todos los formularios con token CSRF

TIPOS = {"estudio": Estudio, "experiencia": Experiencia, "habilidad": Habilidad}


def crear_admin():
    """Crea el usuario admin la primera vez (datos en variables de entorno)."""
    user, pwd = os.environ.get("ADMIN_USER"), os.environ.get("ADMIN_PASSWORD")
    if not (user and pwd):
        return
    try:
        if not consultar("SELECT id FROM usuario LIMIT 1", uno=True):
            consultar("INSERT INTO usuario (username, password_hash) VALUES (%s, %s)",
                      (user, generate_password_hash(pwd)))
    except Exception as e:
        print("No se pudo crear el admin:", e)


crear_admin()


def solo_admin():
    if not session.get("admin"):
        abort(403)


@app.route("/")
def inicio():
    grupos = defaultdict(list)
    for h in Habilidad.listar():
        grupos[h.detalle()].append(h)
    return render_template("index.html", perfil=Perfil.obtener(), estudios=Estudio.listar(),
                           experiencias=Experiencia.listar(), grupos=grupos)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = consultar("SELECT * FROM usuario WHERE username = %s", (form.username.data,), uno=True)
        if u and check_password_hash(u["password_hash"], form.password.data):
            session["admin"] = True
            return redirect(url_for("editar"))
        flash("Usuario o contraseña incorrectos.")
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("inicio"))


@app.route("/editar", methods=["GET", "POST"])
def editar():
    solo_admin()
    perfil = Perfil.obtener()
    form = PerfilForm(data=perfil)
    if form.validate_on_submit():
        Perfil.guardar(form)
        flash("Cambios guardados.")
        return redirect(url_for("editar"))
    items = {t: c.listar() for t, c in TIPOS.items()}
    return render_template("editar.html", form=form, items=items, tipos=TIPOS)


@app.route("/item/<tipo>/nuevo", methods=["POST"])
def item_nuevo(tipo):
    solo_admin()
    if tipo not in TIPOS:
        abort(404)
    TIPOS[tipo].crear(request.form)
    return redirect(url_for("editar"))


@app.route("/item/<tipo>/<int:item_id>/borrar", methods=["POST"])
def item_borrar(tipo, item_id):
    solo_admin()
    if tipo not in TIPOS:
        abort(404)
    TIPOS[tipo].borrar(item_id)
    return redirect(url_for("editar"))


@app.route("/cv")
def cv():
    return send_from_directory("static", "cv.pdf", as_attachment=True, download_name="CV-Lautaro-Reyes.pdf")


if __name__ == "__main__":
    app.run(debug=True)
