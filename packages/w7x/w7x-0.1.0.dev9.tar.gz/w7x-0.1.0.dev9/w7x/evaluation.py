import tfields
import w7x
import joblib
import pathlib
import os
import re
import sys
import importlib
import numpy as np
from scipy.stats import poisson
try:
    import cPickle as pickle
except ImportError:
    import pickle


memory = joblib.Memory(cachedir='/tmp/joblib')


def n_hits_from_load(q, n_tot, area, p_conv):
    """
    Args:
        q(float) heat load
    """
    p_conv *= 1. / 10  # correct for mapping all divertors to one
    return int(round((1. * q * n_tot * area) / p_conv))


def load_from_n_hits(n_hits, n_tot, area, p_conv):
    """
    Args:
        q(float) heat load
    """
    p_conv *= 1. / 10  # correct for mapping all divertors to one
    return (n_hits * p_conv) * 1. / (n_tot * area)


def prob_n_hits_lt_n_des(n_hits_list, n_des_list):
    """
    P(n_hits < n_des | p_conv, n_tot, q_design)
    """
    tile_probs = []
    for n_hits, n_des in zip(n_hits_list, n_des_list):
        n_hits = int(np.round(n_hits))
        p = poisson.cdf(n_des, n_hits)
        tile_probs.append(float(p))
    return tile_probs


@memory.cache
def upper_half(mm_id):
    from sympy.abc import z
    return w7x.flt.MeshedModel.from_mm_id(mm_id).as_Mesh3D().cut(z>0)


