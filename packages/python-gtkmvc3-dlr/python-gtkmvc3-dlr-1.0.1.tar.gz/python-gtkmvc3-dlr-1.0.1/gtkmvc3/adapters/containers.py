#  Author: Roberto Cavada <roboogle@gmail.com>
#
#  Copyright (C) 2007-2015 by Roberto Cavada
#
#  gtkmvc3 is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2 of the License, or (at your option) any later version.
#
#  gtkmvc3 is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110, USA.
#
#  For more information on gtkmvc3 see <https://github.com/roboogle/gtkmvc3>
#  or email to the author Roberto Cavada <roboogle@gmail.com>.
#  Please report bugs to <https://github.com/roboogle/gtkmvc3/issues>
#  or to <roboogle@gmail.com>.


import types
import weakref
from gi.repository import Gtk

from gtkmvc3.adapters.basic import UserClassAdapter, Adapter

from gtkmvc3.adapters.default import *
from gtkmvc3.observer import Observer
from gtkmvc3.support.wrappers import ObsMapWrapper

# this tries solving the issue in gtk about Builder not setting name
# correctly. See https://bugzilla.gnome.org/show_bug.cgi?id=591085
def _get_name(widget):
    try:
        # Will be kind instead of name if it wasn't loaded from XML :(
        return Gtk.Buildable.get_name(widget)
    except AttributeError:
        # Gtk is too old.
        pass

    raise NotImplementedError("StaticContainerAdapter doesn't support "
                              "manually created widgets")


