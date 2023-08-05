# encoding: utf-8
# Copyright (C) 2014, Manfred Moitzi
# License: MIT-License
import pytest

import ezdxf
import os
FILE = "D:\Source\dxftest\ProE_AC1018.dxf"


def test_file_not_exists():
    return not os.path.exists(FILE)


@pytest.mark.skipIf(test_file_not_exists(), "Skip reading ProE AC1018: test file '{}' not available.".format(FILE))
def test_open_proe_ac1018():
    dwg = ezdxf.readfile(FILE)
    modelspace = dwg.modelspace()

    # are there entities in model space
    assert 17 == len(modelspace)

    # can you get entities
    lines = modelspace.query('LINE')
    assert 12 == len(lines)

    # is owner tag correct
    first_line = lines[0]
    assert modelspace.layout_key == first_line.dxf.owner

    # is paper space == 0
    assert 0 == first_line.dxf.paperspace
