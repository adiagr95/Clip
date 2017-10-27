from __future__ import absolute_import

from .base import *
from .constant import *
from .twilio import *

try:
    if os.environ['MOJO_SERVER'] == 'prod':
        ENV = 'prod'
        from .aws_prod import *
        from .prod import *
    else:
        ENV = 'dev'
        from .aws_dev import *
        from .dev import *
except:
    ENV = 'dev'
    from .aws_dev import *
    from .dev import *
