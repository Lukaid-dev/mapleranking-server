import os

from django.utils import timezone

from apps.users.models import User, UserSession
from firebase_admin import auth
from firebase_admin import credentials
from firebase_admin import initialize_app
from rest_framework import authentication, exceptions, status
from rest_framework.response import Response

from .exceptions import FirebaseError
from .exceptions import NoAuthToken

cred = credentials.Certificate(
    {
        "type": os.environ.get("FIREBASE_ACCOUNT_TYPE"),
        "project_id": os.environ.get("FIREBASE_PROJECT_ID"),
        "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID"),
        "private_key": os.environ.get("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
        "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
        "client_id": os.environ.get("FIREBASE_CLIENT_ID"),
        "auth_uri": os.environ.get("FIREBASE_AUTH_URI"),
        "token_uri": os.environ.get("FIREBASE_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.environ.get(
            "FIREBASE_AUTH_PROVIDER_X509_CERT_URL"
        ),
        "client_x509_cert_url": os.environ.get("FIREBASE_CLIENT_X509_CERT_URL"),
    }
)

default_app = initialize_app(cred)


class FirebaseAuthentication(authentication.BaseAuthentication):
    # override authenticate method and write our custom firebase authentication.#

    def authenticate(self, request):
        # Get the authorization Token, It raise exception when no authorization Token is given
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            raise NoAuthToken("No auth token provided")

        # Decoding the Token It raise exception when decode failed.
        id_token = auth_header.split(" ").pop()
        decoded_token = None
        try:
            decoded_token = auth.verify_id_token(id_token)
        except ValueError:
            raise exceptions.AuthenticationFailed(
                "JWT was found to be invalid, or the App’s project ID cannot "
                "be determined."
            )
        except (
            auth.InvalidIdTokenError,
            auth.ExpiredIdTokenError,
            auth.RevokedIdTokenError,
            auth.CertificateFetchError,
        ) as exc:
            if exc.code == "ID_TOKEN_REVOKED":
                raise exceptions.AuthenticationFailed(
                    "Token revoked, inform the user to reauthenticate or " "signOut()."
                )
            else:
                raise exceptions.AuthenticationFailed("Token is invalid.")

        # Return Nothing
        if not id_token or not decoded_token:
            return None

        # Get the uid of an user
        try:
            uid = decoded_token.get("uid")
            email = decoded_token.get("email")
            name = decoded_token.get("name") or ""
            username = email.split("@").pop(0)
            picture = decoded_token.get("picture")
            social = decoded_token.get("firebase").get("sign_in_provider").split(".")[0]
            now = timezone.now()

        except Exception:
            raise FirebaseError()

        if User.objects.filter(uid=uid, is_deleted=False).exists():
            user = User.objects.get(uid=uid, is_deleted=False)
        else:
            # uid가 일치하지만, 이미 삭제된 유저라면
            if User.objects.filter(uid=uid, is_deleted=True).exists():
                print("This user is deleted")
                return Response(
                    {"message": "This user is deleted"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            else:
                # if user is not exist, create user
                username_check = User.objects.filter(username=username).exists()
                # 만약 username이 존재한다면, username에 1씩 증가하는 숫자를 붙여준다.
                if username_check:
                    num = User.objects.filter(username__startswith=username).count() + 1
                    username = f"{username}_{num}"

                user = User.objects.create(
                    uid=uid,
                    username=username,
                    email=email,
                    name=name,
                    date_joined=now,
                    firebase_picture=picture,
                )

        user.last_login = now
        user.save()

        # token
        auth_time = timezone.datetime.fromtimestamp(
            decoded_token["auth_time"]
        ).astimezone()
        issued_at = timezone.datetime.fromtimestamp(decoded_token["iat"]).astimezone()
        expired_at = timezone.datetime.fromtimestamp(decoded_token["exp"]).astimezone()

        session = UserSession.objects.filter(user=user, is_expired=False).last()

        if session:
            if session.expired_at.astimezone() == expired_at:
                session.accessed_at = now
                session.count += 1
                session.save()
            else:
                session.is_expired = True
                session.save()

                UserSession.objects.create(
                    user=user,
                    accessed_at=now,
                    count=1,
                    expired_at=expired_at,
                    auth_time=auth_time,
                    issued_at=issued_at,
                    social=social,
                )
        else:
            UserSession.objects.create(
                user=user,
                accessed_at=now,
                count=1,
                expired_at=expired_at,
                auth_time=auth_time,
                issued_at=issued_at,
                social=social,
            )

        return (user, None)
