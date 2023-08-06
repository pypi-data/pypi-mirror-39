from ..tecutil import sv, XYZPosition
from .. import session


class LightSource(session.Style):
    def __init__(self, plot):
        self.plot = plot
        super().__init__(sv.GLOBALTHREED, uniqueid=self.plot.frame.uid)

    @property
    def background_light(self):
        return self._get_style(float, sv.BACKGROUNDLIGHT)

    @background_light.setter
    def background_light(self, value):
        self._set_style(float(value), sv.BACKGROUNDLIGHT)

    @property
    def intensity(self):
        return self._get_style(float, sv.INTENSITY)

    @intensity.setter
    def intensity(self, value):
        self._set_style(float(value), sv.INTENSITY)

    @property
    def specular_intensity(self):
        if self._get_style(bool, sv.INCLUDESPECULAR):
            return self._get_style(int, sv.SPECULARINTENSITY)
        else:
            return 0

    @specular_intensity.setter
    def specular_intensity(self, value):
        if not value:
            self._set_style(False, sv.INCLUDESPECULAR)
        else:
            self._set_style(True, sv.INCLUDESPECULAR)
            self._set_style(int(value), sv.SPECULARINTENSITY)

    @property
    def specular_shininess(self):
        return self._get_style(int, sv.SPECULARSHININESS)

    @specular_shininess.setter
    def specular_shininess(self, value):
        self._set_style(int(value), sv.SPECULARSHININESS)

    @property
    def surface_color_contrast(self):
        return self._get_style(float, sv.SURFACECOLORCONTRAST)

    @surface_color_contrast.setter
    def surface_color_contrast(self, value):
        self._set_style(float(value), sv.SURFACECOLORCONTRAST)

    @property
    def direction(self):
        return self._get_style(XYZPosition, sv.XYZDIRECTION)

    @direction.setter
    def direction(self, value):
        self._set_style(XYZPosition(value), sv.XYZDIRECTION)

    @property
    def use_gourad_for_contour_flood(self):
        self._get_style(bool, sv.FORCEGOURADFOR3DCONTFLOOD)

    @use_gourad_for_contour_flood.setter
    def use_gourad_for_contour_flood(self, value):
        self._set_style(bool(value), sv.FORCEGOURADFOR3DCONTFLOOD)

    @property
    def use_paneled_for_cell_flood(self):
        self._get_style(bool, sv.FORCEPANELEDFOR3DCELLFLOOD)

    @use_paneled_for_cell_flood.setter
    def use_paneled_for_cell_flood(self, value):
        self._set_style(bool(value), sv.FORCEPANELEDFOR3DCELLFLOOD)
