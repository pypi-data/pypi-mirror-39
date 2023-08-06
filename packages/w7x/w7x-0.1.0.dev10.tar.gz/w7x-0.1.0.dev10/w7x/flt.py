#!/usr/bin/env
"""
Field line tracer specifics
author: daniel.boeckenhoff@ipp.mpg.de
"""

import w7x
from w7x import core
import tfields

import numpy as np
import logging
import os
import re
import pathlib
import functools
from six import string_types


class Base(core.Base):
    """
    Field Line Server Base
    """
    ws_server = w7x.Server.addr_field_line_server


class Points3D(tfields.Points3D, Base):
    """Imitation of the field_line_server Points3D Type.
    Inheriting from tfield.Points3D so the coordinate system is tracked and
    coordinate transformations are inherently possible

    Args:
        many ways to initialize:
        1.
            like tfields.Points3D
        2.
            points3D (osa.Points3D): copyConstructor
        3.
            pointsList (list): list of triples in varioues formats
    Attributes:

    Examples:
        see tfields.points3D.Points3D

        One further constructor implemented:
        >>> import w7x
        >>> ws_points = w7x.Points3D([[1, 2, 3], [4, 5, 6]])
        >>> ws_points_2 = w7x.Points3D(ws_points.as_input())
        >>> assert ws_points.equal(ws_points_2)

    """
    ws_server = w7x.Server.addr_field_line_server
    ws_class = "Points3D"

    def __new__(cls, tensors, *args, **kwargs):
        if w7x.is_w7x_instance(tensors,
                               cls.get_ws_class(),
                               convert=False):
            tensors = np.array([tensors.x1, tensors.x2, tensors.x3]).T
        obj = tfields.Points3D.__new__(cls, tensors, *args, **kwargs)
        return obj

    def __init__(self, *args, **kwargs):
        for attr in self.__slots__:
            kwargs.pop(attr, None)
        super(Base, self).__init__(self, *args, **kwargs)

    def as_input(self):
        """
        return field_line_server type copy of self
        """
        raw_points = self.get_ws_class()()
        raw_points.x1 = list(self[:, 0])
        raw_points.x2 = list(self[:, 1])
        raw_points.x3 = list(self[:, 2])
        return raw_points

    def to_segment_one(self, mirror_z=True):
        """
        Map the points to the first module of w7x and mirror to positive z
        if mirror_zOption is True. The mirror option is interesting for the
        divertor for example.
        Examples:
            >>> import w7x
            >>> import numpy as np
            >>> pStart = w7x.Points3D([[6, np.pi, 1],
            ...                        [6, np.pi / 5 * 3, -1]],
            ...                       coord_sys='cylinder')
            >>> pStart.to_segment_one()
            >>> pStart
            Points3D([[ 6.        , -0.62831853,  1.        ],
                      [ 6.        ,  0.62831853,  1.        ]])

        """
        with self.tmp_transform(tfields.bases.CYLINDER):
            offset_segment_0 = -2 * np.pi / 10
            self.to_segment(0, 5, 1, offset=offset_segment_0)
            if mirror_z:
                condition = self[:, 2] < 0
                self.mirror([1, 2], condition=condition)

    def where_phi_between(self, phi_min, phi_max):
        """
        Args:
            phi_min (float): minimum phi in radian
            phi_max (float): maximum phi in radian
        Returns:
            output of np.where with condition
        """
        with self.tmp_transform(tfields.bases.CYLINDER):
            phi = self[:, 1]
        if phi_min < phi_max:
            return np.where((phi_min <= phi) & (phi <= phi_max))
        elif phi_min > phi_max:
            return np.where(np.logical_not((phi_max < phi) & (phi < phi_min)))
        else:
            return np.where(phi == phi_min)

    def phi_between(self, phi_min, phi_max):
        """
        Args:
            phi_min (float): minimum phi in radian
            phi_max (float): maximum phi in radian
        Returns:
            bool: if phi of all points is in between the given values
        """
        return len(self.where_phi_between(phi_min, phi_max)[0]) == len(self)


class ConnectionLength(Points3D):
    """Class to Convert ConnectionLengthResult in.
    Make it easy to handle info about the different parts you gave it.
    The Hit points are the content of the np.ndarray (Points3D)

    Note:

    Args:
        connectionLengthResult

    Attributes:
        x1 (list): coordinate x
        x2 (list): coordinate y
        x3 (list): coordinate z
        lengths (list)
        parts (list): part ids refering to mm_ids index
        elements (list): element ids refering to face index + 1

    Examples:
        Adding up two instances
        >>> from w7x.flt import ConnectionLength
        >>> import numpy as np
        >>> c = ConnectionLength.create_test()
        >>> c.parts
        [0, 1, 2, 3, 4]
        >>> d = ConnectionLength.create_test()
        >>> b = ConnectionLength.merged(c, d)
        >>> b.parts
        [0, 1, 2, 3, 4, 0, 1, 2, 3, 4]
        >>> b
        ConnectionLength([[  1.        ,   0.        ,   0.97438334],
                          [  0.        ,   1.        ,   0.9579201 ],
                          [-80.        ,   1.        ,   1.9573    ],
                          [-80.        ,  -1.        ,   0.22222222],
                          [  0.        ,  -1.        ,   0.9579201 ],
                          [  1.        ,   0.        ,   0.97438334],
                          [  0.        ,   1.        ,   0.9579201 ],
                          [-80.        ,   1.        ,   1.9573    ],
                          [-80.        ,  -1.        ,   0.22222222],
                          [  0.        ,  -1.        ,   0.9579201 ]])
        >>> b.lengths
        [899.895318339, 2826.55635289, 2.55635289, 222.822222339, 2826.55635289, 899.895318339, 2826.55635289, 2.55635289, 222.822222339, 2826.55635289]
        >>> b.elements
        [44301, 20291, 2, 22222, 20291, 44301, 20291, 2, 22222, 20291]
        >>> len(b)
        10

        Retrieving Groups for all the components
        >>> b.mm_ids = [15, 16, 17, 18, 19]
        >>> assert b.hits(15).equal([[ 1.,  0.,  0.97438334],
        ...                          [ 1.,  0.,  0.97438334]],
        ...                         atol=1e-6, rtol=1e-6)
        >>> p = b.hits(18)
        >>> p.to_segment_one()
        >>> assert p.equal([[ 65.3091448 , -46.21380319, 0.22222222],
        ...                 [ 65.3091448 , -46.21380319, 0.22222222]],
        ...                atol=1e-6, rtol=1e-6)

        Saving and loading like in Points3D
        >>> from tempfile import NamedTemporaryFile
        >>> outFile = NamedTemporaryFile(suffix='.npz')
        >>> c.save(outFile.name)
        >>> _ = outFile.seek(0)
        >>> c1 = ConnectionLength.load(outFile.name)
        >>> assert np.all(c == c1)
        >>> assert np.array_equal(c.parts, [0, 1, 2, 3, 4])
        >>> assert np.array_equal(c.parts, c1.parts)

    """
    __slots__ = ['coord_sys', 'parts', 'elements', 'lengths', '_mm_ids']
    ws_class = "ConnectionLength"

    def __new__(cls, tensors, **kwargs):
        if isinstance(tensors, list):
            if w7x.is_w7x_instance(tensors, cls.get_ws_class()) or \
                    all([hasattr(con, attr)
                         for con in tensors
                         for attr in ['x', 'y', 'z', 'length', 'part', 'element']]):
                points = []
                parts = []
                elements = []
                lengths = []
                for con in tensors:
                    points.append([con.x, con.y, con.z])
                    lengths.append(con.length)
                    parts.append(con.part)
                    elements.append(con.element)
                tensors = points
                kwargs['parts'] = parts
                kwargs['elements'] = elements
                kwargs['lengths'] = lengths

        parts = kwargs.pop('parts', None)
        elements = kwargs.pop('elements', None)
        lengths = kwargs.pop('lengths', None)
        _mm_ids = kwargs.pop('_mm_ids', None)

        if issubclass(type(tensors), ConnectionLength):
            parts = parts or tensors.parts
            elements = elements or tensors.elements
            lengths = lengths or tensors.lengths
            _mm_ids = _mm_ids or tensors._mm_ids

        obj = super(ConnectionLength, cls).__new__(cls, tensors, **kwargs)
        obj.parts = parts
        obj.elements = elements
        obj.lengths = lengths
        obj._mm_ids = _mm_ids
        return obj

    @classmethod
    def merged(cls, *objects, **kwargs):
        """
        Overload merged for taking care of parts, elements and lenghts
            atrributes
        """
        if not all([isinstance(o, cls) for o in objects]):
            # TODO: could allow if all faceScalars are none
            raise TypeError("Merge constructor only accepts {cls} instances."
                            .format(**locals()))

        inst = super(ConnectionLength, cls).merged(*objects, **kwargs)

        kwargs['parts'] = kwargs.pop('parts',
                                     functools.reduce(lambda x, y: x + y,
                                                      [obj.parts for obj in objects]))
        kwargs['elements'] = kwargs.pop('elements',
                                        functools.reduce(lambda x, y: x + y,
                                                         [obj.elements for obj in objects]))
        kwargs['lengths'] = kwargs.pop('lengths',
                                       functools.reduce(lambda x, y: x + y,
                                                        [obj.lengths for obj in objects]))
        inst = cls.__new__(cls, inst, **kwargs)
        return inst

    @classmethod
    def create_test(cls):
        """
        Create a test class filled with some data.
        """
        class C():
            def __init__(self, **kwargs):
                self.__dict__.update(kwargs)
        a = []
        a.append(C(length=899.895318339,
                   x=1.,
                   y=0,
                   z=0.974383343584,
                   part=0,
                   element=44301))
        a.append(C(length=2826.55635289,
                   x=0,
                   y=1,
                   z=0.95792010423,
                   part=1,
                   element=20291))
        a.append(C(length=2.55635289,
                   x=-80,
                   y=1,
                   z=1.9573,
                   part=2,
                   element=2))
        a.append(C(length=222.822222339,
                   x=-80,
                   y=-1,
                   z=0.222222222224,
                   part=3,
                   element=22222))
        a.append(C(length=2826.55635289,
                   x=0,
                   y=-1,
                   z=0.95792010423,
                   part=4,
                   element=20291))
        obj = cls(a)
        obj.mm_ids = list(range(5))
        return obj

    @property
    def mm_ids(self):
        """
        database IDs from ComponentsDB
        """
        try:
            return self._mm_ids
        except:
            log = logging.getLogger()
            log.error(" No mm_ids specified")
            raise ValueError(" No mm_ids specified")

    @mm_ids.setter
    def mm_ids(self, mm_ids):
        if max(self.parts) >= len(mm_ids):
            raise ValueError("Too many parts for the mm_ids given.")
        self._mm_ids = mm_ids

    def hits(self, *mm_ids):
        """
        return the hit points of the field lines on the components of the
        connection Results for the given mm_ids.
        """
        mm_ids = set(mm_ids)
        mask = []
        for part in self.parts:
            if part < 0:  # All invalid parts get False, rest True
                mask.append(False)
            elif self.mm_ids[part] not in mm_ids:
                mask.append(False)
            else:
                mask.append(True)
        p = Points3D(self[mask])
        return p

    def meshed_models(self, mm_ids=None):
        if mm_ids is None:
            mm_ids = self.mm_ids
        elif not set(mm_ids).issubset(self.mm_ids):
            raise ValueError("mm_ids must be subset of self.mm_ids.")

        meshed_models = []
        for mm_id in mm_ids:
            meshed_models.append(MeshedModel.from_mm_id(mm_id))
        return meshed_models


