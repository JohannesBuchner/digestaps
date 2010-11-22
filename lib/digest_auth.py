# This file is part of 'NTLM Authorization Proxy Server'
# Copyright 2001 Dmitry A. Rozmanov <dima@xenon.spb.ru>
#
# NTLM APS is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# NTLM APS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with the sofware; see the file COPYING. If not, write to the
# Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
#

import string, select, base64
import digest_messages, utils

digest_messages = digest_messages.digest_messages()

# 
# See RFC2617
# Also used bits from urllib2.AbstractDigestAuthHandler
# 

class digest_auther:
    """
    Digest authenticator class. Makes an HTTP authentication using Digest method.
    """
    lastauth = ''

    #-----------------------------------------------------------------------
    def __init__(self):
        ""
        pass


    #-----------------------------------------------------------------------
    def proxy_digest_authentication(self, connection):
        self._digest_authentication(connection, 'Proxy-', 'Proxy-')
    #-----------------------------------------------------------------------
    def www_digest_authentication(self, connection):
        self._digest_authentication(connection, '', 'WWW-')
    
    #-----------------------------------------------------------------------
    def _digest_authentication(self, connection, clientheaderprefix = '', serverheaderprefix = ''):
        ""
        connection.logger.log('*** Authorization in progress...\n')
        connection.close_rserver()
        # build an environment
        env = self.build_env_dict(connection)

        auth = connection.rserver_head_obj.get_param_values(serverheaderprefix + 'Authenticate')
        if auth:
            msg2 = auth[0][len('Digest '):]
            connection.logger_auth.log(digest_messages.debug_message2(msg2))
            nonce = digest_messages.parse_message2(msg2)
            Digest_msg3 = digest_messages.create_message3(nonce, env, connection.client_head_obj)
            connection.logger_auth.log(digest_messages.debug_message3(Digest_msg3))
        else:
            Digest_msg3 = ''

        self.lastauth = 'Digest ' + Digest_msg3
        tmp_client_head_obj = connection.client_head_obj.copy()
        tmp_client_head_obj.replace_param_value(clientheaderprefix + 'Authorization', self.lastauth)

        connection.logger.log('*** Connecting to Proxy for Digest request...')
        connection.connect_rserver()
        connection.reset_rserver()
        connection.rserver_buffer = ''
        connection.logger.log('*** Sending Digest header (not body) with Msg3...')
        tmp_client_head_obj.send(connection.rserver_socket)
        connection.logger.log('Done.\n')
        connection.logger.log('*** Digest header with Msg3:\n=====\n' + tmp_client_head_obj.__repr__())

        # upon exit all the remote server variables are reset
        # so new remote server response will be taken by the usual way in connection.run()
        connection.logger.log('*** End of Digest authorization process.\n')

    #-----------------------------------------------------------------------
    def build_env_dict(self, connection):
        ""
        connection.logger.log('*** Building environment for Digest.\n')

        env = {}

        env['USER'] = connection.config['DIGEST_AUTH']['USER']
        env['PASSWORD'] = connection.config['DIGEST_AUTH']['PASSWORD']

        connection.logger.log('*** Digest User: %s\n' % (env['USER'],))

        connection.logger.log('*** Environment has been built successfully.\n')

        return env

