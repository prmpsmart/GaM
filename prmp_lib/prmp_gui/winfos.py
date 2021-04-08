



class Winfos:
    
    def winfo_children(self):
        """Return a list of all widgets which are children of this widget."""

    def winfo_class(self):
        """Return window class name of this widget."""

    def winfo_colormapfull(self):
        """Return true if at the last color request the colormap was full."""

    def winfo_containing(self, rootX, rootY, displayof=0):
        """Return the widget which is at the root coordinates ROOTX, ROOTY."""
        
    def winfo_exists(self):
        """Return true if this widget exists."""

    def winfo_fpixels(self, number):
        """Return the number of pixels for the given distance NUMBER
        (e.g. "3c") as float."""

    def winfo_id(self):
        """Return identifier ID for this widget."""
        
    def winfo_interps(self, displayof=0):
        """Return the name of all Tcl interpreters for this display."""
        
    def winfo_ismapped(self):
        """Return true if this widget is mapped."""
        
    def winfo_manager(self):
        """Return the window manager name for this widget."""
        
    def winfo_name(self):
        """Return the name of this widget."""
        
    def winfo_parent(self):
        """Return the name of the parent of this widget."""
        
    def winfo_pathname(self, id, displayof=0):
        """Return the pathname of the widget given by ID."""
        
    def winfo_pixels(self, number):
        """Rounded integer value of winfo_fpixels."""
        
    def winfo_rgb(self, color):
        """Return tuple of decimal values for red, green, blue for
        COLOR in this widget."""
        
    def winfo_screen(self):
        """Return the screen name of this widget."""
        
    def winfo_screencells(self):
        """Return the number of the cells in the colormap of the screen
        of this widget."""
        
    def winfo_screenvisual(self):
        """Return one of the strings directcolor, grayscale, pseudocolor,
        staticcolor, staticgray, or truecolor for the default
        colormodel of this screen."""
        
    def winfo_screenwidth(self):
        """Return the number of pixels of the width of the screen of
        this widget in pixel."""
        
    def winfo_server(self):
        """Return information of the X-Server of the screen of this widget in
        the form "XmajorRminor vendor vendorVersion"."""
        
    def winfo_toplevel(self):
        """Return the toplevel widget of this widget."""
        
    def winfo_viewable(self):
        """Return true if the widget and all its higher ancestors are mapped."""
        
    def winfo_visual(self):
        """Return one of the strings directcolor, grayscale, pseudocolor,
        staticcolor, staticgray, or truecolor for the
        colormodel of this widget."""
        
    def winfo_visualid(self):
        """Return the X identifier for the visual for this widget."""
        
    def winfo_visualsavailable(self, includeids=False):
        """Return a list of all visuals available for the screen
        of this widget.

        Each item in the list consists of a visual name (see winfo_visual), a
        depth and if includeids is true is given also the X identifier."""


class Geometry:
    
    
    def winfo_depth(self):
        """Return the number of bits per pixel."""
        
    def winfo_geometry(self):
        """Return geometry string for this widget in the form "widthxheight+X+Y"."""

    def winfo_height(self):
        """Return height of this widget."""

        
    def winfo_pointerx(self):
        """Return the x coordinate of the pointer on the root window."""
        
    def winfo_pointerxy(self):
        """Return a tuple of x and y coordinates of the pointer on the root window."""
        
    def winfo_pointery(self):
        """Return the y coordinate of the pointer on the root window."""
        
    def winfo_reqheight(self):
        """Return requested height of this widget."""
        
    def winfo_reqwidth(self):
        """Return requested width of this widget."""
        
    def winfo_rootx(self):
        """Return x coordinate of upper left corner of this widget on the
        root window."""
        
    def winfo_rooty(self):
        """Return y coordinate of upper left corner of this widget on the
        root window."""

    def winfo_screendepth(self):
        """Return the number of bits per pixel of the root window of the
        screen of this widget."""
        
    def winfo_screenheight(self):
        """Return the number of pixels of the height of the screen of this widget
        in pixel."""
        
    def winfo_screenmmheight(self):
        """Return the number of pixels of the height of the screen of
        this widget in mm."""
        
    def winfo_screenmmwidth(self):
        """Return the number of pixels of the width of the screen of
        this widget in mm."""
        
    def winfo_vrootheight(self):
        """Return the height of the virtual root window associated with this
        widget in pixels. If there is no virtual root window return the
        height of the screen."""
        
    def winfo_vrootwidth(self):
        """Return the width of the virtual root window associated with this
        widget in pixel. If there is no virtual root window return the
        width of the screen."""
        
    def winfo_vrootx(self):
        """Return the x offset of the virtual root relative to the root
        window of the screen of this widget."""
        
    def winfo_vrooty(self):
        """Return the y offset of the virtual root relative to the root
        window of the screen of this widget."""
        
    def winfo_width(self):
        """Return the width of this widget."""
        
    def winfo_x(self):
        """Return the x coordinate of the upper left corner of this widget
        in the parent."""
        
    def winfo_y(self):
        """Return the y coordinate of the upper left corner of this widget
        in the parent."""