class ComponentLoad(object):
    """
    Collection class for flt.ComponentLoad instances
    Provides methods for choosing specific components only

    Args:
        *component_load (webservice ComponentLoad):
            e.g.:
                (ComponentLoad){
                    id = 0
                    events = 1
                    elements[] = [
                                  (ElementLoad){
                                      id = 103638
                                      events = 1
                                      area = 0.000175667334795
                                  }
                                  ]
                }
    Examples:
        >>> from w7x.flt import ComponentLoad
        >>> l = ComponentLoad.create_test()
        >>> l.mm_ids = [181, 182, 183, 184, 185]
        >>> l.load_dict()[181]['events'] == [1, 42, 1]
        True

    """
    def __init__(self, component_load):
        self.componentIdDict = {}
        for cl in component_load:
            if cl.id not in self.componentIdDict:
                self.componentIdDict[cl.id] = {}
            for element in cl.elements:
                if element.id not in self.componentIdDict[cl.id]:
                    self.componentIdDict[cl.id][element.id] = element.events
                else:
                    self.componentIdDict[cl.id][element.id] += element.events

    @property
    def mm_ids(self):
        """
        database IDs from ComponentsDB
        """
        try:
            return self._mm_ids
        except:
            log = logging.getLogger()
            log.error(" No mm_ids specified")
            raise ValueError(" No mm_ids specified")

    @mm_ids.setter
    def mm_ids(self, mm_ids):
        self._mm_ids = mm_ids

    def _get_element_ids(self, component_id):
        return sorted(self.componentIdDict[component_id].keys())

    def _get_element_events(self, component_id):
        return [self.componentIdDict[component_id][eId] for eId in
                self._get_element_ids(component_id)]

    def load_dict(self):
        """
        Returns:
            dictionary with following structure:
                {<mm_id>: {'elementIds': <list of ids of elements/triangles>,
                           'events': <list with the number of occuring events corresponding to an element/triangle>},
                 <mm_id2>: ...}
        """
        mm_id_load_dict = {}
        if self.mm_ids is None:
            raise ValueError("Please set mm_ids before.")
        for component_id in sorted(self.componentIdDict.keys()):
            mm_id_load_dict[self.mm_ids[component_id]] = {'elementIds': self._get_element_ids(component_id),
                                                          'events': self._get_element_events(component_id)}
        return mm_id_load_dict

    @classmethod
    def create_test(cls):
        """
        Create a test class filled with some data.
        """
        class C():
            def __init__(self, **kwargs):
                self.__dict__.update(kwargs)
        a = []
        a.append(C(id=0,
                   events=3,
                   elements=[C(id=103638, events=1, area=0.00017),
                             C(id=123456, events=1, area=0.00017),
                             C(id=134679, events=1, area=0.00017)]
                   ))
        a.append(C(id=3,
                   events=21,
                   elements=[C(id=123, events=21, area=0.00017)]
                   ))
        a.append(C(id=0,
                   events=41,
                   elements=[C(id=123456, events=41, area=0.00017)]
                   ))
        return cls(a)


def interprete_mm_id(mm_id):
    """
    Examples:
        >>> from w7x.flt import interprete_mm_id

        mm_id defined in web service
        >>> interprete_mm_id(30)
        (30, None)

        mm_id derived from web service
        >>> interprete_mm_id(420000030)
        (30, 42)

        Own independent mm_id
        >>> interprete_mm_id(421000000)
        (None, 42)

        Own independent mm_id
        >>> interprete_mm_id(1000)
        (None, 1000)

    Returns:
        tuple with 2 arguments:
            1) ws_mm_id (int or None): mm_id from web service if derived from web service definition
            2) own_mm_id (int or None): user defined id

    """
    ws_mm_id = None
    own_mm_id = None
    if mm_id < 1e6:
        if mm_id < 1e3:
            ws_mm_id = mm_id
        else:
            own_mm_id = mm_id
    else:
        headTmp = mm_id // int(1e6)
        head = headTmp // 10
        mid = headTmp - head * 10
        tail = mm_id - headTmp * int(1e6)

        if mid == 1:
            # not derived
            if tail != 0:
                raise ValueError("If mid index is 1, The mm_id"
                                 "should not be derived by definition!")
        elif mid == 0:
            ws_mm_id = tail
        else:
            raise ValueError("Mid digit must be either 1 or 0.")
        own_mm_id = head

    return ws_mm_id, own_mm_id


def component_module(mm_id):
    """
    Returns:
        int: which module the geometry is in
    """
    compDBServer = w7x.get_server(w7x.Server.addr_components_db)
    if mm_id >= 1000:
        mm_id = int(mm_id / 1000)
    componentInfo = compDBServer.service.getComponentInfo(mm_id)[0]
    return int(componentInfo.location.replace('m ', ''))


class LCFSSettings(Base):
    prop_defaults = {
        'LCFSLeftX': None,
        'LCFSRightX': None,
        'LCFSNumPoints': 40,
        'LCFSThreshold': 1000.0,
        'LCFSAccuracy': 0.001
    }
    prop_order = ['LCFSLeftX', 'LCFSRightX']


