from quart import Blueprint, redirect, render_template, url_for

from app.controllers.auth_controller import AuthController
from app.decorators.auth import redirect_if_authenticated
from app.forms.login import LoginForm

login_router = Blueprint("login", __name__)


@login_router.get("/login")
@redirect_if_authenticated()
async def login_page():
    form = await LoginForm.create_form()
    return await render_template("pages/login.html", form=form)


@login_router.post("/login")
@redirect_if_authenticated()
async def login_user_by_form():
    form = await LoginForm.create_form()

    if not await form.validate_on_submit():
        return await render_template("pages/login.html", form=form)

    result = await AuthController().login(
        form.username.data,
        form.password.data,
        form.remember_me.data,
    )

    if result.success:
        return redirect(url_for("files.files_page"))

    return await render_template("pages/login.html", form=form, message=result.error)
