# Created: 16.03.2011
# Copyright (c) 2011-2018, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals

from ezdxf.tools.c23 import isstring
from ezdxf.lldxf.types import DXFTag
from ezdxf.lldxf.extendedtags import ExtendedTags
from ezdxf.lldxf.attributes import DXFAttr, DXFAttributes, DefSubclass
from ezdxf.legacy import tableentries as legacy
from ezdxf.dxfentity import DXFEntity
from ezdxf.tools.complex_ltype import lin_compiler

_LAYERTEMPLATE = """0
LAYER
5
LayerHandle
100
AcDbSymbolTableRecord
100
AcDbLayerTableRecord
2
LayerName
70
0
62
7
6
Continuous
290
1
390
0
"""

# code 390 is required for AutoCAD
# Pointer/handle to PlotStyleName
# uses tag(390, ...) from the '0' layer

none_subclass = DefSubclass(None, {
    'handle': DXFAttr(5),
    'owner': DXFAttr(330),
})

symbol_subclass = DefSubclass('AcDbSymbolTableRecord', {})

layer_subclass = DefSubclass('AcDbLayerTableRecord', {
    'name': DXFAttr(2),  # layer name
    'flags': DXFAttr(70),
    'color': DXFAttr(62),  # dxf color index
    'linetype': DXFAttr(6),  # linetype name
    'plot': DXFAttr(290),  # don't plot this layer if 0 else 1
    'line_weight': DXFAttr(370),  # enum value???
    'lineweight': DXFAttr(370),  # enum value???
    'plot_style_name': DXFAttr(390),  # handle to PlotStyleName object
    'material': DXFAttr(347),  # handle to Material object
})


class Layer(legacy.Layer):
    __slots__ = ()
    TEMPLATE = ExtendedTags.from_text(_LAYERTEMPLATE)
    DXFATTRIBS = DXFAttributes(none_subclass, symbol_subclass, layer_subclass)

    @classmethod
    def new(cls, handle, dxfattribs=None, drawing=None):
        layer = super(Layer, cls).new(handle, dxfattribs, drawing)
        # just for testing scenarios where drawing is None
        if drawing is not None:
            layer.dxf.plot_style_name = drawing.rootdict['ACAD_PLOTSTYLENAME']
        return layer


_STYLETEMPLATE = """0
STYLE
5
0
100
AcDbSymbolTableRecord
100
AcDbTextStyleTableRecord
2
STYLENAME
70
0
40
0.0
41
1.0
50
0.0
71
0
42
0.2
3
arial.ttf
4

"""
style_subclass = DefSubclass('AcDbTextStyleTableRecord', {
    'name': DXFAttr(2),
    'flags': DXFAttr(70),
    'height': DXFAttr(40),  # fixed height, 0 if not fixed
    'width': DXFAttr(41),  # width factor
    'oblique': DXFAttr(50),  # oblique angle in degree, 0 = vertical
    'generation_flags': DXFAttr(71),  # 2 = backward, 4 = mirrored in Y
    'last_height': DXFAttr(42),  # last height used
    'font': DXFAttr(3),  # primary font file name
    'bigfont': DXFAttr(4),  # big font name, blank if none
})


class Style(legacy.Style):
    __slots__ = ()
    TEMPLATE = ExtendedTags.from_text(_STYLETEMPLATE)
    DXFATTRIBS = DXFAttributes(none_subclass, symbol_subclass, style_subclass)


_LTYPETEMPLATE = """0
LTYPE
5
0
100
AcDbSymbolTableRecord
100
AcDbLinetypeTableRecord
2
LTYPENAME
70
0
3
LTYPEDESCRIPTION
72
65
"""
linetype_subclass = DefSubclass('AcDbLinetypeTableRecord', {
    'name': DXFAttr(2),
    'description': DXFAttr(3),
    'length': DXFAttr(40),
    'items': DXFAttr(73),
})


