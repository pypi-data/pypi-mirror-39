# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Cropper(Component):
    """A Cropper component.
Cropper is a component that crop and resize image.

Keyword arguments:
- src (string; optional): The image source url
- width (number; optional): The image box render width/height
- zoom (number; optional): Zoom ratio
- coordinate (boolean; optional): Show coordinate location or not
- rect (list; optional): The rectangle of the nuclei. 
Eg. [x0, y0, x1, y1]

Available events: """
    @_explicitize_args
    def __init__(self, src=Component.UNDEFINED, width=Component.UNDEFINED, zoom=Component.UNDEFINED, coordinate=Component.UNDEFINED, rect=Component.UNDEFINED, **kwargs):
        self._prop_names = ['src', 'width', 'zoom', 'coordinate', 'rect']
        self._type = 'Cropper'
        self._namespace = 'dashx'
        self._valid_wildcard_attributes =            []
        self.available_events = []
        self.available_properties = ['src', 'width', 'zoom', 'coordinate', 'rect']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Cropper, self).__init__(**args)

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
            return ('Cropper(' + props_string +
                   (', ' + wilds_string if wilds_string != '' else '') + ')')
        else:
            return (
                'Cropper(' +
                repr(getattr(self, self._prop_names[0], None)) + ')')