# ----------------------------------------------------------------------
class StaticContainerAdapter (UserClassAdapter):
    """
    This class can be used to bound a set of widgets to a property
    that is a container, like a tuple, a list or a map, or in
    general a class that implements __getitem__ and __setitem__
    methods.

    From the other hand, the set of widgets can be a list provided
    by the user, or a container widget like a Box, a notebook, etc.
    Widgets will be linked by their position when the property is
    list-like, or by their name when the property is map-like.

    This class supports only properties that are static containers,
    i.e. those containers that do not change their length
    dynamically. If the container grows up in length, no change will
    occur in the view-side.
    """
    def __init__(self, model, prop_name,
                 prop_read=None, prop_write=None, value_error=None,
                 spurious=False):

        UserClassAdapter.__init__(self, model, prop_name,
                                  lambda c,i: c.__getitem__(i),
                                  lambda c,v,i: c.__setitem__(i,v),
                                  prop_read, prop_write,
                                  value_error, spurious)

        prop =  Adapter._get_property(self)

        #prop =  self._get_property() # bug fix reported by A. Dentella
        if not (hasattr(prop, "__getitem__") and
                hasattr(prop, "__setitem__")):
            # before giving up, unregisters itself as an observer
            # TODO also tear down Intermediate instances
            self.relieve_model(model)
            raise TypeError("Property " + self._prop_name +
                            " is not a valid container")


        self._prop_is_map = isinstance(prop, dict) or \
                            isinstance(prop, ObsMapWrapper)
        # contained widgets
        self._idx2wid = {}
        self._wid2idx = {}

        self._widgets = None
        return


    def connect_widget(self, wid, getters=None, setters=None,
                       signals=None, arg=None,
                       flavours=None):
        """
        Called when the widget is instantiated, and the adapter is
        ready to connect the widgets inside it (if a container) or
        each widget if wid is a list of widgets. getters and setters
        can be None, a function or a list or a map of
        functions. signals can be None, a signal name, or a list or
        a map of signal names. When maps are used, keys can be
        widgets or widget names. The length of the possible lists or
        maps must be lesser or equal to the number of widgets that
        will be connected.
        """

        if isinstance(wid, Gtk.Container):
            self._widgets = wid.get_children()
        elif isinstance(wid, (list, tuple)):
            self._widgets = wid
        else:
            raise TypeError("widget must be either a Gtk.Container or a list or tuple")

        # prepares the mappings:
        for idx, w in enumerate(self._widgets):
            if self._prop_is_map: idx=_get_name(w)
            self._idx2wid[idx] = w
            self._wid2idx[w] = idx
            pass

        # prepares the lists for signals
        getters = self.__handle_par("getters", getters)
        setters = self.__handle_par("setters", setters)
        signals = self.__handle_par("signals", signals)
        flavours = self.__handle_par("flavours", flavours)

        for wi,ge,se,si,fl in zip(self._widgets, getters, setters, signals, flavours):
            if type(ge) == types.MethodType: ge = ge.im_func
            if type(se) == types.MethodType: se = se.im_func
            UserClassAdapter.connect_widget(self, wi, ge, se, si, arg, False, fl)
            pass

        self.update_widget()
        self._wid = wid
        return


    def update_model(self, idx=None):
        """Updates the value of property at given index. If idx is
        None, all controlled indices will be updated. This method
        should be called directly by the user in very unusual
        conditions."""
        if idx is None:
            for w in self._widgets:
                idx = self._get_idx_from_widget(w)
                try: val = self._read_widget(idx)
                except ValueError: pass
                else: self._write_property(val, idx)
                pass
            pass
        else:
            try: val = self._read_widget(idx)
            except ValueError: pass
            else: self._write_property(val, idx)
        return

    def update_widget(self, idx=None):
        """Forces the widget at given index to be updated from the
        property value. If index is not given, all controlled
        widgets will be updated. This method should be called
        directly by the user when the property is not observable, or
        in very unusual conditions."""
        if idx is None:
            for w in self._widgets:
                idx = self._get_idx_from_widget(w)
                self._write_widget(self._read_property(idx), idx)
            pass
        else: self._write_widget(self._read_property(idx), idx)
        return

    # ----------------------------------------------------------------------
    # Private methods
    # ----------------------------------------------------------------------

    def _get_idx_from_widget(self, wid):
        """Given a widget, returns the corresponding index for the
        model. Returned value can be either an integer or a string"""
        return self._wid2idx[wid]

    def _get_widget_from_idx(self, idx):
        """Given an index, returns the corresponding widget for the view.
        Given index can be either an integer or a string"""
        return self._idx2wid[idx]


    def _read_widget(self, idx):
        sav = self._wid
        self._wid = self._get_widget_from_idx(idx)
        val = UserClassAdapter._read_widget(self)
        self._wid = sav
        return val

    def _write_widget(self, val, idx):
        sav = self._wid
        self._wid = self._get_widget_from_idx(idx)
        UserClassAdapter._write_widget(self, val)
        self._wid = sav
        return

    # This is a private service to factorize code of connect_widget
    def __handle_par(self, name, par):
        if par is None or type(par) in (types.FunctionType,
                                        types.MethodType, str):
            par = [par] * len(self._widgets)
            pass

        elif isinstance(par, dict):
            val = []
            for w in self._widgets:
                if w in par: val.append(par[w])
                elif _get_name(w) in par: val.append(par[_get_name(w)])
                else: val.append(None)
                pass
            par = val
            pass

        elif isinstance(par, list) or isinstance(par, tuple):
            par = list(par)
            par.extend([None]*(len(self._widgets)-len(par)))
            pass

        else: raise TypeError("Parameter %s has an invalid type (should be None, a sequence or a string)" % name)

        return par


    # Callbacks:
    def _on_wid_changed(self, wid):
        """Called when the widget is changed"""
        if self._itsme: return
        self.update_model(self._get_idx_from_widget(wid))
        return

    def _on_prop_changed(self, instance, meth_name, res, args, kwargs):
        """Called by the observation code, we are interested in
        __setitem__"""
        if  not self._itsme and meth_name == "__setitem__": self.update_widget(args[0])
        return

    pass # end of class StaticContainerAdapter

class watch_items_in_tree(Observer):
    def __init__(self, tree, column=0):
        """
        Observe models stored in a list for assignment to their observable
        properties, and notify the container that the row has changed.

        *tree* is a :class:`Gtk.TreeModel` instance.

        *column* is an integer adressing the column of *tree* that contains
        :class:`gtkmvc3.Model` instances.
        """
        Observer.__init__(self)
        self.column = column
        self.rows = weakref.WeakKeyDictionary()
        tree.foreach(self.on_changed)
        tree.connect('row-changed', self.on_changed)

    def on_changed(self, tree, path, iter):
        item = tree.get_value(iter, self.column)
        if item:
            self.rows[item] = Gtk.TreeRowReference.new(model=tree, path=path)
            item.register_observer(self)
        return False

    @Observer.observe('*', assign=True)
    def on_assign(self, item, prop_name, info):
        row = self.rows[item]
        if row.valid():
            path = row.get_path()
            tree = row.get_model()
            iter = tree.get_iter(path)
            tree.row_changed(path, iter)
        else:
            item.unregister_observer(self)
            del self.rows[item]
