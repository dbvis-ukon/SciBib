#
   Copyright (C) 2020 University of Konstanz -  Data Analysis and Visualization Group
   This file is part of SciBib <https://github.com/dbvis-ukon/SciBib>.

   SciBib is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   SciBib is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with SciBib.  If not, see <http://www.gnu.org/licenses/>.

#
#  SciBib is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SciBib is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SciBib.  If not, see <http://www.gnu.org/licenses/>.
#
#  SciBib is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SciBib is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SciBib.  If not, see <http://www.gnu.org/licenses/>.

from flask import Blueprint, render_template, request, jsonify, abort, current_app as app
from flask_security import login_required, roles_required
from flask_security.utils import hash_password, send_mail
from flask_security.recoverable import send_reset_password_instructions
from backend.db_controller.db import SQLAlchemy
# from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from backend.db_controller.db import users, role as Role, Users_publication
from backend.db_controller.query.users import addUser
from backend.db_controller.query.roles_users import addRolesUsers, deleteRolesUsersByUser, deleteRolesUsersByRole
from backend.db_controller.query.role import addRole

user_blueprint = Blueprint('user', __name__)

db = SQLAlchemy()

@user_blueprint.route('/admin/users')
@login_required
@roles_required('admin')
def render_user_management():
    """
    Render the view to manage new users and roles.
    @return: the view to render
    @rtype: unicode string
    """
    u = [ {'id': r.id,
               'username': r.username,
               'email': r.email,
               'active': r.active,
               'roles': [{'id': role.id, 'name': role.name} for role in r.roles]
               }
              for r in users.query.all() ]
    r = [ {'id': r.id, 'name': r.name, 'description': r.description} for r in Role.query.all()]


    return render_template('public/admin/users/user_management.html', data={'users': u, 'roles': r})

@user_blueprint.route('/add/user', methods=['POST'])
@login_required
@roles_required('admin')
def add_user():
    """
    Handles POST requests to add a new user to the database. Adds the new user to the database and sends a welcome email as well as
    an email to change the user password.
    @return: Either a JSON with an object of the new user or a HTTP 500 error
    @rtype: JSON
    """
    id = None

    session = db.session()
    try:
        if not 'input-email' in request.form or not isinstance(request.form['input-email'], str):
            raise ValueError("No email provided for adding a user.")

        firstname = request.form['input-firstname'] if 'input-firstname' in request.form else ''
        lastname = request.form['input-lastname'] if 'input-lastname' in request.form else ''
        email = request.form['input-email']
        username = email.split('@')[0]
        if len(username) < 2:
            app.logger.exception("{} {}: Username must be at least two characters long. Make sure to specify a valid email.".format(__file__, __name__))
            return ("Could not add user.", 500)

        password = request.form['input-password'] if 'input-password' in request.form else ''
        roles = request.form.getlist('select-roles') if 'select-roles' in request.form else []
        active = 1 if 'input-active' in request.form else 0

        newUser = addUser(session,
                firstname=firstname,
                lastname=lastname,
                username=username,
                email=email,
                password=password,
                active=active,
                created=datetime.now())
        session.flush()
        id = newUser.id

        for role in roles:
            addRolesUsers(session,
                user_id=id,
                role_id=role
            )
        session.commit()

        role_names = []
        for r in roles:
            role = session.query(Role.name).filter(Role.id == r).first()
            if role is not None:
                role_names.append(role[0])

        send_mail('[SciBib] Welcome!', newUser.email, 'welcome', user=newUser)
        send_reset_password_instructions(newUser)

        app.logger.info("{} {}: Successfully added user {} ({})".format(__file__, __name__, email, id))
        return jsonify({
            'msg': 'User {} successfully added.'.format(username),
            'user': {'id': id,
                    'firstname': firstname,
                     'lastname': lastname,
                     'email': email,
                     'username': username,
                     'roles': role_names,
                     'active': active}
        })
    except Exception as ex:
        app.logger.exception("{} {}: Exception occurred while trying to add user:".format(__file__, __name__))
        if id:
            session.query(users).filter(users.id == id).delete()
        session.rollback()
        return ("Could not add user: {}".format(ex), 500)
    finally:
        session.close()

