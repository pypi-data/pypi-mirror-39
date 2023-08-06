LIME file format
================

The LIME file format is described in `this document`__.

.. _lime_description: http://usqcd.jlab.org/usqcd-docs/c-lime/lime_1p2.pdf

__ lime_description_

A brief summary follows. A LIME file is composed by one or more LIME
records, one after the other. One LIME record has the following structure:

 +-----------------------------+
 | header (144 bytes)          |
 +-----------------------------+
 | data (<=2^63 bytes)         |
 +-----------------------------+
 | null padding (0 to 7 bytes) |
 +-----------------------------+

About the padding: the data block is completed with so many times '0' 
as needed to make its length (number of bytes) divisible by 8.


Header
======

The header of each LIME record has the following structure:

 +------------------------------------------------+
 | 32 bits (>): LIME magic number (1164413355_10) |
 +------------------------------------------------+
 | 16 bits (>): LIME file version number          |
 +------------------------------------------------+
 |  1 bit: Message begin bit                      |
 +------------------------------------------------+
 |  1 bit: Message end bit                        |
 +------------------------------------------------+
 | 14 bits: reserved space                        |
 +------------------------------------------------+
 | 64 bits (>): data length                       |
 +------------------------------------------------+
 | 128 bytes (ASCII): LIME type                   |
 +------------------------------------------------+


