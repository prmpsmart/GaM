from . import *



class PRMP_DropDownWidget:
    WidgetClass = None

    def __init__(self, master=None, ddwc=None, dropdown_windowclass=None, ddwk={}, dropdown_windowkwargs={}, attr='', valueType=str, validatecmd=None, **kwargs):
        """
        Create an entry with a drop-down widget
        """

        self.dropdown_window = None

        self.attr = attr # will be used to get the attr of the return value from the dropdown_windowclass
        self.valueType = valueType # a function to be used to convert the attr of the desired value to be viewed in this widget

        self._determine_downarrow_name_after_id = ''

        # dropdown_window
        dropdown_windowclass = ddwc or dropdown_windowclass
        dropdown_windowkwargs = ddwk or dropdown_windowkwargs
        self.geo = dropdown_windowkwargs.get('geo')

        self.WidgetClass.__init__(self, master, **kwargs)

        if issubclass(dropdown_windowclass, (PRMP_Window, PRMP_MainWindow)): dropdown_windowkwargs.update(dict(tooltype=1, normTk=1))
        self.dropdown_window = dropdown_windowclass(self, callback=self.set, **dropdown_windowkwargs) if dropdown_windowclass else Toplevel(self, **dropdown_windowkwargs)
        self.dropdown_window.withdraw()

        # add validation to Entry so that only desired input format are accepted

        self.validate_cmd = validatecmd
        if validatecmd:
            validatecmd = self.register(validatecmd)
            self.configure(validate='focusout', validatecommand=validatecmd)

        # self._downarrow_name = ''

        # --- bindings
        # determine new downarrow button bbox
        self.bind('<Configure>', self._determine_downarrow_name, '+')
        self.bind('<Map>', self._determine_downarrow_name, '+')

        # handle appearance to make the entry behave like a Combobox but with a drop-down widget instead of a drop-down list
        self.bind('<Leave>', lambda e: self.state(['!active']))
        self.bind('<ButtonPress-1>', self._on_b1_press, '+')
        self.bind('<Down>', self.drop_down, '+')
        # update entry content when date is selected in the Calendar
        # hide dropdown_window if it looses focus
        self.dropdown_window.bind('<FocusOut>', self._on_focus_out_dropdown_window, '+')
        self.dropdown_window.bind('<Up>', self._on_focus_out_dropdown_window, '+')

    def _determine_downarrow_name(self, event=None):
        """Determine downarrow button name."""
        try:
            self.after_cancel(self._determine_downarrow_name_after_id)
        except ValueError:
            # nothing to cancel
            pass
        if self.winfo_ismapped():
            self.update_idletasks()
            y = self.winfo_height() // 2
            x = self.winfo_width() - 10
            try: name = self.identify(x, y)
            except: name = 'no_name'
            if name: self._downarrow_name = name
            else:
                self._determine_downarrow_name_after_id = self.after(10, self._determine_downarrow_name)

    def _on_b1_press(self, event=None):
        """Trigger self.drop_down on widget press and set widget state to ['pressed', 'active']."""

        if str(self['state']) != 'disabled':
            self['state'] = 'pressed'
            self.drop_down()

    def _on_focus_out_dropdown_window(self, event):
        """Withdraw drop-down window when it looses focus."""
        if self.focus_get() is not None:
            if self.focus_get() == self:
                x, y = event.x, event.y
                if (type(x) != int or type(y) != int or self.identify(x, y) != self._downarrow_name):
                    self.dropdown_window.withdraw()
                    self.state(['!pressed'])
            else:
                self.dropdown_window.withdraw()
                self.state(['!pressed'])
        elif self.grab_current():
            # 'active' won't be in state because of the grab
            x, y = self.dropdown_window.winfo_pointerxy()
            xc = self.dropdown_window.winfo_rootx()
            yc = self.dropdown_window.winfo_rooty()
            w = self.dropdown_window.winfo_width()
            h = self.dropdown_window.winfo_height()
            if xc <= x <= xc + w and yc <= y <= yc + h:
                # re-focus dropdown_window so that <FocusOut> will be triggered next time
                self.dropdown_window.focus_force()
            else:
                self.dropdown_window.withdraw()
                self.state(['!pressed'])
        else:
            if 'active' in self.state():
                # re-focus dropdown_window so that <FocusOut> will be triggered next time
                self.dropdown_window.focus_force()
            else:
                self.dropdown_window.withdraw()
                self.state(['!pressed'])

    def set(self, value):
        """Insert text in the entry."""
        self.value = value
        if 'readonly' in self.state():
            readonly = True
            self.state(('!readonly',))
        else: readonly = False

        value = self.getValue(value)
        self.WidgetClass.set(self, value)
        if readonly: self.state(('readonly',))

    def getValue(self, value):
        if self.attr: value = getattr(value, self.attr, None)
        if self.valueType: value = self.valueType(value)
        return value

    def destroy(self):
        try: self.after_cancel(self._determine_downarrow_name_after_id)
        except ValueError: pass
        self.WidgetClass.destroy(self)

    def drop_down(self, event=None):
        """Display or withdraw the drop_down window depending on its current state."""

        if self.dropdown_window.winfo_ismapped(): self.dropdown_window.withdraw()
        else:
            if self.validate_cmd: self.validate_cmd()
            x = self.winfo_rootx()
            h = self.winfo_height()
            y = self.winfo_rooty()
            py = y + h

            if self.geo: self.dropdown_window.size((*self.geo, x, py))
            get = self.get()

            if get: self.dropdown_window.set(get)

            self.dropdown_window.focus_set()
            self.dropdown_window.deiconify()

    def configure(self, cnf={}, **kw):
        """
        Configure resources of a widget.

        The values for resources are specified as keyword
        arguments. To get an overview about
        the allowed keyword arguments call the method :meth:`~PRMP_DropDownEntry.keys`.
        """
        if not isinstance(cnf, dict):
            raise TypeError("Expected a dictionary or keyword arguments.")

        dropdown_windowkwargs = kw.pop('ddwk', {}) or kw.pop('dropdown_windowkwargs', {})
        self.WidgetClass.configure(self, **kw)

        if self.dropdown_window: self.dropdown_window.configure(**dropdown_windowkwargs)

    def config(self, *args, **kwargs): return self.configure(*args, **kwargs)

    def get(self):
        try: get_ = self.dropdown_window.validate_cmd(self.value)
        except: get_ = None

        if get_: self.value = get_
        return self.value
