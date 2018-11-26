#!/usr/bin/env python3

## 2018-11-26 : tkooda : convert tai64n timestamps on stdin to localtime (http://cr.yp.to/daemontools/tai64nlocal.html)

import sys
import re
import tai64n # https://github.com/tkooda/py-tai64
from datetime import timezone # Python 3.3+ , https://stackoverflow.com/questions/4563272/convert-a-python-utc-datetime-to-a-local-datetime-using-only-python-standard-lib/13287083


def main():
	pattern = re.compile( r"^@([0-9a-f]{24})(.*)", re.IGNORECASE )
	
	for line in sys.stdin:
		match = pattern.match( line )
		if match:
			dt = tai64n.decode_tai64n( match.group(1) ).replace( tzinfo = timezone.utc ).astimezone( tz = None ) # convert UTC to localtime
			sys.stdout.write( dt.strftime( "%Y-%m-%d %H:%M:%S.%f000" ) + match.group( 2 ) + "\n" )
		else:
			sys.stdout.write( line )
		sys.stdout.flush()


if __name__ == '__main__':
	main()