class Linetype(legacy.Linetype):
    __slots__ = ()
    TEMPLATE = ExtendedTags.from_text(_LTYPETEMPLATE)
    DXFATTRIBS = DXFAttributes(none_subclass, symbol_subclass, linetype_subclass)

    def _setup_pattern(self, pattern, length):
        complex_line_type = True if isstring(pattern) else False
        if complex_line_type:  # a .lin like line type definition string
            self._setup_complex_pattern(pattern, length)
        else:
            # pattern: [2.0, 1.25, -0.25, 0.25, -0.25] - 1. element is total pattern length
            # pattern elements: >0 line, <0 gap, =0 point
            subclass = self.tags.get_subclass('AcDbLinetypeTableRecord')
            subclass.append(DXFTag(73, len(pattern) - 1))
            subclass.append(DXFTag(40, float(pattern[0])))
            for element in pattern[1:]:
                subclass.append(DXFTag(49, float(element)))
                subclass.append(DXFTag(74, 0))

    def _setup_complex_pattern(self, pattern, length):
        tokens = lin_compiler(pattern)
        subclass = self.tags.get_subclass('AcDbLinetypeTableRecord')
        subclass.append(DXFTag(73, 0))  # temp length of 0
        subclass.append(DXFTag(40, length))
        count = 0
        for token in tokens:
            if isinstance(token, DXFTag):
                if subclass[-1].code == 49:  # useless 74 only after 49 :))
                    subclass.append(DXFTag(74, 0))
                subclass.append(token)
                count += 1
            else:  # TEXT or SHAPE
                subclass.extend(token.complex_ltype_tags(self.drawing))
        subclass.append(DXFTag(74, 0))  # useless 74 at the end :))
        subclass.update(DXFTag(73, count))


_APPIDTEMPLATE = """0
APPID
5
0
100
AcDbSymbolTableRecord
100
AcDbRegAppTableRecord
2
APPIDNAME
70
0
"""
appid_subclass = DefSubclass('AcDbRegAppTableRecord', {
    'name': DXFAttr(2),
    'flags': DXFAttr(70),
})


class AppID(legacy.AppID):
    __slots__ = ()
    TEMPLATE = ExtendedTags.from_text(_APPIDTEMPLATE)
    DXFATTRIBS = DXFAttributes(none_subclass, symbol_subclass, appid_subclass)


_DIMSTYLETEMPLATE = """0
DIMSTYLE
105
0
100
AcDbSymbolTableRecord
100
AcDbDimStyleTableRecord
2
STANDARD
70
0
3

4

5

6

7

40
1.0
41
3.0
42
2.0
43
9.0
44
5.0
45
0.0
46
0.0
47
0.0
48
0.0
140
3.0
141
2.0
142
0.0
143
25.399999999999999
144
1.0
145
0.0
146
1.0
147
2.0
71
0
72
0
73
1
74
1
75
0
76
0
77
0
78
0
170
0
171
2
172
0
173
0
174
0
175
0
176
0
177
0
178
0
"""
handle105_subclass = DefSubclass(None, {
    'handle': DXFAttr(105),
    'owner': DXFAttr(330),
})

