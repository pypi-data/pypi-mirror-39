"""
specific methods for poincare plotting
"""
import tfields


def plot_poincare_surfaces(poincareSurfaces, **kwargs):
    """
    Args:
        poincareSurfaces (list of Points3D): each Points3D instance is one
            fieldLine followed around the torus
    """
    methodName = kwargs.pop('methodName', 'scatter')
    po = tfields.plotting.PlotOptions(kwargs)
    rMin = po.pop('rMin', 4.0)
    rMax = po.pop('rMax', 6.6)
    zMin = po.pop('zMin', -1.3)
    zMax = po.pop('zMax', +1.3)
    phiRad = po.pop('phiRad', None)

    po.set_default('yAxis', 2)
    po.set_default('labelList', ['r (m)', r'$\phi$ (rad)', 'z (m)'])
    if methodName is 'scatter':
        po.set_default('marker', '.')
        po.set_default('s', 1)
    po.set_default('methodName', methodName)
    color_given = True
    if 'color' not in po.plotKwargs:
        color_given = False
        cmap, _, _ = po.getNormArgs()
        color_cycle = tfields.plotting.color_cycle(cmap, len(poincareSurfaces))
    elif isinstance(po.get('color'), list):
        color_given = False  # hack to set the color from list
        color_cycle = iter(po.get('color'))
    artists = []
    for i, surfacePoints in enumerate(poincareSurfaces):
        with surfacePoints.tmp_transform(tfields.bases.CYLINDER):
            phiSurface = surfacePoints[:, 1]
            if phiRad is None:
                phiRad = phiSurface[0]
            if bool((phiSurface != phiRad).any()):
                continue
            if not color_given:
                po.set('color', next(color_cycle))
            artists.append(surfacePoints.plot(axis=po.axis, **po.plotKwargs))
    tfields.plotting.set_aspect_equal(po.axis)
    po.axis.set_xlim(rMin, rMax)
    po.axis.set_ylim(zMin, zMax)
    return artists


def plot_poincare_geometries(geometries, **kwargs):
    po = tfields.plotting.PlotOptions(kwargs)
    po.set_default('methodName', 'plot')
    po.set_default('lw', 1)
    artists = []
    for p in range(len(geometries)):
        for g in range(len(geometries[p])):
            artists.extend(plot_poincare_surfaces(geometries[p][g], axis=po.axis,
                                                **po.plotKwargs)) 
    return artists