class TracerEvaluator(object):
    main_mm_id = None
    mm_ids = None
    def __init__(self):
        self.setup()
        self.clear()

    def setup(self):
        self._mesh = None
        self._design_loads = None
        self._design_loads_local = None
        self._design_loads_average = None
        self._areas = None
        self._areas_local = None
        self._areas_average = None
        self._n_tot = None
        self._p_conv = None

    def clear(self):
        self._conn_len = None
        self._hits = None
        self._n_crits = {}
        self._n_hits = None
        self._n_hits_local = None
        self._n_hits_average = None

    @staticmethod
    def from_loader(loader_file_dir):
        loader_file_dir = pathlib.Path(os.path.abspath(loader_file_dir))
        sys.path.append(str(loader_file_dir.parent))
        module = importlib.import_module('{loader_file_dir.name}.loader'
                                         .format(**locals()))
        evaluator = module.TracerEvaluator()
        return evaluator

    @property
    def connection_length(self):
        """
        w7x.flt.ConnectionLenght: Result of a field line tracer diffusion
            process. It contains the hit points (connection_length.hits).
        """
        if self._conn_len is None:
            raise ValueError("connection_length not set")
        return self._conn_len

    @connection_length.setter
    def connection_length(self, conn_len):
        self.clear()
        self._conn_len = conn_len

    @property
    def hits(self):
        """
        hit points in upper module one.
        when setting the hit points, we take care of the mapping to upper module
        one.
        """
        if self._hits is None: 
            if self.mm_ids is None:
                raise NotImplementedError("mm_ids not set")
            hits = self.connection_length.hits(*self.mm_ids)
            self.hits = hits
        return self._hits

    @hits.setter
    def hits(self, hits):
        self.clear()
        hits = hits.copy()
        hits.to_segment_one(mirror_z=True)  # map to upper mesh in module 1
        self._hits = hits

    @property
    def design_loads(self):
        if self._design_loads is None:
            raise ValueError("Design loads not set")
        return self._design_loads

    @design_loads.setter
    def design_loads(self, values):
        self._design_loads = values

    @property
    def design_loads_local(self):
        if self._design_loads_local is None:
            raise ValueError("Design loads not set")
        return self._design_loads_local

    @design_loads_local.setter
    def design_loads_local(self, values):
        self._design_loads_local = values

    @property
    def design_loads_average(self):
        if self._design_loads_average is None:
            raise ValueError("Design loads not set")
        return self._design_loads_average

    @design_loads_average.setter
    def design_loads_average(self, values):
        self._design_loads_average = values

    @property
    def areas(self):
        if self._areas is None:
            raise ValueError("Areas not set")
        return self._areas

    @areas.setter
    def areas(self, values):
        self._areas = values

    @property
    def areas_local(self):
        if self._areas_local is None:
            raise ValueError("areas_local not set")
        return self._areas_local

    @areas_local.setter
    def areas_local(self, values):
        self._areas_local = values

    @property
    def areas_average(self):
        if self._areas_average is None:
            raise ValueError("areas_average not set")
        return self._areas_average

    @areas_average.setter
    def areas_average(self, values):
        self._areas_average = values

    @property
    def mesh(self):
        if self._mesh is None:
            raise ValueError("Mesh not set")
        return self._mesh

    @mesh.setter
    def mesh(self, value):
        self._mesh = value

    @property
    def n_hits(self):
        """
        Number of hits per section defined by the evaluator.
        This can be calculated automatically if self.hits or 
        self.connection_length has been set. 
        If the values of n_hits have been calculated before, you can also set
        it. Be aware, that we clear all attributes, if n_hits is set by the
        user.
        """
        if self._n_hits is None:
            self._n_hits = self._eval_n_hits()
        return self._n_hits

    @n_hits.setter
    def n_hits(self, n_hits):
        self.clear()
        self._n_hits = n_hits

    @property
    def n_hits_local(self):
        if self._n_hits_local is None:
            raise ValueError("n_hits_local not set")
        return self._n_hits_local

    @n_hits_local.setter
    def n_hits_local(self, n_hits):
        self.clear()
        self._n_hits_local = n_hits

    @property
    def n_hits_average(self):
        if self._n_hits_average is None:
            raise ValueError("n_hits_average not set")
        return self._n_hits_average

    @n_hits_average.setter
    def n_hits_average(self, n_hits):
        self.clear()
        self._n_hits_local = n_hits

    def _eval_n_hits(self):
        raise NotImplementedError()

    @property
    def n_tot(self):
        if self._n_tot is None:
            raise ValueError()
        return self._n_tot

    @n_tot.setter
    def n_tot(self, value):
        self._n_tot = value
        self._n_crits = {}

    @property
    def p_conv(self):
        if self._p_conv is None:
            raise ValueError("p_conv is not set")
        return self._p_conv

    @p_conv.setter
    def p_conv(self, value):
        if self._n_tot is None:
            raise ValueError("Please set n_tot first")
        self._n_crits = {}
        self._p_conv = value

    def n_crits(self, variant='local'):
        if variant not in self._n_crits:
            if variant == 'local':
                n_crits = []
                for area, q_crit in zip(self.areas_local, self.design_loads_local):
                    n_crit = n_hits_from_load(
                        q_crit,
                        self.n_tot,
                        area,
                        p_conv=self.p_conv)
                    n_crits.append(n_crit)
                self._n_crits[variant]= n_crits
            else:
                raise NotImplementedError()
        return self._n_crits[variant]
        
    def prob_n_hits_lt_n_des_local(self):
        """
        P(n_hits < n_des | p_conv, n_tot)
        """
        return prob_n_hits_lt_n_des(self.n_hits_local, self.n_crits('local'))

    def n_hits_lt_n_des_local(self):
        """
        n_hits <= n_des
        """
        return self.n_hits_local <= self.n_crits('local')


class TileBasedTracerEvaluator(TracerEvaluator):
    reshape = (-1, 12)
    def setup(self):
        super(TileBasedTracerEvaluator, self).setup()
        self._box_search_tree = None
        self._box_search_tree_path = None
        self._templates = None

    def clear(self):
        super(TileBasedTracerEvaluator, self).clear()
        self._mesh_hits = None

    @property
    def box_search_tree(self):
        if self._box_search_tree is None:
            if os.path.exists(self._box_search_tree_path):
                with open(self._box_search_tree_path, 'rb') as f:
                    self._box_search_tree = pickle.load(f)
            else:
                tree = tfields.bounding_box.Searcher(self.mesh)
                if self._box_search_tree_path is not None:
                    with open(self._box_search_tree_path, 'wb') as f:
                        pickle.dump(tree, f)
                self._box_search_tree = tree

        return self._box_search_tree 

    @property
    def mesh_hits(self):
        """
        tfields.Tensors that can be used as map field for self.mesh
        """
        if self._mesh_hits is None:
            # with tfields.lib.log.timeit('old'):
            #     mesh_hits = tfields.Tensors(self.mesh.in_faces(self.hits, delta=None))
            # with tfields.lib.log.timeit('new'):
            mesh_hits = tfields.Tensors(self.box_search_tree.in_faces(self.hits, delta=None))
            mesh_hits = tfields.Tensors(mesh_hits.sum(axis=0))
            self.mesh_hits = mesh_hits
        return self._mesh_hits

    @mesh_hits.setter
    def mesh_hits(self, mesh_hits):
        self._mesh_hits = mesh_hits

    @property
    def templates(self):
        if self._templates is None:
            raise ValueError("templates not set")
        return self._templates

    def _tiles(self):
        """
        Map the mesh to a tile geometry with the template
        provided for this
        """
        # convert to hits per area
        mesh_hits = self.mesh_hits / self.mesh.triangles().areas()
        self.mesh.maps[0].fields.append(mesh_hits)

        tiles = []
        for template in self.templates:
            tile = self.mesh.cut(template)
            if len(tile.maps) > 0 and len(tile.maps[0].fields) > 0:
                # convert hits per area back to hits. You will get fractions of
                # hits now.
                areas = tile.triangles().areas()
                areas[np.isnan(areas)] = 0.
                tile.maps[0].fields[0] *= areas
            tiles.append(tile)
        self.mesh.maps[0].fields = []
        return tiles

    def _eval_n_hits(self):
        tiles = self._tiles()
        n_hits = []
        for tile in tiles:
            if len(tile.maps) == 0:
                n = 0.
            else:
                n = float(tile.maps[0].fields[0].sum()) 
            n_hits.append(n)
        return n_hits


