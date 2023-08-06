pastpy - Python library for working with PastPerfect databases
==============================================================

Usage:

..

    from pastpy.object_dbf_table import ObjectDbfTable

    with ObjectDbfTable.open(dbf_file_path) as table:
        for object_ in table:
            print object_

where dbf_file_path is a path to the .DBF file (FoxPro) exported by PastPerfect 5.0. The .DBF file must be accompanied by a corresponding .FPT file with the same base name in the same directory.
