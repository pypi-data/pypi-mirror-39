# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ImageBox(Component):
    """A ImageBox component.
ImageBox is a component that encapsulates several nuclei image items.

Keyword arguments:
- id (string; optional)
- className (string; optional): The class of image box
- style (dict; optional): The style of the container (div)
- data (optional): The data of nuclei. data has the following type: dict containing keys 'src', 'masks'.
Those keys have the following types: 
  - src (string; optional): The image source url
  - masks (list; optional): An array of masks
- prob (number; optional): The currently selected probability threshold
- filter (boolean; optional): Filter by label or not
- width (number; optional): The image box render width/height
- channel (list; optional): An array of options
- cell (list; optional): An array of options
- enhance (list; optional): An array of options
- clickData (dict; optional): Data from latest click event
- coordinate (boolean; optional): Show coordinate location or not

Available events: """
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, data=Component.UNDEFINED, prob=Component.UNDEFINED, filter=Component.UNDEFINED, width=Component.UNDEFINED, channel=Component.UNDEFINED, cell=Component.UNDEFINED, enhance=Component.UNDEFINED, clickData=Component.UNDEFINED, coordinate=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'className', 'style', 'data', 'prob', 'filter', 'width', 'channel', 'cell', 'enhance', 'clickData', 'coordinate']
        self._type = 'ImageBox'
        self._namespace = 'dashx'
        self._valid_wildcard_attributes =            []
        self.available_events = []
        self.available_properties = ['id', 'className', 'style', 'data', 'prob', 'filter', 'width', 'channel', 'cell', 'enhance', 'clickData', 'coordinate']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(ImageBox, self).__init__(**args)

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
            return ('ImageBox(' + props_string +
                   (', ' + wilds_string if wilds_string != '' else '') + ')')
        else:
            return (
                'ImageBox(' +
                repr(getattr(self, self._prop_names[0], None)) + ')')
