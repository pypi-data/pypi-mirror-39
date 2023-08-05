# myFbase

Change to/from any base you like

## How to use

### Installation

    $ pip install myFbase

### Usage

    from myFbase import MyFbase

    mfb = MyFbase('abc')
    print(mfb.encode(8))  # cc
    print(mfb.decode('cc'))  # 8
