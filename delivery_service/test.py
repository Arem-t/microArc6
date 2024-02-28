from keycloak.keycloak_openid import KeycloakOpenID

KEYCLOAK_URL = "http://0.0.0.0:8180/"
KEYCLOAK_CLIENT_ID = "mikhin"
KEYCLOAK_REALM = "delivery_service_realm"
KEYCLOAK_CLIENT_SECRET = "AliwqwCWP6RvWgENTnWaFvopI3G5s7lm"

keycloak_openid = KeycloakOpenID(server_url=KEYCLOAK_URL,
                                  client_id=KEYCLOAK_CLIENT_ID,
                                  realm_name=KEYCLOAK_REALM,
                                  client_secret_key=KEYCLOAK_CLIENT_SECRET)

token = keycloak_openid.token("testuser", "1")

token_info = keycloak_openid.introspect(token["access_token"])

print(token_info)