class CylindricalGrid(Base):
    """
    Order of grid in the ws is
    for phi
        for r
            for z
    """
    prop_defaults = {
        'RMin': w7x.Defaults.CylindricalGrid.RMin,
        'RMax': w7x.Defaults.CylindricalGrid.RMax,
        'ZMin': w7x.Defaults.CylindricalGrid.ZMin,
        'ZMax': w7x.Defaults.CylindricalGrid.ZMax,
        'numR': w7x.Defaults.CylindricalGrid.numR,
        'numZ': w7x.Defaults.CylindricalGrid.numZ,
        'numPhi': w7x.Defaults.CylindricalGrid.numPhi,
        'PhiMin': w7x.Defaults.CylindricalGrid.PhiMin,
        'PhiMax': w7x.Defaults.CylindricalGrid.PhiMax
    }

    def spacing(self):
        return self.numR, self.numPhi, self.numZ


class CartesianGrid(Base):
    """
    Order of grid in the ws is
    for phi
        for r
            for z
    """
    prop_defaults = {
        'numX': w7x.Defaults.CartesianGrid.numX,
        'numY': w7x.Defaults.CartesianGrid.numY,
        'numZ': w7x.Defaults.CartesianGrid.numZ,
        'ZMin': w7x.Defaults.CartesianGrid.ZMin,
        'ZMax': w7x.Defaults.CartesianGrid.ZMax,
        'XMin': w7x.Defaults.CartesianGrid.XMin,
        'XMax': w7x.Defaults.CartesianGrid.XMax,
        'YMin': w7x.Defaults.CartesianGrid.YMin,
        'YMax': w7x.Defaults.CartesianGrid.YMax,
    }

    ws_class = "CartesianGrid"


class Grid(Base):
    """
    see http://webservices.ipp-hgw.mpg.de/docs/fieldlinetracer.html#Grid
    Examples:
        >>> from w7x.flt import CylindricalGrid, Grid
        >>> cyl = CylindricalGrid(numPhi=49)
        >>> afsFilePath = "/afs/ipp-garching.mpg.de/u/dboe/exch/fieldn_altern181x181x96.w7x.1000_1000_1000_1000_+0000_+0000.01.04m.dat"
        >>> grid = Grid(cylindrical=cyl, afsFileName=afsFilePath)
        >>> grid.as_input()
        (Grid){
            cylindrical = (CylindricalGrid){
                              RMin = 4.05
                              RMax = 6.75
                              ZMin = -1.35
                              ZMax = 1.35
                              numR = 181
                              numZ = 181
                              PhiMin = None (float)
                              PhiMax = None (float)
                              numPhi = 49
                          }
            hybrid = None (CylindricalGrid)
            afsFileName = /afs/ipp-garching.mpg.de/u/dboe/exch/fieldn_altern181x181x96.w7x.1000_1000_1000_1000_+0000_+0000.01.04m.dat
            gridField = None (Points3D)
            fieldSymmetry = 5
        }

    """
    prop_defaults = {'cylindrical': None,
                    'hybrid': None,
                    'afsFileName': None,
                    'gridField': None,
                    'fieldSymmetry': w7x.Defaults.fieldSymmetry,
                    }

    ws_class = "Grid"

    def __init__(self, **kwargs):
        super(Grid, self).__init__(**kwargs)
        """
        The wsDoku says you need to define hybrid but haukes code shows cylindrical.
        I will take default hybrid grid.
        It appears to not have any effect to change between the two.
        """
        if self.hybrid is not None:
            raise AttributeError("You should not use the hybrid grid.")
        if self.cylindrical is None:
            self.cylindrical = CylindricalGrid()


