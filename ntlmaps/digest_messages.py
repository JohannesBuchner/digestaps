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

import ntlm_procs, utils
import base64, string
import hashlib
import time

from urllib2 import randombytes

class digest_messages:
	nonce_count = 0 

	def get_algorithm_impls(self, algorithm): 
		# lambdas assume digest modules are imported at the top level 
		if algorithm == 'MD5': 
			H = lambda x: hashlib.md5(x).hexdigest() 
		elif algorithm == 'SHA1': 
			H = lambda x: hashlib.sha1(x).hexdigest() 
		# MD5-sess not implemented
		KD = lambda s, d: H("%s:%s" % (s, d)) 
		return H, KD

	def debug_message2(self, msg):
		return 'MESSAGE2:=> ' + str(self.parse_message2(msg)) + "\n"
	
	def parse_message2(self, msg):
		d = {}
		for pair in msg.split(","):
			split = pair.split("=")
			k = split[0].strip(' ')
			if len(split) == 2:
				v = split[1].strip(' ,"')
				d[k] = v
			else:
				pass
				#v = k
		return d

	def get_cnonce(self, nonce):
		dig = hashlib.sha1("%s:%s:%s:%s" % (self.nonce_count, nonce, 
			time.ctime(), randombytes(8))).hexdigest()
		return dig[:16] 

	def create_response3(self, chal, env, req = None):
		username = env['USER']
		password = env['PASSWORD']
		realm = chal['realm']
		nonce = chal['nonce']
		qop = chal.get('qop')
		algorithm = chal.get('algorithm', 'MD5')
		opaque = chal.get('opaque')
		
		H, KD = self.get_algorithm_impls(algorithm)
		entitydigest = None
		
		if False and algorithm and algorithm == 'MD5-sess':
			A1 = H('%s:%s:%s:%s:%s', (username, realm, password)) + ("%s:%s" % (nonce,cnonce))
		else:
			A1 = '%s:%s:%s' % (username, realm, password)
		
		if req is None:
			method = 'GET'
			digesturi = '/'
		else:
			method = req.get_http_method()
			digesturi = req.get_http_url()
			
		if not qop or qop == 'auth' or True:
			A2 = method + ':' + digesturi
		elif qop == 'auth-int':
			A2 = method + ':' + H(body)
		
		if qop and qop == 'auth':
			self.nonce_count += 1
			ncvalue = '%08x' % self.nonce_count
			cnonce = self.get_cnonce(nonce)
			reqdigest = KD(H(A1), nonce+":"+ncvalue+":"+cnonce+":"+qop+":"+H(A2)) 
		else:
			reqdigest = KD(H(A1), nonce+":"+H(A2))
		
		response = chal
		response['response'] = reqdigest
		if opaque:
			response['opaque'] = opaque
		else:
			response['digest'] = entitydigest
		response['nc'] = ncvalue
		response['opaque'] = opaque
		response['cnonce'] = cnonce
		response['uri'] = digesturi
		response['username'] = username
		del response['stale']
		return response
		
	def create_message3(self, chal, env, req):
		response = self.create_response3(chal, env, req)
		pairs = []
		for k in response.keys():
			v = response[k]
			if v is not None:
				pairs.append('%s="%s"' % (k, v))
		text = ", ".join(pairs)
		return text

	def debug_message3(self, msg):
		return msg