class SearchingSphereTracerEvaluator(TracerEvaluator):
    """
    Examples:
        Saving hits in blender manner:
            con_l = ...
            evaluator = w7x.evaluation.SearchingSphereTracerEvaluator()
            evaluator.connection_length = con_l
            mm_ids = getattr(w7x.MeshedModelsIds, 'baffle')
            evaluator.mm_ids = mm_ids

            radius = 0.056
            evaluator.radius = radius
            print(evaluator.n_hits)  # this line is necessary, so that n_hits is
            # calculated

            sphere = tfields.Mesh3D.grid((radius, radius, 1),
                                         (-np.pi, np.pi, 12),
                                         (-np.pi / 2, np.pi / 2, 12),
                                         coord_sys='spherical')
            sphere.transform('cartesian')
            for i in range(3):
                sphere[:, i] += evaluator.center[i]
            sphere.save('~/tmp/center.obj')

            oktaeder_radius = 0.001
            oktaeder = tfields.Mesh3D.grid((oktaeder_radius, oktaeder_radius, 1),
                                           (-np.pi, np.pi, 5),
                                           (-np.pi / 2, np.pi / 2, 3),
                                           coord_sys='spherical')
            oktaeder.transform('cartesian')
            point_meshes = []
            for point in evaluator.hits:
                big_point = oktaeder.copy()
                for i in range(3):
                    big_point[:, i] += point[i]
                point_meshes.append(big_point)
            point_meshes = tfields.Mesh3D.merged(*point_meshes) 
            point_meshes.save('~/tmp/hit_points.obj')
    """
    def setup(self):
        super(SearchingSphereTracerEvaluator, self).setup()
        self._radius = None

    def clear(self):
        super(SearchingSphereTracerEvaluator, self).clear()
        self.center = None

    @property
    def radius(self):
        if self._radius is None:
            raise ValueError("radius not set")
        return self._radius

    @radius.setter
    def radius(self, radius):
        self._radius = radius

    @property
    def areas(self):
        """
        Segment areas
        """
        return [np.pi * self.radius**2]

    @areas.setter
    def areas(self, areas):
        raise ValueError("Not allowed to set the radius directly")

    def _eval_n_hits(self):
        if len(self.hits) == 0:
            self.center = [np.nan] * 3
            return [0]
        epsilon_neighbourhoods = self.hits.epsilon_neighbourhood(self.radius)
        n_in_sphere = [v.shape[0] for v in epsilon_neighbourhoods]
        max_index = n_in_sphere.index(max(n_in_sphere))
        self.center = self.hits[max_index]
        n_hits = n_in_sphere[max_index]
        return [n_hits]

    def plot(self, value, **kwargs):
        axis = kwargs.pop('axis', tfields.plotting.gca(2))
        artist = axis.text(0.5, 0.5, value)
        return artist

    @property
    def areas_local(self):
        return self.areas

    @property
    def n_hits_local(self):
        self._n_hits_local = self.n_hits
        return super(SearchingSphereTracerEvaluator, self).n_hits_local
