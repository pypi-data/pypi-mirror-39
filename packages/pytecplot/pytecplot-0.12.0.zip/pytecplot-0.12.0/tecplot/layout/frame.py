from builtins import str

import logging

from contextlib import contextmanager
from ctypes import byref, c_void_p, cast
from numbers import Number
from six import string_types

from ..tecutil import _tecutil
from ..constant import *
from ..exception import *
from .. import annotation, constant, plot, session, tecutil
from ..tecutil import (IndexSet, StringList, XYPosition,
                       check_arglist_argtypes, flatten_args, lock,
                       lock_attributes, sv)


log = logging.getLogger(__name__)


@lock_attributes
class Frame(object):
    """`Frame` object within a `Page`, holding onto a `Dataset` and a `Plot`.

    Parameters:
        uid (`int`, optional): This must be a *valid* unique ID
            number pointing internally to a Frame object or `None`. A new
            `Frame` is created if set to `None`. (default: `None`)
        page (`Page`, optional): The destination `Page` of this newly
            created `Frame`. If `None`, the currently active `Page` is used.
            (default: `None`)

    Warning:
        Though it is possible to create a `Frame` object using the
        constructor, it is usually sufficient to obtain a frame through
        `tecplot.active_frame()` or `Page.frame()`. One can also create a
        `Frame` using a `Page` handle with `Page.add_frame()`.

    The concept of the `Frame` is central to understanding the
    |Tecplot Engine|. The `Frame` is what connects a `Dataset` to a `Plot`
    handle from which one manipulates the desired image as well as accessing
    the attached data:

    .. code-block:: python

        import tecplot

        frame = tecplot.active_frame()

        # will print: 'Frame "Frame 001"'
        print(frame)
    """

    page = None
    """The `Page` containing this Frame.

    This provides access to the parent `Page`:

    .. code-block:: python

        import tecplot

        frame = tecplot.active_frame()
        page = frame.page

        # Will print: "Page 001"
        print(page.name)
    """

    def __init__(self, uid, page):
        self.page = page
        self.uid = uid
        """The internal unique ID number of this Frame."""
        self._sv = [sv.FRAMELAYOUT]

    def __str__(self):
        """Brief string representation.

        Returns:
            `str`: Brief representation of this `Frame`.

        Example:

        .. code-block:: python

            import tecplot
            frame = tecplot.active_frame()

            # will print: 'Frame: "Frame 001"'
            print(frame)
        """
        return 'Frame: "{name}"'.format(name=self.name)

    def __repr__(self):
        """Executable string representation.

        Returns:
            `str`: Internal representation of this `Frame`.

        The string returned can be executed to generate an identical
        copy of this `Frame` object:

        .. code-block:: python

            import tecplot
            from tecplot.layout import Frame, Page

            frame = tecplot.active_frame()

            '''
            The "repr" string of the Frame is executable code.
            The following will print: "Frame(uid=11, page=Page(uid=1))"
            '''
            print(repr(frame))

            frame2 = None
            exec('frame2 = '+repr(frame))

            '''
            At this point, frame2 is just another handle to
            the exact same frame object in the Tecplot Engine
            '''
            assert frame2 == frame
        """
        return 'Frame(uid={uid}, page={page})'.format(uid=self.uid,
                                                      page=repr(self.page))

    def __eq__(self, other):
        """Checks for `Frame` equality in the |Tecplot Engine|.

        Returns:
            `bool`: `True` if the unique ID numbers are the same for both
            `Frames <Frame>`.

        Example:

        .. code-block:: python

            import tecplot

            page = tecplot.active_page()
            frame1 = page.active_frame()
            frame2 = page.add_frame()

            assert not (frame1 == frame2)
            assert page.active_frame() == frame2
        """
        return self.uid == other.uid

    @property
    def position(self):
        """`tuple`: ``(x,y)`` position of the `Frame` in inches.

        The `Frame` x position is relative to the left side of the paper.
        The `Frame` y position is relative to the top of the paper.

        If x is `None`, the `Frame` x position is not changed.
        If y is `None`, the `Frame` y position is not changed.

        Set `Frame` position 1 inch from the left side of the paper
        and two inches from the top of the paper::

            >>> tp.active_frame().position=(1.0, 2.0)

        Move the active `Frame` one inch to the right::

            >>> tp.active_frame().position=(tp.active_frame().position.x+1, None)
        """
        x = self._get_style(float, sv.XYPOS, sv.X)
        y = self._get_style(float, sv.XYPOS, sv.Y)
        return XYPosition(x, y)

    @position.setter
    def position(self, *pos):
        pos = XYPosition(*flatten_args(*pos))
        if pos.x is not None:
            self._set_style(float(pos.x), sv.XYPOS, sv.X)
        if pos.y is not None:
            self._set_style(float(pos.y), sv.XYPOS, sv.Y)

    @property
    def aux_data(self):
        """Auxiliary data for this frame.

        Returns:
            `AuxData`

        This is the auxiliary data attached to the frame. Such data is written
        to the layout file by default and can be retrieved later. Example
        usage::

            >>> aux = tp.active_frame().aux_data
            >>> aux['Result'] = '3.14159'
            >>> print(aux['Result'])
            3.14159
        """
        return session.AuxData(self, AuxDataObjectType.Frame)

    def texts(self):
        """Get an iterator for all `Text` objects in the frame.

        This example shows how to obtain a list of all red `Text` objects::

            >>> from tecplot.constant import Color
            >>> all_red_text_objects = [T for T in tp.active_frame().texts()
            ...                         if T.color == Color.Red]
        """
        return annotation.Annotation._Iterator(annotation.Text, self)

    def geometries(self):
        """*Not Implemented*"""
        raise TecplotNotImplementedError

    def images(self):
        """*Not Implemented*"""
        raise TecplotNotImplementedError

    @contextmanager
    def activated(self):
        """Context for temporarily activating this `Frame`.

        Example:

        .. code-block:: python

            import tecplot

            page = tecplot.active_page()
            frame1 = page.active_frame()
            frame2 = page.add_frame()

            assert frame2.active

            with frame1.activated():
                # frame1 is active only during this context
                assert frame1.active
                # there is only one frame active at a time
                assert not frame2.active

            assert frame2.active
        """
        frame_uid = _tecutil.FrameGetActiveID()
        if self.uid == frame_uid:
            yield
        else:
            page_uid = _tecutil.PageGetUniqueID()
            self.activate()
            try:
                yield
            finally:
                with lock():
                    if _tecutil.PageGetUniqueID() != page_uid:
                        _tecutil.PageSetCurrentByUniqueID(page_uid)
                    _tecutil.FrameActivateByUniqueID(frame_uid)

    @lock()
    def load_stylesheet(self, filename, plot_style=True, text=True, geom=True,
                        streams=True, contours=True, frame_geom=False,
                        merge=False):
        """Apply a stylesheet settings file to this frame.

        Parameters:
            filename (`str`): The path to a stylesheet file. (See note
                below conerning absolute and relative paths.)
            plot_style (`bool`, optional): Apply the stylesheet's
                plot style. (default: `True`)
            text (`bool`, optional): Include the stylesheet's text
                objects. (default: `True`)
            geom (`bool`, optional): Include the stylesheet's
                geometry objects. (default: `True`)
            streams (`bool`, optional): Include the stylesheet's
                stream traces. (default: `True`)
            contours (`bool`, optional): Include the stylesheet's
                contour levels. (default: `True`)
            frame_geom (`bool`, optional): Apply the stylesheet's
                frame position and size. (default: `False`)
            merge (`bool`, optional): Merge with the frame's current
                style. (default: `False`)

        .. note:: **Absolute and relative paths with PyTecplot**

            Relative paths, when used within the PyTecplot API are always from
            Python's current working directory which can be obtained by calling
            :func:`os.getcwd()`. This is true for batch and `connected
            <tecplot.session.connect()>` modes. One exception to this is paths
            within a macro command or file which will be relative to the
            |Tecplot Engine|'s home directory, which is typically the |Tecplot
            360| installation directory. Finally, when connected to a remote
            (non-local) instance of Tecplot 360, only absolute paths are
            allowed.

            Note that backslashes must be escaped which is especially important
            for windows paths such as ``"C:\\\\Users"`` or
            ``"\\\\\\\\server\\\\path"`` which will resolve to ``"C:\\Users"``
            and ``"\\\\server\\path"`` respectively. Alternatively, one may use
            Python's raw strings: ``r"C:\\Users"`` and ``r"\\\\server\\path"``

        Example usage::

            >>> frame = tecplot.active_frame()
            >>> frame.load_stylesheet('my_style.sty')
        """
        filepath = tecutil.normalize_path(filename)
        with self.activated():
            log.debug('Applying style from {} to frame'.format(filepath))
            if not _tecutil.ReadStylesheet(filepath, plot_style, text, geom,
                                           streams, contours, merge,
                                           frame_geom):
                raise TecplotSystemError()

    @lock()
    def save_stylesheet(self, filename, plot_style=True, aux_data=True,
                        text=True, geom=True, streams=True, contours=True,
                        defaults=False, relative_paths=True, compress=False):
        """Save the frame's current style to a file.

        Parameters:
            filename (`str`): The path to a stylesheet file. (See note
                below conerning absolute and relative paths.)
            plot_style (`bool`, optional): Include the frame's plot
                style. (default: `True`)
            aux_data (`bool`, optional): Include auxiliary data.
                (default: `True`)
            text (`bool`, optional): Include text objects. (default:
                `True`)
            geom (`bool`, optional): Include geometry objects.
                (default: `True`)
            streams (`bool`, optional): Include  stream traces.
                (default: `True`)
            contours (`bool`, optional): Include contour levels.
                (default: `True`)
            defaults (`bool`, optional): Include all factory defaults
                used by the current style. (default: `False`)
            relative_paths (`bool`, optional): Use relative paths.
                (default: `True`)
            compress (`bool`, optional): Compress the output of the
                style. (default: `False`)

        .. note:: **Absolute and relative paths with PyTecplot**

            Relative paths, when used within the PyTecplot API are always from
            Python's current working directory which can be obtained by calling
            :func:`os.getcwd()`. This is true for batch and `connected
            <tecplot.session.connect()>` modes. One exception to this is paths
            within a macro command or file which will be relative to the
            |Tecplot Engine|'s home directory, which is typically the |Tecplot
            360| installation directory. Finally, when connected to a remote
            (non-local) instance of Tecplot 360, only absolute paths are
            allowed.

            Note that backslashes must be escaped which is especially important
            for windows paths such as ``"C:\\\\Users"`` or
            ``"\\\\\\\\server\\\\path"`` which will resolve to ``"C:\\Users"``
            and ``"\\\\server\\path"`` respectively. Alternatively, one may use
            Python's raw strings: ``r"C:\\Users"`` and ``r"\\\\server\\path"``

        Example usage::

            >>> frame = tecplot.active_frame()
            >>> frame.save_stylesheet('my_style.sty')
        """
        filepath = tecutil.normalize_path(filename)
        with self.activated():
            with tecutil.ArgList() as arglist:
                arglist.update((
                    (sv.FNAME, str(filepath)),
                    (sv.INCLUDEPLOTSTYLE, bool(plot_style)),
                    (sv.INCLUDEAUXDATA, bool(aux_data)),
                    (sv.INCLUDETEXT, bool(text)),
                    (sv.INCLUDEGEOM, bool(geom)),
                    (sv.INCLUDESTREAMPOSITIONS, bool(streams)),
                    (sv.INCLUDECONTOURLEVELS, bool(contours)),
                    (sv.INCLUDEFACTORYDEFAULTS, bool(defaults)),
                    (sv.USERELATIVEPATHS, bool(relative_paths)),
                    (sv.COMPRESS, bool(compress))))
                if not _tecutil.WriteStylesheetX(arglist):
                    raise TecplotSystemError()

    @property
    def name(self):
        """`str`: Returns or sets the name.

        This is the name used when searching for `Frame` objects in
        `Page.frames` and `Page.frame`. It does not have to be unique,
        even for multiple frames in a single `Page`:

        .. code-block:: python

            import tecplot

            frame = tecplot.active_frame()
            frame.name = '3D Data View'

            # will print: "this frame: 3D Data View"
            print('this frame:', frame.name)
        """
        with self.activated():
            return _tecutil.FrameGetName()[1]

    @name.setter
    @lock()
    def name(self, name):
        with self.activated():
            _tecutil.FrameSetName(name)

    @property
    def active(self):
        """Checks if this `Frame` is active.

        Returns:
            `bool`: `True` if this `Frame` is the active `Frame`.
        """
        return self.uid == _tecutil.FrameGetActiveID()

    @property
    def current(self):
        return self.uid == _tecutil.FrameGetUniqueID()

    @lock()
    def activate(self):
        """Causes this `Frame` to become active.

        The parent `Page` is implicitly "activated" as a side-effect of this
        operation:

        .. code-block:: python

            import tecplot

            page1 = tecplot.active_page()
            frame1 = page1.active_frame()
            page2 = tecplot.add_page()
            frame2 = page2.active_frame()
            assert not (frame1.active and page1.active)
            assert frame2.active and page2.active

            frame1.activate()
            assert not (frame2.active or page2.active)
            assert frame1.active and page1.active
        """
        if not self.active:
            if self.page is not None:
                self.page.activate()
            if not _tecutil.FrameActivateByUniqueID(self.uid):
                err = 'could not activate frame with uid {0}'.format(self.uid)
                raise TecplotSystemError(err)

    @property
    def plot_type(self):
        """`constant.PlotType`: Returns or sets the current plot type.

        A `Frame` can have only one active plot type at any given time. The
        types are enumerated by `constant.PlotType`:

        .. code-block:: python

            import os
            import tecplot
            from tecplot.constant import PlotType

            frame = tecplot.active_frame()
            assert frame.plot_type is PlotType.Sketch

            install_dir = tecplot.session.tecplot_install_directory()
            infile = os.path.join(install_dir, 'examples', 'SimpleData', 'SpaceShip.lpk')
            tecplot.load_layout(infile)

            frame = tecplot.active_frame()
            assert frame.plot_type is PlotType.Cartesian3D

            frame.plot_type = PlotType.Cartesian2D
            assert frame.plot_type is PlotType.Cartesian2D

        .. note:: Plot type cannot be set to `constant.PlotType.Automatic`.
        """
        return _tecutil.FrameGetPlotTypeForFrame(self.uid)

    @plot_type.setter
    @lock()
    def plot_type(self, plot_type):
        with self.activated():
            try:
                res = _tecutil.FrameSetPlotType(plot_type.value)
            except TecplotSystemError as err:
                if not self.has_dataset:
                    res = SetValueReturnCode.ContextError1
                else:
                    raise err
            if res not in [SetValueReturnCode.Ok,
                           SetValueReturnCode.DuplicateValue]:
                if res is SetValueReturnCode.ContextError1:
                    raise TecplotSystemError('no dataset attached to frame')
                raise TecplotSystemError(res)

    def plot(self, plot_type=PlotType.Active):
        """The primary `Plot` style-control object.

        Returns:
            `Plot`:
                One of the possible `Plot` subclasses, depending on the
                ``plot_type`` specified. By default, the active plot
                type, obtained from `Frame.plot_type`, is used.

        The `Plot` object is the handle through which one can manipulate the
        style and visual representation of the `Dataset`. Possible return types
        are: `SketchPlot`, `Cartesian2DFieldPlot`, `Cartesian3DFieldPlot`,
        `PolarLinePlot` and `XYLinePlot`. Each of these have their own specific
        set of attributes and methods:

        .. code-block:: python

            import os
            import tecplot
            from tecplot.constant import PlotType

            install_dir = tecplot.session.tecplot_install_directory()
            infile = os.path.join(install_dir, 'examples', 'SimpleData', 'SpaceShip.lpk')
            tecplot.load_layout(infile)

            frame = tecplot.active_frame()
            assert frame.plot_type is PlotType.Cartesian3D

            plot3d = frame.plot()
            plot3d.show_contour = True
        """
        if plot_type is PlotType.Active:
            plot_type = None
        _dispatch = {
            PlotType.Cartesian2D: plot.Cartesian2DFieldPlot,
            PlotType.Cartesian3D: plot.Cartesian3DFieldPlot,
            PlotType.XYLine: plot.XYLinePlot,
            PlotType.PolarLine: plot.PolarLinePlot,
            PlotType.Sketch: plot.SketchPlot}
        return _dispatch[plot_type or self.plot_type](self)

    @lock()
    def move_to_bottom(self):
        """Moves `Frame` behind all others in `Page`.
        """
        _tecutil.FrameMoveToBottomByUniqueID(self.uid)

    @lock()
    def move_to_top(self):
        """Moves `Frame` in front of all others in `Page`.
        """
        _tecutil.FrameMoveToTopByUniqueID(self.uid)

    @lock()
    def active_zones(self, *zones):
        """Returns or sets the active `Zones <data_access>`.

        Parameters:
            zones (`Zones <data_access>`, optional): The `Zone <data_access>`
                objects, which must be in the `Dataset` attached to this
                `Frame`, that will be activated. All other `Zones
                <data_access>` will be deactivated.

        Returns:
            `Zones <data_access>`:
                This will return a generator of active `Zones <data_access>` in
                this `Frame`.

        This should only be used on frames with an active plot type that
        contains a dataset with at least one zone.
        """
        if __debug__:
            if self.plot_type is PlotType.Sketch:
                err = 'Active plot type is Sketch which has no active zones.'
                raise TecplotLogicError(err)
            if not self.has_dataset:
                raise TecplotLogicError('Frame has no dataset.')
            if self.dataset.num_zones == 0:
                raise TecplotLogicError('Dataset has no zones.')

        with self.activated():
            if zones:
                with IndexSet(*zones) as zoneset:
                    _tecutil.ZoneSetActive(zoneset, AssignOp.Equals.value)
            else:
                zoneset = _tecutil.ZoneGetActiveForFrame(self.uid)
                zones = [self.dataset.zone(i) for i in zoneset]
                zoneset.dealloc()
            return zones

    @lock()
    def delete_text(self, text):
        """Delete a `text <annotation.Text>` object from a frame.

        When deleted, the text object is no longer displayed in the frame and is
        permanently invalid. To display the text in the frame again,
        a new text object must be created by calling `add_text`.

        .. warning::
            Use this method with care.
            After a text object has been deleted by calling this method,
            it is no longer valid, and all properties of the deleted text
            object will throw `TecplotLogicError` when accessed.

        Example usage:

        .. code-block:: python

            import tecplot as tp

            text = tp.active_frame().add_text("abc")
            tp.active_frame().delete_text(text)

            # The text object is no longer valid.
            # Any property access will throw TecplotLogicError
            try:
                print(text.text_string)
            except tp.exception.TecplotLogicError as e:
                print(e)

        .. seealso:: `add_text`
        """
        text._delete()

    @lock()
    def add_text(self, text, position=None, coord_sys=None, typeface=None,
                 bold=None, italic=None, size_units=None, size=None,
                 color=None, angle=None, line_spacing=None, anchor=None,
                 box_type=None, line_thickness=None, box_color=None,
                 fill_color=None, margin=None, zone=None):
        """Adds a `text <annotation.Text>` to a `Frame`.

        Parameters:
            text (`str`): The text to add to the `Frame`.
                The text string must have a non-zero length.
            position (`tuple` of `floats <float>` (x,y), optional): The
                position of the anchor as a percentage of the
                specified coordinates. (default: (0,0))
            coord_sys (`CoordSys`, optional): Coordinate system used to
                position the anchor of the text object. The possible values
                are: `CoordSys.Grid` or `CoordSys.Frame`. (default:
                `CoordSys.Frame`)
            typeface (`str`, optional): The typeface name. For
                consistency across various platforms, Tecplot guarantees that
                the following standard typeface names are available:
                "Helvetica", "Times", "Courier", "Greek", "Math", and "User
                Defined". Other typefaces may or may not be available depending
                on the TrueType fonts available. If the typeface name or style
                is not available, a suitable replacement will be selected.
                (default: "Helvetica")
            bold (`bool`, optional): Use the bold variation of the
                specified typeface. (default: `True`)
            italic (`bool`, optional): Use the italic variation of
                the specified typeface. (default: `False`)
            size_units (`Units`, optional): Text sizing units. Possible
                values are: `Units.Grid`, `Units.Frame` or `Units.Point`.
                (default: `Units.Point`)
            size (`float`, optional): Text height in the specified units.
                (default: 14)
            color (`Color`, optional): Color of the text
                   (default: `Color.Black`)
            angle (`float`, optional): Angle of the text baseline in degrees
                from -360 to 360. (default: 0)
            line_spacing (`float`, optional): Line spacing in units of line
                size. Can take values from 0 to 50. (default: 1)
            anchor (`TextAnchor`, optional): Anchor position with respect to
                the text box. Possible values are: `TextAnchor.Left`,
                `TextAnchor.Center`, `TextAnchor.Right`,
                `TextAnchor.MidLeft`, `TextAnchor.MidCenter`,
                `TextAnchor.MidRight`, `TextAnchor.HeadLeft`,
                `TextAnchor.HeadCenter`, `TextAnchor.HeadRight`,
                `TextAnchor.OnSide` (default: `TextAnchor.Left`)
            box_type (`constant.TextBox`, optional): Type of text box can be one
                of: `constant.TextBox.None_`, `constant.TextBox.Filled` or `constant.TextBox.Hollow`.
                (default: `constant.TextBox.None_`)
            line_thickness (`float`, optional): Text box boarder line
                thickness may be a value in the range from 0.0001 to 100.
                (default: 0.1)
            box_color (`Color`, optional): Text box border line color. See
                `Color` for possible values. (default: `Color.Black`)
            fill_color (`Color`, optional): Text box fill color. See `Color`
                for possible values. (default: `White`)
            margin (`float`, optional): Margin between the text and text
                box. May be in the range from 0 to 2000. (default: 20)
            zone (`Zone <data_access>`, optional): `Zone <data_access>` or
                `XYLinemap` to which the text will be attached. (default: None)

        Returns:
            `annotation.Text`: The resulting `text box <annotation.Text>`
            object.

        Example:

        .. code-block:: python
            :emphasize-lines: 5-6

            import tecplot
            from tecplot.constant import Color

            frame = tecplot.active_frame()
            frame.add_text('Hello, World!', position=(35, 50),
                           bold=True, italic=False, color=Color.Blue)

        .. seealso:: `delete_text`
        """
        with self.activated():
            with tecutil.ArgList() as arglist:
                if __debug__:
                    check_arglist_argtypes(
                        'frame.add_text',
                        ([tuple], [position], ['position']),
                        ([CoordSys], [coord_sys], ['coord_sys']),
                        (string_types, [typeface, text], ['typeface', 'text']),
                        ([bool], [bold, italic], ['bold', 'italic']),
                        ([Units], [size_units], ['size_units']),
                        ([Number], [size, angle, line_thickness, margin,
                                    line_spacing],
                            ['size', 'angle', 'line_thickness', 'margin',
                             'line_spacing']),
                        ([Color], [color, box_color, fill_color],
                            ['color', 'text_color', 'fill_color']),
                        ([TextAnchor], [anchor], ['anchor']),
                        ([TextBox], [box_type], ['box_type']),
                    )

                if zone is not None:
                    arglist[sv.ATTACHTOZONE] = True
                    arglist[sv.ZONE] = zone.index + 1

                def optional(type_, value):
                    return type_(value) if value is not None else None

                # Note that TecUtil calls SV_TEXTCOLOR the color of the text,
                # and SV_COLOR as the text *box* color. These names correspond
                # to the 'color' and 'box_color' parameters.
                arglist.update((
                    (sv.TEXT, text),
                    (sv.POSITIONCOORDSYS, coord_sys),
                    (sv.ISBOLD, bold),
                    (sv.ISITALIC, italic),
                    (sv.SIZEUNITS, size_units),
                    (sv.ANCHOR, anchor),
                    (sv.COLOR, box_color),
                    (sv.TEXTCOLOR, color),
                    (sv.FILLCOLOR, fill_color),
                    (sv.BOXTYPE, box_type)))
                if position is not None:
                    arglist[sv.XPOS] = optional(float, position[0])
                    arglist[sv.YPOS] = optional(float, position[1])

                arglist[sv.HEIGHT] = optional(float, size)
                arglist[sv.ANGLE] = optional(float, angle)
                arglist[sv.LINETHICKNESS] = optional(float, line_thickness)
                arglist[sv.MARGIN] = optional(float, margin)
                arglist[sv.LINESPACING] = optional(float, line_spacing)

                return annotation.Text(_tecutil.TextCreateX(arglist), self)

    @lock()
    def create_dataset(self, name, var_names=None, reset_style=False):
        """Create an empty `Dataset`.

        This will create a new `Dataset` and replace the existing one,
        destroying all data associated with it.

        Parameters:
            name (`str`): Title of the new `Dataset`. This does not
                have to be unique.
            var_names (`list` of `strings <str>`, optional): `Variable`
                names. This only sets the names and not the data type or
                location. See `add_variable`. (default: `None`)
            reset_style (`bool`): Reset style of the active `Frame`
                before loading the `Dataset`. (default: `False`)

        Returns:
            `Dataset`: The newly created `Dataset`.

        .. note:: Relationships between `Frame` and `Dataset`

            A `Frame` may only hold a single `Dataset`, though this `Dataset`
            may be shared between several `Frames <Frame>`. Therefore, this
            method will only *replace* the current dataset when **reset_style**
            is set to `True` and will fail otherwise. If this `Frame` already
            has a `Dataset`, it may be more efficient to do one of the following
            instead:

                * Add a new (blank) frame with `Page.add_frame()` and create
                  a `Dataset` for this.
                * Add new zones to the existing `Dataset` with
                  `Dataset.add_ordered_zone()`, `Dataset.add_fe_zone()` or
                  `Dataset.add_poly_zone()`.
                * Change the existing data `in-place <Array>`.

        .. note::

            When performing many data-manipulation operations including adding
            zones, adding variables, modifying field data or connectivity, and
            especially in connected mode, it is recommended to do this all with
            the `tecplot.session.suspend()`. This will prevent the Tecplot
            engine from trying to "keep up" with the changes. Tecplot will be
            notified of all changes made upon exit of this context. This may
            result in significant performance gains for long operations. See
            the documentation for `tecplot.session.suspend()` for more
            information.

        """
        with self.activated():
            if var_names is not None:
                var_names = StringList(*var_names)
            try:
                if not _tecutil.DataSetCreate(name, var_names, reset_style):
                    raise TecplotSystemError()
            finally:
                if var_names is not None:
                    var_names.dealloc()
            return self.dataset

    def _get_style(self, rettype, *svargs):
        svargs = self._sv + list(svargs)
        return session.get_style(rettype, *svargs, uniqueid=self.uid)

    def _set_style(self, value, *svargs):
        svargs = self._sv + list(svargs)
        session.set_style(value, *svargs, uniqueid=self.uid)

    @property
    def background_color(self):
        """`Color`: Color of the background."""
        return self._get_style(constant.Color, sv.BACKGROUNDCOLOR)

    @background_color.setter
    def background_color(self, value):
        self._set_style(constant.Color(value), sv.BACKGROUNDCOLOR)

    @property
    def border_thickness(self):
        """`float`: The border thickness in units of `Frame.size_pos_units`."""
        return self._get_style(float, sv.BORDERTHICKNESS)

    @border_thickness.setter
    def border_thickness(self, value):
        self._set_style(float(value), sv.BORDERTHICKNESS)

    @property
    def height(self):
        """`float`: The height in units of `Frame.size_pos_units`."""
        return self._get_style(float, sv.HEIGHT)

    @height.setter
    def height(self, value):
        self._set_style(float(value), sv.HEIGHT)

    @property
    def show_border(self):
        """`bool`: Show or hide the `Frame`'s border."""
        return self._get_style(bool, sv.SHOWBORDER)

    @show_border.setter
    def show_border(self, value):
        self._set_style(bool(value), sv.SHOWBORDER)

    @property
    def show_header(self):
        """`bool`: Show or hide the `Frame`'s header in the border."""
        return self._get_style(bool, sv.SHOWHEADER)

    @show_header.setter
    def show_header(self, value):
        self._set_style(bool(value), sv.SHOWHEADER)

    @property
    def header_background_color(self):
        """`Color`: The header's background color."""
        return self._get_style(constant.Color, sv.HEADERCOLOR)

    @header_background_color.setter
    def header_background_color(self, value):
        self._set_style(constant.Color(value), sv.HEADERCOLOR)

    @property
    def size_pos_units(self):
        """`FrameSizePosUnits`: The units used for size properties.

        Possible values: `Paper`, `Workspace <FrameSizePosUnits.Workspace>`.
        """
        return self._get_style(constant.FrameSizePosUnits, sv.FRAMESIZEPOSUNITS)

    @size_pos_units.setter
    def size_pos_units(self, value):
        self._set_style(constant.FrameSizePosUnits(value), sv.FRAMESIZEPOSUNITS)

    @property
    def transparent(self):
        """`bool`: Use transparency within this `Frame`."""
        return self._get_style(bool, sv.ISTRANSPARENT)

    @transparent.setter
    def transparent(self, value):
        self._set_style(bool(value), sv.ISTRANSPARENT)

    @property
    def width(self):
        """`float`: The width in units of `Frame.size_pos_units`."""
        return self._get_style(float, sv.WIDTH)

    @width.setter
    def width(self, value):
        self._set_style(float(value), sv.WIDTH)