class Machine(Base):
    """
    Object to closely lie above web service Machine object
    Examples:
        >>> import w7x as ws
        >>> from w7x.flt import Machine, CartesianGrid
        >>> a = Machine(meshedModelsIds=w7x.MeshedModelsIds.divertor,
        ...             grid=CartesianGrid())
        >>> a.as_input()
        (Machine){
            meshedModels[] = [
        <BLANKLINE>
                              ]
            meshedModelsIds[] = [
                                 165,
                                 166,
                                 167,
                                 168,
                                 169
                                 ]
            assemblyIds[] = None (int)
            grid = (CartesianGrid){
                       XMin = -7
                       XMax = 7
                       YMin = -7
                       YMax = 7
                       ZMin = -1.5
                       ZMax = 1.5
                       numX = 500
                       numY = 500
                       numZ = 100
                   }
        }

    """
    prop_defaults = {'meshedModels': None,
                    'meshedModelsIds': None,
                    'assemblyIds': None,
                    'grid': None
                    }
    ws_class = "Machine"
    ws_class_args = [1]

    def __init__(self, *args, **kwargs):
        """
        Args:
            *args (int | Mesh3D | str):
                int -> mm_ids
                Mesh3D | str -> MeshedModel
        """
        if len(args) == 1 and isinstance(args[0], list):
            args = args[0]

        if len(args) == 1 and w7x.is_w7x_instance(args[0], self.get_ws_class()):
            # copy constructor
            pass
        elif len(args) > 0:
            raise DeprecationWarning("args only supported for copy constructor")
            # meshed_models = kwargs.pop('meshedModels', [])
            # meshed_models_ids = kwargs.pop('meshedModelsIds', [])
            # mm_ids = []
            # for arg in args:
            #     if issubclass(type(arg), tfields.Mesh3D):
            #         meshed_models.append(MeshedModel(arg))
            #     elif isinstance(arg, string_types):
            #         meshed_models.append(tfields.Mesh3D.load(arg))
            #     elif isinstance(arg, int):
            #         mm_ids.append(arg)
            #     else:
            #         arg_type = type(arg)
            #         raise NotImplementedError("No valid argument type "
            #                                   "'{arg_type}'.".format(**locals()))

            # for mm_id in mm_ids:
            #     ws_mm_id, own_mm_id = interprete_mm_id(mm_id)
            #     if own_mm_id is None:
            #         meshed_models_ids.append(mm_id)
            #     else:
            #         meshed_models.append(MeshedModel.from_mm_id(mm_id))

            # kwargs['meshedModels'] = meshed_models
            # kwargs['meshedModelsIds'] = meshed_models_ids
            # kwargs['grid'] = kwargs.pop('grid', CartesianGrid())

        meshed_models = kwargs.pop('meshedModels', [])
        for i in range(len(meshed_models)):
            mm = meshed_models[i]
            if issubclass(type(mm), tfields.Mesh3D):
                meshed_models[i] = MeshedModel(mm)
            if not isinstance(meshed_models[i], MeshedModel):
                raise ValueError("meshed model of wrong type {0}"
                                 .format(type(mm)))
        mm_ids_db = []
        mm_ids_user = []
        mm_ids = kwargs.pop('meshedModelsIds', [])
        for mm_id in mm_ids:
            ws_mm_id, own_mm_id = interprete_mm_id(mm_id)
            if own_mm_id is None:
                mm_ids_db.append(mm_id)
            else:
                mm_ids_user.append(mm_id)
        if len(meshed_models) != 0:
            if len(mm_ids_user) == 0:
                mm_ids_user = [1000 + i for i in range(len(meshed_models))]
            else:
                if len(mm_ids_user) != len(meshed_models):
                    raise ValueError("len(meshed_models) != len(mm_ids_user)")
        elif len(mm_ids_user) != 0:
            raise ValueError("len(meshed_models) != len(mm_ids_user)")

        kwargs['meshedModels'] = meshed_models
        kwargs['meshedModelsIds'] = mm_ids_db
        kwargs['grid'] = kwargs.pop('grid', CartesianGrid())
        super(Machine, self).__init__(**kwargs)
        self._mm_ids_user = mm_ids_user

    @classmethod
    def default(cls):
        return cls.from_mm_ids(*w7x.Defaults.Machine.mm_ids)

    @classmethod
    def from_mm_ids(cls, *mm_ids, **kwargs):
        grid = CartesianGrid()
        return cls(grid=grid,
                   meshedModelsIds=w7x.GeoSet(mm_ids))

    def get_mm_ids(self, user_defined=True, pre_defined=True):
        """
        Args:
            user_defined (bool): return mm_ids, defined by yourself (mm_id >= 1000)?
            pre_defined (bool): return mm_ids, defined by ws?
        """
        if pre_defined:
            mm_ids_db = self.meshedModelsIds or []
        else:
            mm_ids_db = []
        if user_defined:
            mm_ids_user = self._mm_ids_user
        else:
            mm_ids_user = []
        return mm_ids_user + mm_ids_db
        # pre_defined_mm_ids = []
        # user_defined_mm_ids = []
        # for mm_id in self.meshedModelsIds:
        #     if mm_id < 1000:
        #         if pre_defined:
        #             pre_defined_mm_ids.append(mm_id)
        #     else:
        #         if user_defined:
        #             user_defined_mm_ids.append(mm_id)
        # return tfields.lib.util.flatten(user_defined_mm_ids + pre_defined_mm_ids)

    @property
    def mm_ids(self):
        """
        database IDs from ComponentsDB
        """
        return self.get_mm_ids()

    @mm_ids.setter
    def mm_ids(self, mm_ids):
        self.meshedModelsIds = mm_ids

    def meshed_models(self,
                      user_defined=True,
                      pre_defined=False,
                      geoFileDir=None):
        """
        Args:
            user_defined (bool): return MeshedModels, defined by yourself (mm_id >= 1000)?
            pre_defined (bool): return MeshedModels, defined by ws?
        """
        meshed_models = []
        # go through user_defined mm_ids
        for mm_id in self.get_mm_ids(user_defined=user_defined, pre_defined=False):
            geoFilePath = os.path.join(geoFileDir, "mm_id_{0}.obj".format(mm_id))
            meshedModel = MeshedModel.load(geoFilePath).as_input()
            meshed_models.append(meshedModel)

        # go through pre_defined mm_ids
        compDBServer = w7x.get_server(w7x.Server.addr_components_db)
        for mm_id in self.get_mm_ids(user_defined=False, pre_defined=pre_defined):
            meshedModel = MeshedModel(compDBServer.service.getComponentData(mm_id)[0])
            meshed_models.append(meshedModel)
        return meshed_models

    def as_Mesh3D_list(self, user_defined=True, pre_defined=True):
        return [m.as_Mesh3D()
                for m in self.meshed_models(user_defined=user_defined,
                                            pre_defined=pre_defined)]

    def plot_poincare(self, phi=0, **kwargs):
        inters = self.intersect_mesh_phi_planes([phi])
        artists = []
        for mm_id, geoPoints in zip(self.mm_ids, inters[0]):
            geoSet = w7x.getGeoSet(mm_id)
            color = geoSet.color if geoSet else w7x.Defaults.Poincare.geometry_color
            plotKwargs = {'color': color,
                          'methodName': 'plot',
                          'lw': 1}
            plotKwargs.update(kwargs)
            artists.append(w7x.plot_poincare_surfaces(geoPoints, **plotKwargs))
        return artists

    def intersect_mesh_phi_planes(self, phi_list_rad):
        """Get poincare points for a set of mm_ids and phis
        with intersectMeshPhiPlane service from the Mesh server web service.

        Args:
            phi_list_rad (list of floats): list of phi in rad
        Returns:
            phi_container (list[list[Points3D for each vertex] for each mm_id] for each phi)
        Raises:

        Examples:
            >>> import w7x
            >>> machine = w7x.flt.Machine.from_mm_ids(165, 166)
            >>> res = machine.intersect_mesh_phi_planes([0.0, 0.34, 6 * 0.34])
            >>> assert res[0][0][0].equal([[ 5.74323774,  0.,  0.98876001],
            ...                            [ 5.7433343 ,  0.,  0.98801955]],
            ...                           atol=1e-6, rtol=1e-6)
            >>> assert res[0][0][1].equal([[ 5.74201939,  0.,  0.99807376],
            ...                            [ 5.74099873,  0.,  1.00585009]],
            ...                           atol=1e-6, rtol=1e-6)

            >>> res = machine.intersect_mesh_phi_planes([0.0,  5*0.31])
            >>> assert res[0][0][0].equal([[5.74323774, 0., 0.98876001],
            ...                            [5.7433343 , 0., 0.98801955]],
            ...                           atol=1e-6, rtol=1e-6)
            >>> assert res[0][0][1].equal([[ 5.74201939, 0.,  0.99807376],
            ...                            [ 5.74099873, 0.,  1.00585009]],
            ...                           atol=1e-6, rtol=1e-6)
            >>> assert res[1][1][0].equal([[ 6.07343869, 1.55, -0.68684114],
            ...                            [ 6.07343617, 1.55, -0.68893482]],
            ...                           atol=1e-6, rtol=1e-6)
            >>> assert res[1][1][1].equal([[ 6.07340735, 1.55, -0.70596002],
            ...                            [ 6.07343617, 1.55, -0.68893482]],
            ...                           atol=1e-6, rtol=1e-6)
            >>> len(machine.mm_ids) == len(res[0])
            True

        """
        # Check input
        log = logging.getLogger()
        if not type(phi_list_rad) is list:
            raise TypeError("phi_list_rad has to be of type list but is of type"
                            " %s" % type(phi_list_rad))

        if len(phi_list_rad) == 0:
            return []

        mesh_server = w7x.get_server(w7x.Server.addr_mesh_server)

        # Run intersectMeshPhiPlane service for each phi AND mm_id
        phi_container = []
        for iPhi, phi in tfields.lib.log.progressbar(zip(range(len(phi_list_rad)),
                                                         phi_list_rad),
                                                     log=log):
            mm_id_container = []
            for mm_id in self.mm_ids:
                poincare_points_list = []
                # Set up mesh set
                mesh_set = mesh_server.types.SurfaceMeshSet()
                wrap = mesh_server.types.SurfaceMeshWrap()
                reference = mesh_server.types.DataReference()
                reference.dataId = "10"
                wrap.reference = reference
                mesh_set.meshes = [wrap, ]
    
                # append mm_id_wrap
                mm_id_wrap = mesh_server.types.SurfaceMeshWrap()
                mm_id_reference = mesh_server.types.DataReference()
                mm_id_reference.dataId = str(mm_id)
                mm_id_wrap.reference = mm_id_reference
                mesh_set.meshes.append(mm_id_wrap)
    
                # ask web service for result and process it to right format
                res = mesh_server.service.intersectMeshPhiPlane(phi, mesh_set)  # careful: Returns None if there is no component.

                if type(res) is list:
                    if res[0] is None:
                        return []
                    elif str(type(res[0])) == "<class 'osa.xmltypes.PolygonPlaneIntersection'>":
                        # Result is from MeshPhiIntersection
                        for intersection in res:
                            # res.surfs has entries for every phi
                            vertex_points = Points3D(intersection.vertices,
                                                     coord_sys=tfields.bases.CARTESIAN)
                            vertex_points.transform(tfields.bases.CYLINDER)
                            vertex_points[:, 1].fill(phi)  # phi is correct with rounding precision before. This way it is perfectly correct
                            poincare_points_list.append(vertex_points)
                    else:
                        log.error("Can not handle result list content.")
                elif res is None:
                    log.debug("Result was None. Probably there was no intersection of the mesh with this plane.")
                else:
                    log.error("Result is not of the right type")

                mm_id_container.append(poincare_points_list)
            phi_container.append(mm_id_container)
        return phi_container