dimstyle_subclass = DefSubclass('AcDbDimStyleTableRecord', {
    'name': DXFAttr(2),
    'flags': DXFAttr(70),
    'dimpost': DXFAttr(3),
    'dimapost': DXFAttr(4),
    'dimblk': DXFAttr(5),
    'dimblk1': DXFAttr(6),
    'dimblk2': DXFAttr(7),
    'dimscale': DXFAttr(40),
    'dimasz': DXFAttr(41),
    'dimexo': DXFAttr(42),
    'dimdli': DXFAttr(43),
    'dimexe': DXFAttr(44),
    'dimrnd': DXFAttr(45),
    'dimdle': DXFAttr(46),
    'dimtp': DXFAttr(47),
    'dimtm': DXFAttr(48),
    'dimtxt': DXFAttr(140),
    'dimcen': DXFAttr(141),
    'dimtsz': DXFAttr(142),
    'dimaltf': DXFAttr(143),
    'dimlfac': DXFAttr(144),
    'dimtvp': DXFAttr(145),
    'dimtfac': DXFAttr(146),
    'dimgap': DXFAttr(147),
    'dimaltrnd': DXFAttr(148),
    'dimtol': DXFAttr(71),
    'dimlim': DXFAttr(72),
    'dimtih': DXFAttr(73),
    'dimtoh': DXFAttr(74),
    'dimse1': DXFAttr(75),
    'dimse2': DXFAttr(76),
    'dimtad': DXFAttr(77),
    'dimzin': DXFAttr(78),
    'dimazin': DXFAttr(79),
    'dimalt': DXFAttr(170),
    'dimaltd': DXFAttr(171),
    'dimtofl': DXFAttr(172),
    'dimsah': DXFAttr(173),
    'dimtix': DXFAttr(174),
    'dimsoxd': DXFAttr(175),
    'dimclrd': DXFAttr(176),
    'dimclre': DXFAttr(177),
    'dimclrt': DXFAttr(178),
    'dimadec': DXFAttr(179),
    'dimunit': DXFAttr(270),
    'dimdec': DXFAttr(271),
    'dimtdec': DXFAttr(272),
    'dimaltu': DXFAttr(273),
    'dimalttd': DXFAttr(274),
    'dimaunit': DXFAttr(275),
    'dimfrac': DXFAttr(276),
    'dimlunit': DXFAttr(277),
    'dimdsep': DXFAttr(278),
    'dimtmove': DXFAttr(279),
    'dimjust': DXFAttr(280),
    'dimsd1': DXFAttr(281),
    'dimsd2': DXFAttr(282),
    'dimtolj': DXFAttr(283),
    'dimaltz': DXFAttr(285),
    'dimalttz': DXFAttr(286),
    'dimfit': DXFAttr(287),  # obsolete, now use DIMATFIT and DIMTMOVE
    'dimupt': DXFAttr(288),
    'dimatfit': DXFAttr(289),
    'dimtxsty_handle': DXFAttr(340),  # handle of referenced STYLE
    'dimldrblk_handle': DXFAttr(341),  # handle of referenced BLOCK
    'dimblk_handle': DXFAttr(342),  # handle of referenced BLOCK
    'dimblk1_handle': DXFAttr(343),  # handle of referenced BLOCK
    'dimblk2_handle': DXFAttr(344),  # handle of referenced BLOCK
    'dimlwd': DXFAttr(371),  # lineweight enum value
    'dimlwe': DXFAttr(372),  # lineweight enum value
})


class DimStyle(legacy.DimStyle):
    __slots__ = ()
    TEMPLATE = ExtendedTags.from_text(_DIMSTYLETEMPLATE)
    DXFATTRIBS = DXFAttributes(handle105_subclass, symbol_subclass, dimstyle_subclass)


_UCSTEMPLATE = """0
UCS
5
0
100
AcDbSymbolTableRecord
100
AcDbUCSTableRecord
2
UCSNAME
70
0
10
0.0
20
0.0
30
0.0
11
1.0
21
0.0
31
0.0
12
0.0
22
1.0
32
0.0
"""
ucs_subclass = DefSubclass('AcDbUCSTableRecord', {
    'name': DXFAttr(2),
    'flags': DXFAttr(70),
    'origin': DXFAttr(10, xtype='Point3D'),
    'xaxis': DXFAttr(11, xtype='Point3D'),
    'yaxis': DXFAttr(12, xtype='Point3D'),
})


class UCS(legacy.UCS):
    __slots__ = ()
    TEMPLATE = ExtendedTags.from_text(_UCSTEMPLATE)
    DXFATTRIBS = DXFAttributes(none_subclass, symbol_subclass, ucs_subclass)


