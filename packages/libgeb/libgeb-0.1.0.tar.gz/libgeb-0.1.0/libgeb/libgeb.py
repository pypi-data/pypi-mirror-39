#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 11:04:08 2018

@author: antony
"""

CHECK = 42
VERSION = 1
DEFAULT_WINDOW = 1000

INT_BYTES = 4
VERSION_BYTE_OFFSET = INT_BYTES
WINDOW_BYTE_OFFSET = VERSION_BYTE_OFFSET + 1

ENCODE_GENE = 1
ENCODE_TRANSCRIPT = 2
ENCODE_EXON = 4

DEFAULT_WINDOW = 1000


def get_bins_file_name(prefix, chr):
    return '{}.bins.{}.geb'.format(prefix, chr)

def get_btree_file_name(prefix, chr):
    return '{}.btree.{}.geb'.format(prefix, chr)
    
def get_elements_file_name(prefix):
    return '{}.elements.geb'.format(prefix)

def get_data_file_name(prefix):
    return '{}.data.geb'.format(prefix)

def get_radix_file_name(prefix):
    return '{}.radix.geb'.format(prefix)