class MagneticConfig(Base):
    """
    Object to closely lie above web service MagneticConfig object
    Examples:
        >>> import w7x
        >>> datFileName=w7x.Defaults.Paths.test_dat_file
        >>> cyl = w7x.flt.CylindricalGrid(numR=60, numPhi=101, numZ=10)
        >>> grid = w7x.flt.Grid(cylindrical=cyl)
        >>> m = w7x.flt.MagneticConfig.from_dat_file(datFileName, grid=grid)
        >>> flsType = m.as_input()
        >>> flsType  # doctest: +ELLIPSIS
        (MagneticConfig){
            coils[] = None (PolygonFilament)
            coilsCurrents[] = None (float)
            coilsIds[] = None (int)
            coilsIdsCurrents[] = None (float)
            configIds[] = None (int)
            grid = (Grid){
                       cylindrical = (CylindricalGrid){
                                         RMin = 4.05
                                         RMax = 6.75
                                         ZMin = -1.35
                                         ZMax = 1.35
                                         numR = 60
                                         numZ = 10
                                         PhiMin = None (float)
                                         PhiMax = None (float)
                                         numPhi = 101
                                     }
                       hybrid = None (CylindricalGrid)
                       afsFileName = /afs/ipp-garching.mpg.de/home/d/dboe/exch/test.dat
                       gridField = None (Points3D)
                       fieldSymmetry = 5
                   }
            inverseField = None (bool)
        }

    """
    prop_defaults = {'coils': None,
                    'coilsCurrents': None,
                    'coilsIds': None,
                    'coilsIdsCurrents': None,
                    'configIds': None,
                    'grid': None,
                    'inverseField': None
                    }

    ws_class = "MagneticConfig"

    @classmethod
    def default(cls):
        """
        Standard case with ideal coils
        """
        return cls.from_currents()

    @classmethod
    def from_currents(cls,
                      *currents,
                      **kwargs):
        """
        Factory method for vacuum magnetic field construction with biot-savart

        Args:
            *currents (float):
                first 5 currents -> non planar currents
                next 2 currents -> planar currents
                next 2 currents -> sweep coil currents
            **kwargs:
                unit (str):
                    The currents given have the unit Aw like in the web service
                    input for magnetic configs (see coil_currents method docstring)
                scale (float): For all relative units ('rw', 'r'), the 'scale'
                    attribute is active. The default is
                    w7x.Defaults.MagneticConfig.n_windigs_npcs in 'rw'
                coils_ids: specify the coils by picking their ids from the
                    database. 
                    NOTE: The order of the coils is not arbitrary. The coil ids
                        have to be given in the order:
                            1. 50 non planar coils NPC1-NPC5,NPC1-NPC5,...
                            2. 20 planar coils PCA,PCB,PCA,PCB,...
                            3. 10 sweep coils in the order of the half modules
                                (hm10, hm11,...)
                        Some coils_ids are already compiled into a list in 
                        w7x.Defaults.MagneticConfig.coilsIds

        Examples:
            >>> import w7x
            >>> import numpy as np

            Build a low iota configuration from relative winding currents
            >>> m = w7x.flt.MagneticConfig.from_currents(
            ...     1, 1, 1, 1, 1, 0.23, 0.23, 0.001, 0.001,
            ...     unit='rw')

            Build the same config with any other unit combination
            >>> units = ['rw', 'r', 'Aw', 'A']
            >>> for unit in units:
            ...     for check_unit in units:    
            ...         m_tmp = w7x.flt.MagneticConfig.from_currents(
            ...             *m.coil_currents(unit=unit),
            ...             unit=unit, scale=None)
            ...         assert np.array_equal(m_tmp.coil_currents(check_unit),
            ...                               m.coil_currents(check_unit))

            or with pre-defined configurations
            >>> m_alternative = w7x.flt.MagneticConfig.from_currents(
            ...     *w7x.config.Defaults.MagneticConfig.low_iota_rw,
            ...     unit='rw')

        """
        unit = kwargs.pop('unit', 'rw')
        scale = kwargs.pop('scale', None)
        if unit == 'rw' and scale is None:
            scale = w7x.Defaults.MagneticConfig.scale
        elif unit == 'r' and scale is None:
            scale = w7x.Defaults.MagneticConfig.scale / w7x.Defaults.MagneticConfig.n_windigs_npcs
        if scale is None:
            scale = 1.
        if not 'r' in unit and scale != 1:
            raise ValueError("Scale given for absolute currents.")

        currents = list(currents)
        default_currents = w7x.Defaults.MagneticConfig.default_currents_rw
        if len(currents) < len(default_currents):
            if unit != 'rw' and len(currents) < 5:
                raise ValueError("For all units except 'rw' we expect"
                                 " at least the planar coil currents")
            currents = currents + default_currents[len(currents):]

        '''
        convert to Aw
        '''
        currents = np.array(currents, dtype=float)
        currents *= scale

        if 'w' not in unit:
            currents[:5] *= w7x.Defaults.MagneticConfig.n_windigs_npcs
            currents[5:7] *= w7x.Defaults.MagneticConfig.n_windigs_plcs
            currents[7:9] *= w7x.Defaults.MagneticConfig.n_windigs_scs

        kwargs['coilsIds'] = kwargs.pop('coils_ids', w7x.Defaults.MagneticConfig.coilsIds)
        kwargs['coilsIdsCurrents'] = list(currents[:5]) * 10  # non planar coils
        kwargs['coilsIdsCurrents'] += list(currents[5:7]) * 10  # planar coils
        kwargs['coilsIdsCurrents'] += list(currents[7:]) * 5  # sweep coils
        if not len(kwargs['coilsIds']) == len(kwargs['coilsIdsCurrents']):
            raise ValueError("#Coils: %s, \t#Currents: %s" % (len(kwargs['coilsIds']),
                                                              len(kwargs['coilsIdsCurrents'])))
        kwargs['grid'] = kwargs.pop('grid', Grid())
        return cls(**kwargs)

    @classmethod
    def from_afs_file(cls, filePath, **kwargs):
        """
        set AFS BField file
        Args:
            filePath (str): afs file path
            **kwargs: forwarded to constructor of cls
            
        """
        if 'grid' not in kwargs:
            raise AttributeError("Please specify a grid.")
        # create Grid with afsFileName and hybrid grid if existing.
        kwargs['grid'] = kwargs.pop('grid', Grid())
        # check that file is afs file
        if not filePath.startswith('/afs'):
            raise TypeError('FilePath must be afs file.')
        kwargs['grid'].afsFileName = filePath

        return cls(**kwargs)

    @classmethod
    def from_dat_file(cls, filePathDat,
                      afsExchDir=w7x.Defaults.Paths.afsExchDir, **kwargs):
        """
        Copy file to afs and return the instance with afsFile
        Args:
            see from_afs_file and __init__
        Examples:
            >>> from w7x.flt import MagneticConfig, CartesianGrid, Grid
            >>> datFileName=w7x.Defaults.Paths.test_dat_file
            >>> cyl = CylindricalGrid(numR=60, numPhi=101, numZ=10)
            >>> grid = Grid(cylindrical=cyl)
            >>> m = MagneticConfig.from_dat_file(datFileName, grid=grid)

        """
        log = logging.getLogger()

        filePathDat = tfields.lib.in_out.resolve(filePathDat)
        if filePathDat.startswith('/afs'):
            afsFilePathDat = filePathDat
        else:
            afsFilePathDat = tfields.lib.in_out.resolve(os.path.join(afsExchDir,
                                                        os.path.basename(filePathDat)))

            if filePathDat.startswith('/afs'):
                if not filePathDat == afsFilePathDat:
                    raise ValueError("filePathDat {} is in afs but not the same "
                                     "as afsFilePathDat {}".format((filePathDat,
                                                                    afsFilePathDat)))
            else:
                if os.path.exists(afsFilePathDat):
                    log.info("File {afsFilePathDat} is already existing. "
                             "I will not copy.".format(**locals()))
                else:
                    # Copy file to afs
                    log.info('Copy %s to %s' % (filePathDat, afsFilePathDat))
                    tfields.lib.in_out.cp(filePathDat, afsFilePathDat)

        return cls.from_afs_file(afsFilePathDat, **kwargs)

    def scale_currents(self, scale, unit='Aw'):
        """
        Scale the currents with scale
        """
        if self.coilsIdsCurrents is None:
            raise ValueError("No coil currents set yet.")
        if unit == 'Aw':
            self.coilsIdsCurrents = [c * scale for c in self.coilsIdsCurrents]
        else:
            raise NotImplementedError("Unit {unit} not implemented yet."
                                      .format(**locals()))

    def set_nominal_current(self, nominalCurrent, unit='Aw'):
        """
        Scale the currents to reach the nomianlCurrent
        """
        self.scale_currents(nominalCurrent / self.coilsCurrents[0], unit=unit)

    def coil_currents(self, unit='rw'):
        """
        Args:
            unit (str): what spec
                'rw': relative in Aw (see below)
                'r': relative in A
                'A': the current that is actually applied to the coil set
                'Aw': in A * winding number - the current that is applied if there
                    would be just 1 winding. Non planar coils have 108 windings
                    each, planar coils, 36 and control coils 8 windings each.

        Examples:
            >>> from w7x import MagneticConfig
            >>> import numpy as np
            
            >>> m = MagneticConfig.from_currents(
            ...     1, 1, 1, 1, 1, 0.23, 0.23, 0, 0,
            ...     scale = 15000 * 108)
            >>> assert np.array_equal([round(x, 2) for x in m.coil_currents('rw')],
            ...                       [1.0, 1.0, 1.0, 1.0, 1.0, 0.23, 0.23, 0.0, 0.0])
            >>> assert np.array_equal([round(x, 2) for x in m.coil_currents('r')],
            ...                        [1.0, 1.0, 1.0, 1.0, 1.0, 0.69, 0.69, 0.0, 0.0])
            >>> assert np.array_equal([round(x) for x in m.coil_currents('Aw')],
            ...                       [1620000.0, 1620000.0, 1620000.0,
            ...                        1620000.0, 1620000.0, 372600.0,
            ...                        372600.0, 0.0, 0.0])
            >>> assert np.array_equal([round(x) for x in m.coil_currents('A')],
            ...                       [15000.0, 15000.0, 15000.0, 15000.0,
            ...                        15000.0, 10350.0, 10350.0, 0.0, 0.0])

        """
        npcs = self.coilsIdsCurrents[:5]
        plcs = self.coilsIdsCurrents[50:52]
        scs = self.coilsIdsCurrents[70:72]
        npcs = np.array(npcs)
        plcs = np.array(plcs)
        scs = np.array(scs)
        I_n = npcs[0]
        if unit == 'Aw':
            return list(npcs) + list(plcs) + list(scs)
        if unit == 'A':
            return (
                list(npcs * 1. / w7x.Defaults.MagneticConfig.n_windigs_npcs)
                + list(plcs * 1. / w7x.Defaults.MagneticConfig.n_windigs_plcs)
                + list(scs * 1. / w7x.Defaults.MagneticConfig.n_windigs_scs)
            )
        if unit == 'rw':
            return (
                list(npcs * 1. / I_n)
                + list(plcs * 1. / I_n)
                + list(scs * 1. / I_n)
            )
        if unit == 'r':
            currents = np.array(self.coil_currents('A'))
            return list(currents * 1. / currents[0])

        raise NotImplementedError(unit)

    def geiger_string(self):
        """
        Examples:
            >>> import w7x
            >>> w7x.MagneticConfig.default().geiger_string()
            '1000_1000_1000_1000_+0000_+0000'

        """
        return "{0:-04d}_{1:-4d}_{2:-4d}_{3:-4d}_{4:0=+5d}_{5:0=+5d}" \
                .format(*[int(x * 1000) for x in self.coil_currents()[1:8]])

    def poincare_in_phi_plane(self, phi_list_rad,
                              seeds=None,
                              numPoints=300,
                              errors=None):
        """Calculate poincare points flux surface wise with field line tracer service from the web service.
    
        Args:
            phi_list_rad (list of floats): list of phi in rad
            seeds (PoincareSeeds): seeds object for initial points for field lines. Each seed in seeds will give a surface
            numPoints (int, optional): number of toroidal revolutions per seed = number of points per fluxSurface.
        Returns:
            list of w7x.Points3D instances: poincareFluxSurfaces.
            Each fluxSurface
                        ->length: number of seeds
                        ->meaning: it represents a closed flux surface
                        ->phi0 is attached to the object as a stamp
    
        Raises:
    
        Examples:
            >>> from w7x.flt import MagneticConfig, Points3D
            >>> config = MagneticConfig.default()
            >>> res = config.poincare_in_phi_plane([0.0, 2.0], Points3D([[6.0, 0.0, 0.0]]), 3)
            >>> assert len(res) == 2
            >>> assert res[0].shape == (3, 3)
            >>> assert res[1].shape == (3, 3)
            >>> res2 = config.poincare_in_phi_plane([0.0, 2.0], Points3D([[6.0, 0.0, 0.0]]), 1)
            >>> assert len(res2) == 2
            >>> assert res2[0].shape == (1, 3)
            >>> assert res2[1].shape == (1, 3)
            >>> res3 = config.poincare_in_phi_plane([2.0], Points3D([[6.0, 0.0, 0.0]]), 1)
            >>> assert len(res3) == 1
            >>> assert res3[0].shape == (1, 3)

        """
        log = logging.getLogger()

        if seeds is None:
            log.info("No seeds given. I will build default seeds.")
            seeds = w7x.Defaults.Poincare.seeds

        seeds = Points3D(seeds)
        errors = errors or []

        if not numPoints > 0:
            raise ValueError("numPoints must be greater than 0")
    
        field_line_server = w7x.get_server(w7x.Server.addr_field_line_server)

        # Poincare Task
        task = field_line_server.types.Task()
        task.step = w7x.Defaults.Poincare.stepSize  # parameter controling the accurancy of the calculation.
        task.poincare = field_line_server.types.PoincareInPhiPlane()
        task.poincare.numPoints = numPoints
        task.poincare.phi0 = phi_list_rad  # list of phi in radians or just one phi.
    
        poincareFluxSurfaces = []
        nSuccess = 0
        nFailed = 0
        log.info("Running through Seeds. Tracing the seedPoints for all given phi.")
        for i_seed in range(len(seeds)):
            seed_point = seeds[i_seed:i_seed + 1]
            res = w7x.run_service(field_line_server.service.trace,
                                  seed_point.as_input(),
                                  self.as_input(),
                                  task,
                                  errors=errors)

            if res is None:
                log.warning("Turn %i of %i : fail" % (i_seed + 1, len(seeds)))
                nFailed += 1
                continue
            else:
                nSuccess += 1
                for surf in res.surfs:
                    p = Points3D(surf.points)
                    p.transform(tfields.bases.CYLINDER)
                    p[:, 1].fill(surf.phi0)  # phi is correct with rounding precision before. This way it is perfectly correct
                    poincareFluxSurfaces.append(p)
                log.info("Turn %i of %i : success" % (i_seed + 1, len(seeds)))
        if nFailed > 0:
            log.warning("")
            log.warning("Trace finished with %s succeded and %s failed." % (nSuccess, nFailed))
            log.warning("")
        else:
            log.info("Trace finished with %s succeded and %s failed." % (nSuccess, nFailed))
    
        return poincareFluxSurfaces

    def magnetic_characteristics(self, points3D, taskStepSize=0.2, returnType=list):
        """
        Args:
            points3D (field_line_server.types.Points3D): points to retrieve characteristics from. Give None to take lcfs point
            taskStepSize (float)
            returnType (type): return either list or tfields.TensorFields.
        Examples:
            >>> from w7x.flt import MagneticConfig, Points3D
            >>> config = MagneticConfig.default()
            >>> mchars = config.magnetic_characteristics(Points3D([[6.2, 0., 0.]]))  # This is long lasting.
            >>> assert len(mchars) == 1
            >>> mchar = mchars[0]
            >>> assert mchar.iota < 1
            >>> assert mchar.iota > 0.95
            >>> assert mchar.reff < 0.6
            >>> assert mchar.reff > 0.5
            >>> assert mchar.phi0 == 0.0

        """
        field_line_server = w7x.get_server(w7x.Server.addr_field_line_server)
        # process input points3D
        points3D = Points3D(points3D)
        points3D.transform(tfields.bases.CARTESIAN)

        # define task
        task = field_line_server.types.Task()
        task.step = taskStepSize
        task.characteristics = field_line_server.types.MagneticCharacteristics()
        task.characteristics.axisSettings = field_line_server.types.AxisSettings()

        # run web service
        log = logging.getLogger()
        log.info("Retrieving MagneticCharacteristics with the points given.")
        result = w7x.run_service(field_line_server.service.trace,
                                 points3D.as_input(),
                                 self.as_input(),
                                 task, None, None)  # the None after 'task' can be machine boundary.

        if result is None:
            return None
        if returnType is list:
            return result.characteristics
        elif issubclass(returnType, tfields.TensorFields):
            return returnType(points3D, [[m.iota, m.diota, m.reff, m.dreff, m.phi0, m.theta0]
                                         for m in result.characteristics])

    def iota(self, points3D, taskStepSize=0.2, returnType=list):
        """
        Args: see magnetic_characteristics
        Examples:
            >>> from w7x.flt import MagneticConfig, Points3D
            >>> import tfields
            >>> config = MagneticConfig.default()
            >>> iotas = config.iota(Points3D([[6.2, 0., 0.]]))  # This is long lasting.
            >>> assert iotas[0] > 0.95
            >>> assert iotas[0] < 1.0

            # >>> config.iota(Points3D([[ 6.2, 0., 0.]]),
            # ...                returnType=tfields.TensorFields)  # This is long lasting.
            # points: [[ 6.2  0.          0.        ]]
            # scalars: [[ 0.98849176]]

        """
        magnetic_characteristics = self.magnetic_characteristics(points3D, taskStepSize, returnType)
        if returnType is list:
            return [charact.iota for charact in magnetic_characteristics]
        elif issubclass(returnType, tfields.TensorFields):
            magnetic_characteristics.dropScalars(
                range(1, len(magnetic_characteristics.scalars.T)))
            return magnetic_characteristics

    def find_axis_at_phi(self, phi=0, size=w7x.Defaults.Poincare.stepSize, settings=None):
        """
        Args:
            phi (float): phi in rad
            size (float): step size
            settings (field_line_server.types.AxisSettings())
        Returns:
            Points3D: magnetic axis position at phi=<phi>
        """
        field_line_server = w7x.get_server(w7x.Server.addr_field_line_server)
        if settings is not None:
            settings = settings.as_input()
        else:
            settings = field_line_server.types.AxisSettings(1)
        logging.getLogger().info("Finding axis at phi.")
        result = w7x.run_service(field_line_server.service.findAxisAtPhi,
                                phi,
                                size,
                                self.as_input(),
                                settings)
        return Points3D(result.points, coord_sys=tfields.bases.CARTESIAN)

    def plot_poincare(self, phi=0, seeds=None, numPoints=300, errors=None, **kwargs):
        """
        Plot a poincare plot
        Args:
            phi (float): phi in rad
            seeds (Points3D): seed points. If None, take default seeds
        """
        surfs = self.poincare_in_phi_plane([phi], seeds=seeds,
                                           numPoints=numPoints, errors=errors)
        return w7x.plot_poincare_surfaces(surfs, **kwargs)


