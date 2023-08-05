# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class JQuerySlider(Component):
    """A JQuerySlider component.


Keyword arguments:
- id (string; optional): The ID used to identify this compnent in Dash callbacks
- opacity (number; optional)
- enable (boolean; optional)

Available events: """
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, opacity=Component.UNDEFINED, enable=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'opacity', 'enable']
        self._type = 'JQuerySlider'
        self._namespace = 'pwbmcomponents'
        self._valid_wildcard_attributes =            []
        self.available_events = []
        self.available_properties = ['id', 'opacity', 'enable']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(JQuerySlider, self).__init__(**args)

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
            return ('JQuerySlider(' + props_string +
                   (', ' + wilds_string if wilds_string != '' else '') + ')')
        else:
            return (
                'JQuerySlider(' +
                repr(getattr(self, self._prop_names[0], None)) + ')')