@user_blueprint.route('/delete/user/', methods=['POST'])
@login_required
@roles_required('admin')
def delete_user():
    """
    Handles POST requests to delete a user from the database.
    @return: Either a JSON with a success messages or an HTTP 500 error in case of failure.
    @rtype: JSON
    """
    session = db.session()
    try:
        if not 'user_id' in request.json or not isinstance(request.json['user_id'], int):
            raise ValueError("user_id needed and user_id must be of type 'int'")

        user_id = request.json['user_id']

        deleteRolesUsersByUser(session, user_id)
        session.query(Users_publication).filter(Users_publication.user_id == user_id).delete()
        session.query(users).filter(users.id == user_id).delete()
        session.commit()

        app.logger.info("{} {}: Successfully removed user ({})".format(__file__, __name__, user_id))
        return jsonify({
            'msg': 'User successfully removed.'
        })
    except Exception:
        app.logger.exception("{} {}: Exception occurred while trying to delete user:".format(__file__, __name__))
        session.rollback()
        return ("Something went wrong. Could not remove user", 500)
    finally:
        session.close()


@user_blueprint.route('/edit/user/<user_id>', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def edit_user(user_id):
    """
    Handles GET and POST requests to edit a user. GET request sends info on user. POST request submits changes.
    In case of failure, any change is rolled-back.
    @param user_id: the database ID of the user to edit.
    @type user_id: int
    @return: JSON with the current user data or HTTP 500 in case of error
    @rtype: JSON
    """
    if request.method == 'GET':

        # user_id = request.args['user_id']
        session = db.session()
        try:
            u = session.query(users).filter(users.id == user_id).first()

            if u is None:
                abort(404, description="User not found.")

            #r = session.query(roles_users).filter(roles_users.user_id == user_id)
            return jsonify({'id': u.id,
                            'username': u.username,
                            'email': u.email,
                            'password': '',
                            'first_name': u.first_name,
                            'last_name': u.last_name,
                            'active': u.active,
                            'is_superuser': u.is_superuser,
                            'roles': [{'id': role.id, 'name': role.name} for role in u.roles]})
        except Exception:
            app.logger.exception("{} {}: Exception occurred while trying to delete category:".format(__file__, __name__))
            return ("An error occured.", 500)
            pass
        finally:
            session.close()
    elif request.method == 'POST':
        session = db.session()

        try:
            if not 'input-email' in request.form or not isinstance(request.form['input-email'], str):
                raise ValueError("No email provided for adding a user.")

            email = request.form['input-email']
            # handle special case for the admin user. It is the only user allowed without email
            username = email.split('@')[0] if request.form['input-username-hidden'] != 'admin' else 'admin'
            if len(username) < 2:
                app.logger.exception("{} {}: Username must be at least two characters long. Make sure to specify a valid email.".format(__file__, __name__))
                return ("Could not edit user.", 500)

            firstname = request.form['input-firstname'] if 'input-firstname' in request.form else ''
            lastname = request.form['input-lastname'] if 'input-lastname' in request.form  else ''
            password = hash_password(request.form['input-password']) if 'input-password' in request.form else ''
            roles = request.form.getlist('edit-select-roles') if 'edit-select-roles' in request.form else []
            active = 1 if 'input-active' in request.form else 0

            deleteRolesUsersByUser(session, user_id)

            update_data = {
                'username': username,
                'email': email,
                'first_name': firstname,
                'last_name': lastname,
                'active': active
            }
            if password != '':
                update_data['password'] = password

            session.query(users).filter(users.id == user_id).update(update_data)

            for role_id in roles:
                addRolesUsers(session,
                    user_id=user_id,
                    role_id=role_id
                )

            session.commit()
            app.logger.info("{} {}: Successfully edited user ({})".format(__file__, __name__, user_id))
            return jsonify({
                'msg': 'User edited successfully.',
                'user': {'username': username,
                         'email': email,
                         'firstname': firstname,
                         'lastname': lastname,
                         'active': active}
            })
        except Exception:
            app.logger.exception("{} {}: Exception occurred while trying to edit user: {}".format(__file__, __name__, user_id))
            session.rollback()
            return ("Could not edit user.", 500)
        finally:
            session.close()

@user_blueprint.route('/add/role', methods=['POST'])
@login_required
@roles_required('admin')
def add_role():
    """
    Handles POST requests to add a new role to the database.
    @return: Either a JSON containing an object of the new role or a HTTP 500 in case of error.
    @rtype: JSON
    """
    session = db.session()

    try:
        if not 'input-name' in request.form or not isinstance(request.form['input-name'], str):
            raise ValueError("A role name must be provided to add a role.")

        name = request.form['input-name']
        desc = request.form['input-description'] if 'input-description' in request.form else ''

        newRole = addRole(session,
                name=name,
                description=desc)
        session.commit()

        app.logger.info("{} {}: Successfully added role ({})".format(__file__, __name__, name))
        return jsonify({
            'msg': 'Role {} added successfully.'.format(name),
            'role': {'id': newRole.id, 'name': newRole.name, 'description': newRole.description}
        })
    except Exception:
        app.logger.exception("{} {}: Exception occurred while trying to add role:".format(__file__, __name__))
        session.rollback()
        return ("Something went wrong. Could not add role", 500)
    finally:
        session.close()

@user_blueprint.route('/delete/role/', methods=['POST'])
@login_required
@roles_required('admin')
def delete_role():
    """
    Handles POST requests to delete a role from the database.
    @return: Either a JSON with a success message in case of success or a HTTP 500 in case of failure.
    @rtype: JSON
    """
    role_id = request.json['role_id']
    session = db.session()
    try:
        if not 'role_id' in request.json or not isinstance(request.json['role_id'], int):
            raise ValueError("role_id needed and role_id must be of type 'int'")

        deleteRolesUsersByRole(session, role_id)
        session.query(Role).filter(Role.id == role_id).delete()
        session.commit()
        app.logger.info("{} {}: Successfully deleted role ({})".format(__file__, __name__, role_id))
        return jsonify({
            'msg': 'Role <b>removed</b> successfully.'
        })
    except Exception:
        app.logger.exception("{} {}: Exception occurred while trying to delete role:".format(__file__, __name__))
        session.rollback()
        return ("Something went wrong. Could not remove role", 500)
    finally:
        session.close()

@user_blueprint.route('/edit/role/<role_id>', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def edit_role(role_id):
    """
    Handles GET and POST requests to edit a role. GET requests sends current role info to the frontend. POST request
    submits changes.
    @param role_id: the database ID of the role to edit
    @type role_id: int
    @return: Either the current role info in case of success or a HTTP 500 in case of failure.
    @rtype:
    """
    if request.method == 'GET':
        session = db.session()
        try:
            r = session.query(Role).filter(Role.id == role_id).first()

            if r is None:
                abort(404, description="Role not found.")

            return jsonify({'id': r.id, 'name': r.name, 'description': r.description})
        except Exception:
            app.logger.exception("{} {}: Exception occurred while trying to delete category:".format(__file__, __name__))
            return ("An error occured.", 500)
        finally:
            session.close()
    elif request.method == 'POST':
        session = db.session()
        try:
            if not 'input-name' in request.form or not isinstance(request.form['input-name'], str):
                raise ValueError("Role name of typ 'str' needed to edit role.")

            name = request.form['input-name']
            description = request.form['input-description'] if 'input-description' in request.form else ''
            # update Publication data
            session.query(Role).filter(Role.id == role_id).update({
                'name': name,
                'description': description
            })
            session.commit()
            app.logger.info("{} {}: Successfully edited role ({})".format(__file__, __name__, role_id))
            return jsonify({
                'msg': 'Role edited successfully.',
                'role': {'id': role_id,'name': name, 'description': description}
            })
        except Exception:
            app.logger.exception("{} {}: Exception occurred while trying to delete category:".format(__file__, __name__))
            session.rollback()
            return ("An error occured.", 500)
        finally:
            session.close()
