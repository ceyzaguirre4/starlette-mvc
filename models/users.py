import sqlalchemy
from starlette.authentication import (
    AuthenticationBackend, AuthenticationError, SimpleUser, UnauthenticatedUser,
    AuthCredentials
)


def create_table(metadata):
    return sqlalchemy.Table(
        "users",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("name", sqlalchemy.String),
        sqlalchemy.Column("male", sqlalchemy.Boolean),
    )


# for user authentication
class userAuthentication(AuthenticationBackend):
    async def authenticate(self, request):
        def is_valid(auth):
            # TODO: You'd want to verify the username and password here,
            #       possibly by installing `DatabaseMiddleware`
            #       and retrieving user information from `request.database`.
            return True

        if "Authorization" not in request.headers:
            return
        
        auth = request.headers["Authorization"]

        if not is_valid(auth):
            raise AuthenticationError('Invalid basic auth credentials')

        return AuthCredentials(["user_auth"]), SimpleUser('TODO:username')
