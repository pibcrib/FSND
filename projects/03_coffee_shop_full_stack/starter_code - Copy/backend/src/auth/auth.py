import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'pibcrib.us.auth0.com'
ALGORITHMS = ['RS256']
# ik coffee shop is spelled wrong here but it was too much of a hassle to remake the auth0 api so I rolled with it
API_AUDIENCE = 'coffeshop'


# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


#     get_token_auth_header()
#       it should attempt to get the header from the request
#       it should raise an AuthError if no header is present
#       it should attempt to split bearer and the token
#       it should raise an AuthError if the header is malformed
#       return the token part of the header
def get_token_auth_header():
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']

        # separates Bearer from JWT token and returns only the token
        header_parts = auth_header.split(' ')
        if len(header_parts) == 2:
            if header_parts[0].lower() == 'bearer':
                token = header_parts[1]
                return token
            else:
                raise AuthError(
                    {'code': 'invalid_header', 'description': 'Authorization header does not contain Bearer token.'}, 401)
        else:
            raise AuthError(
                {'code': 'invalid_header', 'description': 'Malformed Autorization header.'}, 401)

    raise AuthError({'code': 'invalid_header',
                    'description': 'Authorization is not present in the request headers.'}, 401)


#      check_permissions(permission, payload)
#           @INPUTS
#               permission: string permission (i.e. 'post:drink')
#               payload: decoded jwt payload
#
#           it should raise an AuthError if permissions are not included in the payload
#           it should raise an AuthError if the requested permission string is not in the payload permissions array
#           return true otherwise
def check_permissions(permission, payload):
    # gets list of permissions included in verified JWT payload
    payload_permissions = payload['permissions']
    if payload_permissions:
        for p in payload_permissions:
            if p == permission:
                return True

        # raises error if payload_permissions does not contain permission needed to access resource
        raise AuthError({'code': 'invalid_permission',
                        'description': 'Access Forbidden. User is not allowed to access resource.'}, 403)

    raise AuthError({'code': 'invalid_permission',
                    'description': 'No permission(s) were included in payload. User is not allowed to access resource.'}, 403)


#      verify_decode_jwt(token)
#           @INPUTS
#           token: a json web token (string)
#
#           it should be an Auth0 token with key id (kid)
#           it should verify the token using Auth0 /.well-known/jwks.json
#           it should decode the payload from the token
#           it should validate the claims
#           return the decoded payload
def verify_decode_jwt(token):
    # Gets set of public keys used for verifying JWTs issued by Auth0, signed using RS256
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # gets ecrypted JWT header from unverified token
    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({'code': 'invalid_header',
                        'description': 'Malformed Authorization header.'}, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    # validates JWT, and returns payload if decryption was successful
    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 401)

    # raises an error if the set of public keys does not have a key with KID that matches the token's KID
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 400)


#      requires_auth(permission='')
#           @INPUTS
#           permission: string permission (i.e. 'post:drink')
#
#           it should use the get_token_auth_header method to get the token
#           it should use the verify_decode_jwt method to decode the jwt
#           it should use the check_permissions method validate claims and check the requested permission
#           return the decorator which passes the decoded payload to the decorated method
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
                check_permissions(permission, payload)

            except AuthError as e:
                print(e)
                raise e
            except Exception as e:
                print(e)
                raise e

            return f(*args, **kwargs)

        return wrapper
    return requires_auth_decorator
