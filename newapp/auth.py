from django.contrib.auth.backends import ModelBackend
from ldap3 import Server, Connection, ALL
from django.conf import settings

class LDAPBackend(ModelBackend):
    
    def authenticate(username, password):
        if(username and password):
            server = Server(settings.LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN, get_info=ALL)
            try:
                conn = Connection(server, user='FILE\\' + username, password=password, auto_bind=True)
                print(conn)
                who = conn.extend.standard.who_am_i()
                if who:
                    conn.unbind()
                    return username
            except:
                return None
        else:
            return None