class Polygon(Base):
    """
        element.vertices gives you the three points numbers to a triangle. This is normally refered to as face
    """

    ws_class = "Polygon"
    prop_defaults = {
        'vertices': None
    }


class MeshedModel(Base):
    """
    Args:
        multiple ways:
            vertices (list)
            faces (list)

            - or -

            group from ObjFile

            - or -

            tfields.Mesh3D object
    Attributes:
        nodes (Points3D): = vertices (coordinates) of the points.
        elements (list[Polygon]): = faces (always three indices of points for a triangle). Starting at 1 here
    Examples:
        use with Mesh3D as inp
        >>> from w7x.flt import MeshedModel
        >>> import tfields
        >>> m = tfields.Mesh3D([[1,2,3], [3,3,3], [0,0,0], [5,6,7]],
        ...                    faces=[[0, 1, 2], [1, 2, 3]])
        >>> mm = MeshedModel(m)

        Get the osa type, in this case for field line server
        >>> fls = mm.as_input()

        return Mesh3D works
        >>> bool((m == mm.as_Mesh3D()).all())
        True

        create with meshed Model from fls works
        >>> m2 = MeshedModel(fls).as_Mesh3D()
        >>> assert tfields.Points3D(m2).equal(
        ...     [[ 1.,  2.,  3.],
        ...      [ 3.,  3.,  3.],
        ...      [ 0.,  0.,  0.],
        ...      [ 5.,  6.,  7.]])
        >>> assert tfields.Tensors(m2.faces).equal([[0, 1, 2], [1, 2, 3]])

    """

    ws_class = "MeshedModel"
    prop_defaults = {
        'nodes': None,
        'elements': None,
        'nodesIds': None,
        'elementsIds': None
    }

    def __init__(self, *args, **kwargs):
        log = logging.getLogger()
        args = list(args)
        if len(args) > 1:
            log.error(" Implementation did not work.")
            raise NotImplementedError(" Implementation with args %s not yet implemented!" % args)
        elif len(args) == 1 and issubclass(args[0].__class__, tfields.Mesh3D):
            mesh3D = args.pop(0)
            nodes = Points3D(mesh3D)
            faces = mesh3D.faces + 1
            kwargs['nodes'] = kwargs.pop('nodes', nodes)
            kwargs['elements'] = kwargs.pop('elements',
                                            [Polygon(vertices=face) for face in faces])
        super(MeshedModel, self).__init__(*args, **kwargs)

    @classmethod
    def from_mm_id(cls, mm_id):
        compDBServer = w7x.get_server(w7x.Server.addr_components_db)
        meshedModelFLSType = compDBServer.service.getComponentData(mm_id)[0]
        return cls(meshedModelFLSType)

    def as_Mesh3D(self):
        faces = np.array([pol.vertices for pol in self.elements])
        faces -= 1
        return tfields.Mesh3D(Points3D(self.nodes), faces=faces)


