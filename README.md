# El Tetrado

This is an application to analyze base pairing patterns of DNA/RNA 3D
structures to find and classify tetrads and quadruplexes. For more
details, please refer to Popenda *et al.* (2019)

# Dependencies

The project is written in Python 3 and uses only standard libraries. The
main mode of operation is to analyze JSON outputs generated by DSSR (Lu,
Bussemaker and Olson, 2015). User is required to either run `x3dna-dssr
--json` himself and provide paths only to the output files or to
[download](http://forum.x3dna.org/site-announcements/download-instructions/)
`x3dna-dssr` binary and place it alongside El Tetrado.

# Usage

    usage: eltetrado [-h] [--json] [--strict] [--version] input
    
    positional arguments:
      input       a JSON file produced by DSSR if "--json" is used, otherwise a
                  PDB or PDBx/MMCIF file to be analyzed first by DSSR
    
    optional arguments:
      -h, --help  show this help message and exit
      --json      parse input file from JSON format
      --strict    nucleotides in tetrade linked only by cWH pairing
      --version   show program's version number and exit

  - `--json`: When set, the input is assumed to be a JSON file generated
    with `x3dna-dssr --json`. Otherwise, the input will be treated as a
    DNA/RNA 3D structure in PDB or PDBx/mmCIF format
  - `--strict`: When set, a tetrad can consist of cWH base pairs only.
    Otherwise, a tetrad may contain any type of base
pairs

# Examples

## 1MY9: Solution structure of a K+ cation stabilized dimeric RNA quadruplex containing two G:G(:A):G:G(:A) hexads, G:G:G:G tetrads and UUUU loops

![](1MY9.png)

    $ curl ftp://ftp.wwpdb.org/pub/pdb/data/structures/divided/mmCIF/my/1my9.cif.gz | gzip -d > 1my9.cif
    
    $ ./eltetrado 1my9.cif
    
    n4-helix with 4 tetrads
      parallel stem with 2 tetrads
        1:A.G1 1:A.G4 1:A.G10 1:A.G13 +O
        1:A.G2 1:A.G5 1:A.G11 1:A.G14 +O
      parallel stem with 2 tetrads
        1:B.G15 1:B.G18 1:B.G24 1:B.G27 +O
        1:B.G16 1:B.G19 1:B.G25 1:B.G28 +O

## 4RJ1: Structural variations and solvent structure of UGGGGU quadruplexes stabilized by Sr2+ ions

![](4RJ1.png)

    $ curl ftp://ftp.wwpdb.org/pub/pdb/data/biounit/coordinates/divided/rj/4rj1.pdb1.gz | gzip -d > 4rj1-1.pdb
    
    $ ./eltetrado 4rj1-1.pdb
    
    n4-helix with 9 tetrads
      parallel stem with 5 tetrads
        1:A.G1002 3:A.G1002 2:A.G1002 4:A.G1002
        1:A.G1003 3:A.G1003 2:A.G1003 4:A.G1003
        1:A.G1004 3:A.G1004 2:A.G1004 4:A.G1004
        1:A.G1005 3:A.G1005 2:A.G1005 4:A.G1005
        1:A.U1006 3:A.U1006 2:A.U1006 4:A.U1006
      parallel stem with 4 tetrads
        1:B.G2002 3:B.G2002 2:B.G2002 4:B.G2002
        1:B.G2003 3:B.G2003 2:B.G2003 4:B.G2003
        1:B.G2004 3:B.G2004 2:B.G2004 4:B.G2004
        1:B.G2005 3:B.G2005 2:B.G2005 4:B.G2005
    single tetrad without stacking
        1:B.U2006 3:B.U2006 2:B.U2006 4:B.U2006

# Bibliography

<div id="refs" class="references">

<div id="ref-Lu2015">

Lu, X. J., Bussemaker, H. J. and Olson, W. K. (2015) ‘DSSR: An
integrated software tool for dissecting the spatial structure of RNA’,
*Nucleic Acids Research*, 43(21), p. gkv716. doi:
[10.1093/nar/gkv716](https://doi.org/10.1093/nar/gkv716).

</div>

<div id="ref-Popenda2019">

Popenda, M., Miskiewicz, J., Sarzynska, J., Zok, T. and Szachniuk, M.
(2019) ‘Novel classification of tetrads and quadruplex structures’, *in
press*.

</div>

</div>
