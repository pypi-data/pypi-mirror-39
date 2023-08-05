"""
Change to/from any base you like
Example:
    from myFbase import MyFbase

    mfb = MyFbase('abc')
    print(mfb.encode(8))  # cc
    print(mfb.decode('cc'))  # 8
"""

from .myfbase import MyFbase
__version__ = "0.0.2"
