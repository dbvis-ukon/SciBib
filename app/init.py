import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from configurations import DB_URL
from backend.db_controller.db import db
from backend.db_controller.db import users, role, roles_users
from backend.db_controller.query.users import addUser
from backend.db_controller.query.role import addRole
from backend.db_controller.query.roles_users import addRolesUsers
from main import app, init_logging


def init_tables():
    """
    Initialize database tables
    """
    engine = db.create_engine(DB_URL, {})
    db.metadata.create_all(engine)

def userExists(session, u):
    """
    Check if a user already exists in the database
    @param session: An open SQLAlchemy session
    @type session: SQLAlchemy session
    @param u: the user object to check against
    @type u: User object
    @return: if the user already exists
    @rtype: bool
    """
    with app.app_context():
        exists = session.query(users).filter(users.username == u).first()
        return True if exists is not None else False

def roleExists(session, r):
    """
    Check if a role already exists in the database
    @param session: An open SQLAlchemy session
    @type session: SQLAlchemy session
    @param r: the role object to check against
    @type r: Role object
    @return: if the role already exists
    @rtype: bool
    """
    with app.app_context():
        exists = session.query(role).filter(role.name == r).first()
        return True if exists is not None else False

def rolesUsersExists(session, r, u):
    """
    Check if a roles <-> users mapping already exists in the database
    @param session: An open SQLAlchemy session
    @type session: SQLAlchemy session
    @param r: the role object to check against
    @type r: Role object
    @param u: the user object to check against
    @type u: User object
    @return: if the mapping already exists
    @rtype: bool
    """
    with app.app_context():
        exists = session.query(roles_users).filter(roles_users.c.role_id == r and roles_users.c.user_id == u).first()
        return True if exists is not None else False

def create_admin_user_and_roles():
    """
    Initialize the admin user for the database
    """
    engine = db.create_engine(DB_URL, {})
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        with app.app_context():
            # add new user
            if not userExists(session, 'admin'):
                newUser = addUser(session,
                              username='admin',
                              password='superuser',
                              active=1)
            else:
                newUser = session.query(users).filter(users.username == 'admin').first()

            if not roleExists(session, 'admin'):
                newRole = addRole(session,
                              name='admin')
            else:
                newRole = session.query(role).filter(role.name == 'admin').first()

            if not roleExists(session, 'editor'):
                newRole2 = addRole(session,
                              name='editor')

            session.flush()
            user_id = newUser.id
            role_id = newRole.id

            if not rolesUsersExists(session, role_id, user_id):
                addRolesUsers(session,
                          user_id=user_id,
                          role_id=role_id)
            session.commit()
    except Exception:
        app.logger.exception('Could not create admin user')
    finally:
        session.close()

def execute_sql_file(path):
    """
    Execute sql from file
    @param path: path to sql file
    @type path: string
    """
    sql = open(path)
    engine = db.create_engine(DB_URL, {})
    escaped_sql = text(sql.read().replace('\n', ' '))
    engine.execute(escaped_sql)

def main():
    """
    Initialize the database. Needs only to be executed when scibib is first initialized. If already initialized,
    this file will just do nothing.
    """
    # log to get error messages
    init_logging()
    init_tables()
    create_admin_user_and_roles()
    #execute_sql_file(os.path.join('scripts', 'add_unique_user.sql'))
    execute_sql_file(os.path.join('scripts', 'triggerCitename.sql'))


if __name__ == '__main__':
    main()
    print("Initialized database")
