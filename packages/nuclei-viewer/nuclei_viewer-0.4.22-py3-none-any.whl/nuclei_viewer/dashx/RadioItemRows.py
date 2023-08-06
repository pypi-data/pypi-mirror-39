# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class RadioItemRows(Component):
    """A RadioItemRows component.
RadioItemRows is a component that encapsulates several radio item inputs.
The values and labels of the RadioItemRows is specified in the `options`
property and the seleced item is specified with the `value` property.
Each radio item is rendered as an input with a surrounding label.

Keyword arguments:
- id (string; optional)
- options (list; optional): An array of options
- value (string; optional): The currently selected value
- style (dict; optional): The style of the container (div)
- className (string; optional): The class of the container (div)

Available events: """
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, options=Component.UNDEFINED, value=Component.UNDEFINED, style=Component.UNDEFINED, className=Component.UNDEFINED, onChange=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'options', 'value', 'style', 'className']
        self._type = 'RadioItemRows'
        self._namespace = 'dashx'
        self._valid_wildcard_attributes =            []
        self.available_events = []
        self.available_properties = ['id', 'options', 'value', 'style', 'className']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(RadioItemRows, self).__init__(**args)

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
            return ('RadioItemRows(' + props_string +
                   (', ' + wilds_string if wilds_string != '' else '') + ')')
        else:
            return (
                'RadioItemRows(' +
                repr(getattr(self, self._prop_names[0], None)) + ')')
