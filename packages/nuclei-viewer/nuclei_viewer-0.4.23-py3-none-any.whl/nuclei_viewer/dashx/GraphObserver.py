# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class GraphObserver(Component):
    """A GraphObserver component.
GraphObserver is a component that handle event of graph figure.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The children of this component
- id (string; optional)
- cell (string; optional): The target cell type
- clickData (dict; optional): Data from latest click event
- color (dict; optional): Color code

Available events: """
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, cell=Component.UNDEFINED, clickData=Component.UNDEFINED, color=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'cell', 'clickData', 'color']
        self._type = 'GraphObserver'
        self._namespace = 'dashx'
        self._valid_wildcard_attributes =            []
        self.available_events = []
        self.available_properties = ['children', 'id', 'cell', 'clickData', 'color']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(GraphObserver, self).__init__(children=children, **args)

    def __repr__(self):
        if(any(getattr(self, c, None) is not None
               for c in self._prop_names
               if c is not self._prop_names[0])
           or any(getattr(self, c, None) is not None
                  for c in self.__dict__.keys()
                  if any(c.startswith(wc_attr)
                  for wc_attr in self._valid_wildcard_attributes))):
            props_string = ', '.join([c+'='+repr(getattr(self, c, None))
                                      for c in self._prop_names
                                      if getattr(self, c, None) is not None])
            wilds_string = ', '.join([c+'='+repr(getattr(self, c, None))
                                      for c in self.__dict__.keys()
                                      if any([c.startswith(wc_attr)
                                      for wc_attr in
                                      self._valid_wildcard_attributes])])
            return ('GraphObserver(' + props_string +
                   (', ' + wilds_string if wilds_string != '' else '') + ')')
        else:
            return (
                'GraphObserver(' +
                repr(getattr(self, self._prop_names[0], None)) + ')')
