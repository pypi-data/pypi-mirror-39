======
TODO's
======

* make `epoch.zulu` serialize microsecond-level accuracy (instead of the
  current millisecond) and make it print the minimal necessary, eg:

    input                     output
    -----                     ------
    1234567890                2009-02-13T23:31:30Z
    1234567890.12             2009-02-13T23:31:30.12Z
    1234567890.123456         2009-02-13T23:31:30.123456Z
    1234567890.123456789      2009-02-13T23:31:30.123456Z