DDW = PRMP_DropDownWidget

class PRMP_DropDownEntry(PRMP_DropDownWidget, SEntry):

    entry_kw = {'cursor': 'xterm', 'style': 'dropdownEntry.TCombobox'}
    WidgetClass = SEntry

    def __init__(self, master=None, **kwargs):

        # sort keywords between entry options and calendar options
        entry_kw = {}

        style = kwargs.pop('style', self.entry_kw['style'])

        for key in self.entry_kw: entry_kw[key] = kwargs.pop(key, self.entry_kw[key])

        entry_kw['font'] = kwargs.get('font', None)
        self._cursor = entry_kw['cursor']

        entry_kw.update(kwargs.pop('config', {}))

        super().__init__(master, config=entry_kw, **kwargs)
        self.bind('<Motion>', self._on_motion, '+')

    def _on_b1_press(self, event):
        """Trigger self.drop_down on downarrow button press and set widget state to ['pressed', 'active']."""
        x, y = event.x, event.y
        if self.identify(x, y) == self._downarrow_name: super()._on_b1_press()

    def _on_motion(self, event):
        """Set widget state depending on mouse position to mimic Combobox behavior."""
        x, y = event.x, event.y
        if 'disabled' not in self.state():
            if self.identify(x, y) == self._downarrow_name:
                self.state(['active'])
                ttk.Entry.configure(self, cursor='arrow')
            else:
                self.state(['!active'])
                ttk.Entry.configure(self, cursor=self._cursor)

    def state(self, args=''):
        """
        Modify or inquire widget state.

        Widget state is returned if statespec is None, otherwise it is
        set according to the statespec flags and then a new state spec
        is returned indicating which flags were changed. statespec is
        expected to be a sequence.
        """
        # change cursor depending on state to mimic Combobox behavior
        if 'disabled' in args or 'readonly' in args: self.configure(cursor='arrow')
        elif '!disabled' in args or '!readonly' in args: self.configure(cursor='xterm')
        return super().state(args)

    def configure(self, cnf={}, **kw):
        kwargs = cnf.copy()
        kwargs.update(kw)

        entry_kw = {}
        keys = list(kwargs.keys())
        for key in keys:
            if key in self.entry_kw: entry_kw[key] = kwargs.pop(key)
        font = kwargs.get('font', None)

        if font is not None: entry_kw['font'] = font

        self._cursor = str(entry_kw.get('cursor', self._cursor))
        if entry_kw.get('state') == 'readonly' and self._cursor == 'xterm' and 'cursor' not in entry_kw:
            entry_kw['cursor'] = 'arrow'
            self._cursor  = 'arrow'

        self.WidgetClass.configure(self, entry_kw)
        super().configure(cnf=cnf, **kwargs)
DDE = DropDownEntry = PRMP_DropDownEntry

class PRMP_DropDownButton(PRMP_DropDownWidget, Button): WidgetClass = Button
DDB = DropDownButton = PRMP_DropDownButton

class PRMP_DropDownCheckbutton(PRMP_DropDownWidget, Checkbutton):
    WidgetClass = Checkbutton

    def getValue(self, val):
        val = super().getValue(val)
        self.configure(text=val)
        return val
DDCb = DropDownCheckbutton = PRMP_DropDownCheckbutton


class PRMP_DropDownCalendarWidget(PRMP_DropDownWidget):
    def __init__(self, *args, **kwargs):
        from .dialogs import PRMP_CalendarDialog

        super().__init__(*args, ddwc=PRMP_CalendarDialog, ddwk=dict(gaw=0, geo=(300, 250)), **kwargs)


class PRMP_DropDownCalendarEntry(PRMP_DropDownEntry):
    def __init__(self, *args, **kwargs):
        from .dialogs import PRMP_CalendarDialog

        super().__init__(*args, ddwc=PRMP_CalendarDialog, ddwk=dict(gaw=0, geo=(300, 250)), **kwargs)
