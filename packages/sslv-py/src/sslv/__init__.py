'''
Find homes on SS.lv.

Sludinajumi class is the functional entrypoint for this. It
implements `homefinder_lib.Source` and as such works as described
in the interface.

This module also provides parsers for extracting information from
specific types of SS.lv webpages.
'''

from .sludinajumi import (
	Sludinajumi
)

from . import (
	parser
)

