#!/usr/bin/env python

"""Implementation of the tabular data display widget."""

import os
import sys
import numbers

try:
    # Python 3
    import tkinter as tk
except (ImportError):
    # Python 2
    import Tkinter as tk

try:
    try:
        # Python 3
        import tkinter.ttk as ttk
    except (ImportError):
        # Python 2
        import ttk
except (ImportError):
    # Can't provide ttk's Scrollbar
    pass


__all__ = ["DataCanvas"]


class DataCanvas(tk.Frame):
    """Tabular data display widget.

    The constructor accepts the usual Tkinter keyword arguments, plus
    a handful of its own:

      scrollbars (str; default: "both")
        Which scrollbars to provide.
        Must be one of "vertical", "horizontal," "both", or "neither".

      shade_rows (bool; default: True)
        Enables shading alternate rows for readability.

      use_ttk (bool; default: False)
        Whether to use ttk widgets if available.
        The default is to use standard Tk widgets. This setting has
        no effect if ttk is not available on your system.
    """

    # Implementation note:
    # This is essentially a combination of tkMagicGrid and tkScrolledFrame,
    # except it draws cells directly on the canvas rather than using a whole
    # bunch of individual Label widgets.

    def __init__(self, master=None, **kw):
        """Return a new scrollable frame widget."""

        tk.Frame.__init__(self, master)

        # Which scrollbars to provide
        if "scrollbars" in kw:
            scrollbars = kw["scrollbars"]
            del kw["scrollbars"]

            if not scrollbars:
                scrollbars = self._default_scrollbars
            elif not scrollbars in self._valid_scrollbars:
                raise ValueError("scrollbars parameter must be one of "
                                 "'vertical', 'horizontal', 'both', or "
                                 "'neither'")
        else:
            scrollbars = self._default_scrollbars

        # Whether to shade alternate rows
        if "shade_rows" in kw:
            self._shade_rows = kw["shade_rows"]
            del kw["shade_rows"]
        else:
            # Shade rows by default
            self._shade_rows = True

        # Whether to use ttk widgets if available
        if "use_ttk" in kw:
            if ttk and kw["use_ttk"]:
                Scrollbar = ttk.Scrollbar
            else:
                Scrollbar = tk.Scrollbar
            del kw["use_ttk"]
        else:
            Scrollbar = tk.Scrollbar

        # Default to a 1px sunken border
        if not "borderwidth" in kw:
            kw["borderwidth"] = 1
        if not "relief" in kw:
            kw["relief"] = "sunken"

        # Set up the grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Canvas widget
        c = self._canvas = tk.Canvas(self,
                                     borderwidth=0,
                                     highlightthickness=0,
                                     takefocus=0)

        # Enable scrolling when the canvas has the focus
        self.bind_arrow_keys(c)
        self.bind_scroll_wheel(c)

        # Scrollbars
        xs = self._x_scrollbar = Scrollbar(self,
                                           orient="horizontal",
                                           command=c.xview)
        ys = self._y_scrollbar = Scrollbar(self,
                                           orient="vertical",
                                           command=c.yview)
        c.configure(xscrollcommand=xs.set, yscrollcommand=ys.set)

        # Lay out our widgets
        c.grid(row=0, column=0, sticky="nsew")
        if scrollbars == "vertical" or scrollbars == "both":
            ys.grid(row=0, column=1, sticky="ns")
        if scrollbars == "horizontal" or scrollbars == "both":
            xs.grid(row=1, column=0, sticky="we")

        # Forward these to the canvas widget
        self.bind = c.bind
        self.focus_set = c.focus_set
        self.unbind = c.unbind
        self.xview = c.xview
        self.xview_moveto = c.xview_moveto
        self.yview = c.yview
        self.yview_moveto = c.yview_moveto

        # The row and column where we should add our next cell
        self._row = 0
        self._col = 0

        # Length of the largest row we've added
        self._row_max = 0

        # List of lists of dictionaries of keyword arguments for constructing
        # table cells (phew!). Contrast with tkMagicGrid, where self._cells
        # contains the Tk widgets themselves.
        #
        # To access a particular widget, use self._cells[row][column]
        self._cells = [ [] ]

        if self._shade_rows:
            # Set the frame background to the default cell background
            self.configure(background=self.bg_color)

        # Process our remaining configuration options
        self.configure(**kw)

    def __setitem__(self, key, value):
        """Configure resources of a widget."""

        if key in self._canvas_keys:
            # Forward these to the canvas widget
            self._canvas.configure(**{key: value})

        else:
            # Handle everything else normally
            tk.Frame.configure(self, **{key: value})

    # ------------------------------------------------------------------------

    def add_cell(self, contents="", **kw):
        """Add a cell with the specified contents to the current row.

        After you have finished adding cells, use the display() method
        to display your data on the canvas.
        """

        if contents or isinstance(contents, numbers.Number):
            # Preset the cell text
            kw["text"] = str(contents)

        if isinstance(contents, numbers.Number):
            # Right-align numeric values by default
            if not "anchor" in kw:
                kw["anchor"] = "e"
            if not "justify" in kw:
                kw["justify"] = "right"

        else:
            # Left-align all other values by default
            if not "anchor" in kw:
                kw["anchor"] = "w"
            if not "justify" in kw:
                kw["justify"] = "left"

        # Whether to colorize the widget
        if ("bg" in kw
            or "background" in kw
            or "fg" in kw
            or "foreground" in kw):
            # Don't colorize the widget if the user specified colors
            do_colorize = False

        else:
            # Assume we need to colorize the widget
            do_colorize = True

        # Store this cell's information
        self._cells[self._row].append(kw)

        # Increment the grid column
        self._col += 1

        # Check if this is the longest row we've added, and if it is,
        # store its length for later reference
        if self._col > self._row_max:
            self._row_max = self._col

        # Set the default foreground/background colors
        if do_colorize:
            self._colorize(kw)

    def add_header(self, *cells, **kw):
        """Add a header row to the grid.

        The next cell added to the grid will start a new row.

        After you have finished adding cells, use the display() method
        to display your data on the canvas.
        """

        return self.add_row(*cells,
                            background=self.bg_header,
                            foreground=self.fg_header,
                            **kw)

    def add_row(self, *cells, **kw):
        """Add an entire row of cells to the grid.

        The next cell added to the grid will start a new row.

        After you have finished adding cells, use the display() method
        to display your data on the canvas.
        """

        header_widgets = []

        for cell in cells:
            widget = self.add_cell(cell, **kw)
            header_widgets.append(widget)

        self.end_row()

        return header_widgets

    def bind_arrow_keys(self, widget):
        """Bind the specified widget's arrow key events to the canvas."""

        widget.bind("<Up>",
                    lambda event: self._canvas.yview_scroll(-1, "units"))

        widget.bind("<Down>",
                    lambda event: self._canvas.yview_scroll(1, "units"))

        widget.bind("<Left>",
                    lambda event: self._canvas.xview_scroll(-1, "units"))

        widget.bind("<Right>",
                    lambda event: self._canvas.xview_scroll(1, "units"))

    def bind_scroll_wheel(self, widget):
        """Bind the specified widget's mouse scroll event to the canvas."""

        widget.bind("<MouseWheel>", self._scroll_canvas)
        widget.bind("<Button-4>", self._scroll_canvas)
        widget.bind("<Button-5>", self._scroll_canvas)

    def cget(self, key):
        """Return the resource value for a KEY given as string."""

        if key in self._canvas_keys:
            return self._canvas.cget(key)

        else:
            return tk.Frame.cget(self, key)

    # Also override this alias for cget()
    __getitem__ = cget

    def configure(self, cnf=None, **kw):
        """Configure resources of a widget."""

        # This is overridden so we can use our custom __setitem__()
        # to pass certain options directly to the canvas.
        if cnf:
            for key in cnf:
                self[key] = cnf[key]

        for key in kw:
            self[key] = kw[key]

    # Also override this alias for configure()
    config = configure

    def display(self):
        """Display data on the canvas."""

        # Clear the canvas
        self._canvas.delete("all")

        col_widths = []
        row_heights = []

        for _ in range(self._row_max):
            # Initialize all column widths to zero
            col_widths.append(0)

        for _ in range(len(self._cells)):
            # Initialize all row heights to zero
            row_heights.append(0)

        cur_row = 0
        for row in self._cells:
            cur_col = 0
            for cell in row:
                # Create an off-screen Label widget for this cell to
                # measure the necessary row height and column width
                l = tk.Label(self._canvas, **cell)

                col_widths[cur_col] = max(col_widths[cur_col],
                                          l.winfo_reqwidth())
                row_heights[cur_row] = max(row_heights[cur_row],
                                           l.winfo_reqheight())

                l.destroy()
                cur_col += 1

            cur_row += 1

        # Draw cells on the canvas
        y = 0
        cur_row = 0
        for row in self._cells:
            height = row_heights[cur_row]

            x = 0
            cur_col = 0
            for cell in row:
                width = col_widths[cur_col]

                # Get cell attributes...
                anchor = cell["anchor"]

                if "bg" in cell:
                    bg_color = cell["bg"]
                elif "background" in cell:
                    bg_color = cell["background"]
                else:
                    bg_color = self.bg_color

                if "fg" in cell:
                    fg_color = cell["fg"]
                elif "foreground" in cell:
                    fg_color = cell["foreground"]
                else:
                    fg_color = self.fg_color

                # ...and delete the associated keywords so they won't
                # cause problems with the canvas methods
                for key in ("width", "anchor",
                            "bg", "fg", "background", "foreground"):
                    if key in cell:
                        del cell[key]

                # Figure out where to position the text. Since we're drawing
                # directly on the canvas rather than using a Label widget,
                # we have to work out the coordinates ourselves.
                text_anchor = ""
                if len(anchor) <= 2:
                    if "n" in anchor:
                        ty = y
                        text_anchor += "n"
                    elif "s" in anchor:
                        ty = y + height
                        text_anchor += "s"
                    else:
                        ty = y + (height / 2)

                    if "w" in anchor:
                        tx = x
                        text_anchor += "w"
                    elif "e" in anchor:
                        tx = x + width
                        text_anchor += "e"
                    else:
                        tx = x + (width / 2)

                else:
                    tx = x + (width / 2)
                    ty = y + (height / 2)

                if not text_anchor:
                    # Center text vertically and horizontally
                    text_anchor = "center"

                # Add cell padding
                pad_x = self.pad_x
                tx += pad_x
                width += 2 * pad_x

                # Draw a rectangle for the cell background
                self._canvas.create_rectangle(x, y, x + width, y + height,
                                              fill=bg_color,
                                              outline=bg_color)

                # Add the cell text
                self._canvas.create_text(tx, ty,
                                         anchor=text_anchor,
                                         fill=fg_color,
                                         **cell)

                x += width
                cur_col += 1

            y += height
            cur_row += 1

        self._canvas.update_idletasks()
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def end_row(self):
        """End the current row.

        The next cell added to the grid will start a new row.
        """

        self._col = 0
        self._row += 1
        self._cells.append([])

    def erase(self):
        """Erase the canvas and all data."""

        # Clear the canvas
        self._canvas.delete("all")

        # Erase data
        for row in self._cells:
            del row[:]
        del self._cells[:]
        del self._cells
        self._cells = [ [] ]

        # Reset the location of the next cell
        self._row = 0
        self._col = 0

        # Reset the length of the longest row added
        self._row_max = 0

        # Scroll to the top-left corner
        self.scroll_to_top()

    def scroll_to_top(self):
        """Scroll to the top-left corner of the canvas."""

        self._canvas.xview_moveto(0)
        self._canvas.yview_moveto(0)

    # ------------------------------------------------------------------------

    def _colorize(self, kw):
        """Colorize the specified cell.

        This function is used to implement shading alternate rows.
        The "fg"/"foreground" and "bg"/"background" keyword arguments
        will override the default colors.
        """

        if not self._shade_rows:
            return

        if not ("fg" in kw or "foreground" in kw):
            if self._row % 2 == 0:
                kw["foreground"] = self.fg_shade
            else:
                kw["foreground"] = self.fg_color

        if not ("bg" in kw or "background" in kw):
            if self._row % 2 == 0:
                kw["background"] = self.bg_shade
            else:
                kw["background"] = self.bg_color

    def _scroll_canvas(self, event):
        """Scroll the canvas."""

        c = self._canvas

        if sys.platform.startswith("darwin"):
            # macOS
            c.yview_scroll(-1 * event.delta, "units")

        elif event.num == 4:
            # Unix - scroll up
            c.yview_scroll(-1, "units")

        elif event.num == 5:
            # Unix - scroll down
            c.yview_scroll(1, "units")

        else:
            # Windows
            c.yview_scroll(-1 * (event.delta // 120), "units")

    # ------------------------------------------------------------------------

    # Keys for configure() to forward to the canvas widget
    _canvas_keys = "width", "height", "takefocus"

    # Scrollbar-related configuration
    _default_scrollbars = "both"
    _valid_scrollbars = "vertical", "horizontal", "both", "neither"

    # Default colors for the grid
    bg_color = "white"
    fg_color = "black"

    # Shade colors for alternate rows
    bg_shade = "LightSteelBlue"
    fg_shade = "black"

    # Colors for header rows
    bg_header = "SteelBlue"
    fg_header = "white"

    # Default padding for cells
    pad_x = 1
