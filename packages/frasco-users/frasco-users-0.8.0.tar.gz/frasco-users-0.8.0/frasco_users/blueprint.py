from frasco import (Blueprint, with_actions, redirect, request, current_app,\
                    url_for, flash, current_context, pass_feature, session,\
                    populate_obj, ContextExitException)
from frasco.expression import compile_expr
import datetime
import requests


bp = Blueprint("users", __name__, template_folder="templates")


def make_redirect_url(value):
    if value.startswith('http://') or value.startswith('https://'):
        return value
    return url_for(value)


@bp.view('/login', template="users/login.html")
@with_actions([{"form": "LoginForm"}])
@with_actions("form_submitted", ["users.login"])
@pass_feature("users")
def login(users):
    if not users.options["allow_login"]:
        if users.options["login_disallowed_message"]:
            flash(users.options["login_disallowed_message"], "error")
        return redirect(url_for(users.options.get("redirect_after_login_disallowed") or\
            "index", next=request.args.get("next")))
    redirect_url = request.args.get("next") or make_redirect_url(users.options["redirect_after_login"])
    if users.logged_in() or request.method == "POST":
        if (users.options['expire_password_after'] and users.current.last_password_change_at and \
          (datetime.datetime.utcnow() - users.current.last_password_change_at).total_seconds() > users.options['expire_password_after']) \
          or users.current.must_reset_password_at_login:
            token = users._gen_reset_password_token(users.current)
            users.logout()
            flash(users.options['password_expired_message'], 'error')
            return redirect(url_for('.reset_password', token=token))
        return redirect(redirect_url)


@bp.view('/logout')
@with_actions(["users.logout"])
def logout():
    redirect_to = current_app.features.users.options["redirect_after_logout"]
    if redirect_to:
        return redirect(make_redirect_url(redirect_to))


@bp.view('/signup', template="users/signup.html")
@with_actions([
    {"form": {"name": "SignupForm", "obj": "$session[oauth_user_defaults]", "validate_on_submit": False}}])
@pass_feature("users")
def signup(users):
    if request.method == "GET" and not "oauth" in request.args:
        # signup was accessed directly so we ensure that oauth
        # params stored in session are cleaned. this can happen
        # if a user started to login using an oauth provider but
        # didn't complete the process
        session.pop("oauth_user_defaults", None)
        session.pop("oauth_user_attrs", None)

    current_context["must_provide_password"] = "oauth_user_attrs" not in session \
        or users.options["oauth_must_provide_password"]

    redirect_url = request.args.get("next") or make_redirect_url(users.options["redirect_after_signup"])
    if users.logged_in():
        return redirect(redirect_url)
        
    allow_signup = users.options["allow_signup"]
    if users.options["oauth_signup_only"] and "oauth_user_attrs" not in session:
        allow_signup = False
    if not allow_signup:
        if users.options["signup_disallowed_message"]:
            flash(users.options["signup_disallowed_message"], "error")
        return redirect(url_for(users.options.get("redirect_after_signup_disallowed") or\
            "users.login", next=request.args.get("next")))

    if current_context["form"].is_submitted() and current_context["form"].validate():
        if users.options['recaptcha_secret'] and not current_app.debug and not current_app.testing:
            if 'g-recaptcha-response' not in request.form:
                return redirect(url_for('users.signup', next=request.args.get('next')))
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data={
                'secret': users.options['recaptcha_secret'],
                'response': request.form['g-recaptcha-response'],
                'remote_ip': request.remote_addr
            })
            if r.status_code != 200 or not r.json().get('success'):
                if users.options['recaptcha_fail_message']:
                    flash(users.options['recaptcha_fail_message'], 'error')
                return redirect(url_for('users.signup', next=request.args.get('next')))

        user = users.model()
        if "oauth_user_defaults" in session:
            populate_obj(user, session["oauth_user_defaults"] or {})

        if users.options['require_code_on_signup'] and 'code' in current_context['form'] and\
          not users.check_signup_code(current_context['form'].code.data):
            if users.options['bad_signup_code_message']:
                flash(users.options['bad_signup_code_message'], 'error')
            return redirect(url_for('users.signup', next=request.args.get('next')))

        users.signup(user, form=current_context["form"],
            must_provide_password=current_context["must_provide_password"], **session.get("oauth_user_attrs", {}))
        session.pop("oauth_user_defaults", None)
        session.pop("oauth_user_attrs", None)
        return redirect(redirect_url)


@bp.route('/signup/oauth')
@pass_feature("users", "models")
def oauth_signup(users, models):
    if "oauth_user_attrs" not in session or users.options["oauth_must_signup"]:
        oauth = 1 if users.options["oauth_must_signup"] else 0
        return redirect(url_for(".signup", oauth=oauth, next=request.args.get("next")))

    signup_url = url_for(".signup", oauth=1, next=request.args.get("next"))
    user = users.model()
    populate_obj(user, session["oauth_user_defaults"] or {})
    if not users.validate_user(user, flash_messages=False, raise_error=False):
        return redirect(signup_url)

    try:
        users.signup(user, must_provide_password=False, **session["oauth_user_attrs"])
    except ContextExitException:
        return redirect(signup_url)
    del session["oauth_user_defaults"]
    del session["oauth_user_attrs"]
    return redirect(request.args.get("next") or make_redirect_url(users.options["redirect_after_login"]))


@bp.view('/login/reset-password', template="users/send_reset_password.html")
@with_actions([{"form": "SendResetPasswordForm"}])
@with_actions("form_submitted", ["users.gen_reset_password_token"])
def send_reset_password():
    msg = current_app.features.users.options["reset_password_token_success_message"]
    redirect_to = current_app.features.users.options["redirect_after_reset_password_token"]
    if request.method == "POST":
        if msg:
            flash(msg, "success")
        if redirect_to:
            return redirect(make_redirect_url(redirect_to))


@bp.view('/login/reset-password/<token>', methods=('GET', 'POST'), template="users/reset_password.html")
@with_actions([{"form": "ResetPasswordForm"}])
@with_actions("form_submitted", ["users.reset_password"])
def reset_password(token):
    msg = current_app.features.users.options["reset_password_success_message"]
    redirect_to = current_app.features.users.options["redirect_after_reset_password"]
    if request.method == "POST":
        if msg:
            flash(msg, "success")
        if redirect_to:
            return redirect(make_redirect_url(redirect_to))