class Run(object):
    """
    Container class that knows everything important about the w7x setup you want to use.
    Note:

    Args:
        magnetic_config (MagneticConfig):
        machine (Machine):
    Attributes:

    Examples:

        >>> from w7x.flt import Run
        >>> config = Run()

    """
    def __init__(self, magnetic_config=None, machine=None):
        self.magnetic_config = magnetic_config
        self.machine = machine

    @property
    def magnetic_config(self):
        """
        (w7x.flt.MagneticConfig): magnetic configuration of the run 
        """
        return self._magnetic_config

    @magnetic_config.setter
    def magnetic_config(self, magnetic_config):
        if magnetic_config is None:
            magnetic_config = MagneticConfig.default()
        else:
            magnetic_config = MagneticConfig(magnetic_config)
        self._magnetic_config = magnetic_config

    @property
    def machine(self):
        """
        (w7x.flt.Machine): machine geometry of the run 
        """
        return self._machine

    @machine.setter
    def machine(self, machine):
        if machine is None:
            machine = Machine.default()
        else:
            Machine(machine)
        self._machine = machine

    def find_lcfs(self, step=0.001, settings=None, max_time=None):
        """
        Examples:
            >>> import w7x
            >>> run = w7x.flt.Run()
            >>> lcfs_point = run.find_lcfs(0.1)  # This is long lasting.
            >>> assert lcfs_point[0, 0] > 6.2
            >>> assert lcfs_point[0, 0] < 6.21

        """
        field_line_server = w7x.get_server(w7x.Server.addr_field_line_server)
        if settings is None:
            settings = field_line_server.types.LCFSSettings(1)
        else:
            settings = settings.as_input()
            
        logging.getLogger().info("Retrieving Point on Last closed flux surface")
        lCFSPoint = w7x.run_service(field_line_server.service.findLCFS,
                                   step,
                                   self.magnetic_config.as_input(),
                                   self.machine.as_input(),
                                   settings,
                                   max_time=max_time)  # find last closed flux surface
        return Points3D([[lCFSPoint.x, lCFSPoint.y, lCFSPoint.z]])

    def line_phi_span(self, points, phi, step=0.01):
        """
        Args:
            points (w7x.flt.Points3D)
            phi (float): phi in radian
            step (flota): step width of the tracer task
        """
        log = logging.getLogger()
        points = Points3D(points)
        field_line_server = w7x.get_server(w7x.Server.addr_field_line_server)

        config = self.magnetic_config.as_input()
        
        task = field_line_server.types.Task()
        task.step = step
        task.linesPhi = field_line_server.types.LinePhiSpan()
        task.linesPhi.phi = phi

        log.info("starting line tracing ...")
        res = field_line_server.service.trace(points.as_input(),
                                            config,
                                            task,
                                            self.machine.as_input())
        log.info("... done")
        return [Points3D(line.vertices) for line in res.lines]

    def line_phi(self, points, phi, phi_tolerance=1. / 180 * np.pi, step=0.01):
        """
        Get the crossection of the field lines starting at <points> at exactly one
        phi (exact within the tolerance given by <phi_tolerance>).
        You can specify the direction of tracing by switching the bool
        self.magnetic_config.inverseField
        Args:
            points (w7x.Points3D): starting points of tracing
            phi (float): phi in radian
        Returns:
            w7x.Points3D: piercing points of the lines,
                starting at <points> at exactly one
                phi (exact within the tolerance given by <phi_tolerance>).
                The return value will be empty an empty seuqence of Points3D,
                if the step size was not small enough.
        """
        lines = self.line_phi_span(points, phi, step=step)
        container = []
        for line in lines:
            line.transform(tfields.bases.CYLINDER)
            inds = line.where_phi_between(phi - phi_tolerance, phi +
                                          phi_tolerance)
            line = line[inds[0][-1:]]
            line[:, 1] = phi
            container.append(line)
        return Points3D.merged(*container)

    def line_diffusion(
            self,
            start_points=w7x.Defaults.Diffusion.nRevolutions,
            diffusion=w7x.Defaults.Diffusion.diffusion,
            velocity=w7x.Defaults.Diffusion.velocity,
            size=w7x.Defaults.Diffusion.stepSize,
            mean_free_path=w7x.Defaults.Diffusion.meanFreePath,
            additiona_shifts=None,
            start_point_shift=w7x.Defaults.Diffusion.startPointShift,
            **kwargs):
        """
        Args:
            start_points(int | str | Points3D):
                int: number of points to trace
                str: path to full start point set that should be traced
                Points3D: full start point set that should be traced
            diffusion (float): perp. diffusion coefficient
        Returns:
            tuple:
                w7x.flt.ConnectionLength:
                w7x.flt.ComponentLoad:
                w7x.flt.Points3D: start points lying on lcfs
        Examples:
            >>> import w7x
            >>> import tfields

            Triangle approximating the bean plane
            >>> mesh = tfields.Mesh3D([[5.4,0,-1], [5.4,0,1], [6.5,0,0]],
            ...                       faces=[[0,1,2]], coord_sys='cylinder')

            Machine constitued from bean plane triangle and divertor
            >>> machine = w7x.flt.Machine(meshedModels=[mesh],
            ...                           meshedModelsIds=[165])
            >>> run = w7x.flt.Run(machine=machine)

            Initial point starting very close to the triangle
            >>> initial_points = w7x.flt.Points3D([[6.0,0.0001,0]],
            ...                                   coord_sys='cylinder')
            >>> conn_len, comp_load, start_points = run.line_diffusion(
            ...     initial_points)
            >>> assert initial_points.equal(start_points,atol=1e-9)

            As expected, the triangle was hit only
            >>> conn_len.parts
            [0, 0]

            The mm_id 1000 is added automatically
            >>> conn_len.mm_ids
            [1000, 165]

        """
        log = logging.getLogger()
        field_line_server = w7x.get_server(w7x.Server.addr_field_line_server)
        if additiona_shifts is None:
            additiona_shifts = [0.00, 0.01, 0.01, 0.01, 0.01, 0.01, 0.1]

        nStart = None
        launchPointsPath = None
        if type(start_points) is int:
            nStart = start_points
            start_points = None
        elif type(start_points) is str:
            launchPointsPath = start_points
            start_points = None
        elif isinstance(start_points, tfields.Points3D):
            nStart = start_points.shape[0]
            if not isinstance(start_points, Points3D):
                start_points = Points3D(start_points)

        # define all setting inputs for diffusion
        fldTask = field_line_server.types.Task()
        fldTask.step = size
        line_diffusion = field_line_server.types.LineDiffusion()
        line_diffusion.diffusionCoeff = diffusion
        line_diffusion.freePath = mean_free_path
        line_diffusion.velocity = velocity
        fldTask.diffusion = line_diffusion
        fldTask.connection = field_line_server.types.ConnectionLength()
        fldTask.connection.limit = kwargs.pop('connectionLimit', 3000000.0)
        fldTask.connection.returnLoads = True
        config = self.magnetic_config.as_input()
        machine = self.machine.as_input()
        log.info("Machine flsType: \n{machine}".format(**locals()))
        log.info("Config flsType: \n{config}".format(**locals()))

        # check start_points validity
        if start_points is None and launchPointsPath is None:
            log.info("Creating random start lcfs_init_points on last closed flux surface")
            lcfs_init_points = self.find_lcfs()

            """
            remove small value to be save to be inside
            offset changed on 2.11 from 0.001 to 0.02. It shows, that the
            computation time increase due to longer diffusion path
            is waaay less than repeating a whole shot (at least for D=1m^s/s).
            """
            lcfs_init_points[:, 0] -= 0.02 + start_point_shift

        for iShift, additionalShift in enumerate(additiona_shifts):
            if iShift == 0 and start_points is not None:
                # before start_points could have been set by fld it has been
                # given
                log.info("Start points were given.")
            elif launchPointsPath is None:
                lcfs_init_points[:, 0] -= additionalShift
                log.info(" Startpoint: {lcfs_init_points}".format(**locals()))

                traceTask = field_line_server.types.Task()
                traceTask.step = 0.5
                line = field_line_server.types.LineTracing()
                line.numSteps = nStart - 1
                traceTask.lines = line

                log.info("Trace this point " + str(line.numSteps) + "-times.")
                res = w7x.run_service(field_line_server.service.trace,
                                     lcfs_init_points.as_input(), config, traceTask, machine, max_time=None)

                start_points = res.lines[0].vertices

                # END  creating random start_points on last closed flux surface
            else:
                log.info("Reading launch points")
                start_points = Points3D.load(launchPointsPath)

            # force start_points to CARTESIAN and check dimension
            start_points = w7x.Points3D(start_points)
            start_points.transform(tfields.bases.CARTESIAN)
                
            log.info("Line diffusion forwards.")
            # max_time could be something like int(round(line.numSteps / 4000. * 2000)))
            resForward = w7x.run_service(field_line_server.service.trace,
                                         start_points.as_input(),
                                         config,
                                         fldTask,
                                         machine,
                                         max_time=None)
            resForwardClass = ConnectionLength(resForward.connection)
            if len(resForwardClass) == nStart:
                log.info("Length %s accepted!" % len(resForwardClass))
                if launchPointsPath is None:
                    start_points = Points3D(start_points)
                break
            elif launchPointsPath is not None:
                log.warning("LaunchPointsPath is given but number of HitPoints"
                            "is not meeting requested number.")
                break
            elif iShift == len(additiona_shifts) - 1:
                log.error("Also after shift of %s number of H" %
                        sum(additiona_shifts))
                raise ValueError("Also after shift of %s number of H" %
                        sum(additiona_shifts))
            else:
                log.warning("Restart the forward tracing with a new lCFSInitPoint offset of {0}"
                            "since the number of output points ({1}) does not meet"
                            "opts.nRevolutions({2})".format(sum(additiona_shifts[:iShift + 2]),
                                                            len(resForwardClass),
                                                            nStart))

        log.info("Line diffusion backwards.")
        config.inverseField = True
        # max_time could be something like int(round(line.numSteps / 4000. * 2000)))
        resInvers = w7x.run_service(field_line_server.service.trace,
                                   start_points.as_input(),
                                   config,
                                   fldTask,
                                   machine,
                                   max_time=None)

        connection_length = ConnectionLength(resForward.connection +
                                             resInvers.connection)
        connection_length.mm_ids = self.machine.mm_ids

        component_load = ComponentLoad(resForward.loads.components +
                                       resInvers.loads.components)
        component_load.mm_ids = self.machine.mm_ids
        return connection_length, component_load, start_points

    def connection_length(self, points, **kwargs):
        """
        Args:
            points: Points3D
            **kwargs:
                limit (float): lenght limit of line tracing
                step (float): step size of line tracing
                diffusion (field_line_server.type.LineDiffusion()): add diffusion
                    to the tracing
        Returns:
            ConnectionLength
        """
        log = logging.getLogger()

        step = kwargs.pop('step', 5e-3)
        limit = kwargs.pop('limit', 2.0e4)
        diffusion = kwargs.pop('diffusion', None)

        points.transform(tfields.bases.CARTESIAN)
        
        field_line_server = w7x.get_server(w7x.Server.addr_field_line_server)
        task = field_line_server.types.Task()
        task.step = step
        con = field_line_server.types.ConnectionLength()
        con.limit = limit
        con.returnLoads = False
        task.connection = con
        
        if diffusion:
            task.diffusion = diffusion

        log.info("Start tracing ...")
        res = w7x.run_service(field_line_server.service.trace,
                             points.as_input(),
                             self.magnetic_config.as_input(),
                             task,
                             self.machine.as_input())
        connection_length = ConnectionLength(res.connection)
        connection_length.mm_ids = self.machine.mm_ids
        return connection_length

    def plot_poincare(self, phi, seeds=None, **kwargs):
        """
        forward to self.magnetic_config.plot_poincare and
        self.machine.plot_poincare
        """
        artists = []
        if self.magnetic_config is not None:
            artists.extend(self.magnetic_config.plot_poincare(phi, seeds=seeds,
                                                              **kwargs))
        if self.machine is not None:
            artists.extend(self.machine.plot_poincare(phi, **kwargs))


if __name__ == "__main__":
    import doctest
    # doctest.run_docstring_examples(Run.line_diffusion, globals())
    # quit()
    doctest.testmod()
    # doctest.run_docstring_examples(ConnectionLength, globals())
    # doctest.run_docstring_examples(MagneticConfig.coil_currents, globals())
    # doctest.run_docstring_examples(MagneticConfig.from_currents, globals())
    # server = w7x.get_server(w7x.Server.addr_coils_db)
    # for ci in w7x.Coils.idealNonPlanarCoilIds:
    #     print ci
    #     print server.service.getCoilInfo(ci)