_VIEWTEMPLATE = """0
VIEW
5
0
100
AcDbSymbolTableRecord
100
AcDbViewTableRecord
2
VIEWNAME
70
0
10
0.0
20
0.0
11
1.0
21
1.0
31
1.0
12
0.0
22
0.0
32
0.0
40
70.
41
1.0
42
50.0
43
0.0
44
0.0
50
0.0
71
0
"""
view_subclass = DefSubclass('AcDbViewTableRecord', {
    'name': DXFAttr(2),
    'flags': DXFAttr(70),
    'height': DXFAttr(40),
    'width': DXFAttr(41),
    'center_point': DXFAttr(10, xtype='Point2D'),
    'direction_point': DXFAttr(11, xtype='Point3D'),
    'target_point': DXFAttr(12, xtype='Point3D'),
    'lens_length': DXFAttr(42),
    'front_clipping': DXFAttr(43),
    'back_clipping': DXFAttr(44),
    'view_twist': DXFAttr(50),
    'view_mode': DXFAttr(71),
})


class View(legacy.View):
    __slots__ = ()
    TEMPLATE = ExtendedTags.from_text(_VIEWTEMPLATE)
    DXFATTRIBS = DXFAttributes(none_subclass, symbol_subclass, view_subclass)


_VPORTTEMPLATE = """0
VPORT
5
0
100
AcDbSymbolTableRecord
100
AcDbViewportTableRecord
2
VPORTNAME
70
0
10
0.0
20
0.0
11
1.0
21
1.0
12
70.0
22
50.0
13
0.0
23
0.0
14
0.5
24
0.5
15
0.5
25
0.5
16
0.0
26
0.0
36
1.0
17
0.0
27
0.0
37
0.0
40
70.
41
1.34
42
50.0
43
0.0
44
0.0
50
0.0
51
0.0
71
0
72
1000
73
1
74
3
75
0
76
0
77
0
78
0
"""
vport_subclass = DefSubclass('AcDbViewportTableRecord', {
    'name': DXFAttr(2),
    'flags': DXFAttr(70),
    'lower_left': DXFAttr(10, xtype='Point2D'),
    'upper_right': DXFAttr(11, xtype='Point2D'),
    'center_point': DXFAttr(12, xtype='Point2D'),
    'snap_base': DXFAttr(13, xtype='Point2D'),
    'snap_spacing': DXFAttr(14, xtype='Point2D'),
    'grid_spacing': DXFAttr(15, xtype='Point2D'),
    'direction_point': DXFAttr(16, xtype='Point3D'),
    'target_point': DXFAttr(17, xtype='Point3D'),
    'height': DXFAttr(40),
    'aspect_ratio': DXFAttr(41),
    'lens_length': DXFAttr(42),
    'front_clipping': DXFAttr(43),
    'back_clipping': DXFAttr(44),
    'snap_rotation': DXFAttr(50),
    'view_twist': DXFAttr(51),
    'status': DXFAttr(68),
    'view_mode': DXFAttr(71),
    'circle_zoom': DXFAttr(72),
    'fast_zoom': DXFAttr(73),
    'ucs_icon': DXFAttr(74),
    'snap_on': DXFAttr(75),
    'grid_on': DXFAttr(76),
    'snap_style': DXFAttr(77),
    'snap_isopair': DXFAttr(78),
})


class VPort(legacy.VPort):
    __slots__ = ()
    TEMPLATE = ExtendedTags.from_text(_VPORTTEMPLATE)
    DXFATTRIBS = DXFAttributes(none_subclass, symbol_subclass, vport_subclass)


_BLOCKRECORDTEMPLATE = """0
BLOCK_RECORD
5
0
330
0
100
AcDbSymbolTableRecord
100
AcDbBlockTableRecord
2
BLOCK_RECORD_NAME
340
0
"""
blockrec_subclass = DefSubclass('AcDbBlockTableRecord', {
    'name': DXFAttr(2),
    'layout': DXFAttr(340),
})


class BlockRecord(DXFEntity):
    """ Internal Object - use at your own risk!

    Required fields:
    owner: Soft-pointer ID/handle to owner object
    layout: Hard-pointer ID/handle to associated LAYOUT object - is '0' if block definition
    """
    __slots__ = ()
    TEMPLATE = ExtendedTags.from_text(_BLOCKRECORDTEMPLATE)
    DXFATTRIBS = DXFAttributes(none_subclass, symbol_subclass, blockrec_subclass)
