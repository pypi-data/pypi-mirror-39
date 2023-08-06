# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Dropdown(Component):
    """A Dropdown component.
Dropdown is an interactive dropdown element for selecting one or more
items.
The values and labels of the dropdown items are specified in the `options`
property and the selected item(s) are specified with the `value` property.

Use a dropdown when you have many options (more than 5) or when you are
constrained for space. Otherwise, you can use RadioItems or a Checklist,
which have the benefit of showing the users all of the items at once.

Keyword arguments:
- id (string; optional)
- options (list; optional): An array of options
- value (dict; optional): The value of the input.
- className (string; optional): The class of the React-Select component
- placeholder (string; optional): The grey, default text shown when no option is selected
- searchable (boolean; optional): Whether to enable the searching feature or not
- disabled (boolean; optional): Whether is disabled
- ellipsis (string; optional): Whether truncate label string

Available events: """
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, options=Component.UNDEFINED, value=Component.UNDEFINED, className=Component.UNDEFINED, placeholder=Component.UNDEFINED, searchable=Component.UNDEFINED, disabled=Component.UNDEFINED, ellipsis=Component.UNDEFINED, onChange=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'options', 'value', 'className', 'placeholder', 'searchable', 'disabled', 'ellipsis']
        self._type = 'Dropdown'
        self._namespace = 'dashx'
        self._valid_wildcard_attributes =            []
        self.available_events = []
        self.available_properties = ['id', 'options', 'value', 'className', 'placeholder', 'searchable', 'disabled', 'ellipsis']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Dropdown, self).__init__(**args)

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
            return ('Dropdown(' + props_string +
                   (', ' + wilds_string if wilds_string != '' else '') + ')')
        else:
            return (
                'Dropdown(' +
                repr(getattr(self, self._prop_names[0], None)) + ')')
