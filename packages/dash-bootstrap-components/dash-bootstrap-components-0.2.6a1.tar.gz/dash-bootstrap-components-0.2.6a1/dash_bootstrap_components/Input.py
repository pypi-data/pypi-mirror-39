# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Input(Component):
    """A Input component.


Keyword arguments:
- id (string; optional): The ID of this component, used to identify dash components
in callbacks. The ID needs to be unique across all of the
components in an app.
- style (dict; optional): Defines CSS styles which will override styles previously set.
- className (string; optional): Often used with CSS to style elements with common properties.
- type (a value equal to: "text", 'textarea', 'number', 'password', 'email', 'range', 'search', 'tel', 'url', 'hidden'; optional)
- value (string; optional)
- size (string; optional)
- bs_size (string; optional)
- valid (boolean; optional)
- invalid (boolean; optional)
- plaintext (boolean; optional)
- addon (boolean; optional)
- placeholder (string; optional)
- name (string; optional)

Available events: """
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, style=Component.UNDEFINED, className=Component.UNDEFINED, type=Component.UNDEFINED, value=Component.UNDEFINED, size=Component.UNDEFINED, bs_size=Component.UNDEFINED, valid=Component.UNDEFINED, invalid=Component.UNDEFINED, plaintext=Component.UNDEFINED, addon=Component.UNDEFINED, placeholder=Component.UNDEFINED, name=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'style', 'className', 'type', 'value', 'size', 'bs_size', 'valid', 'invalid', 'plaintext', 'addon', 'placeholder', 'name']
        self._type = 'Input'
        self._namespace = 'dash_bootstrap_components'
        self._valid_wildcard_attributes =            []
        self.available_events = []
        self.available_properties = ['id', 'style', 'className', 'type', 'value', 'size', 'bs_size', 'valid', 'invalid', 'plaintext', 'addon', 'placeholder', 'name']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Input, self).__init__(**args)

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
            return ('Input(' + props_string +
                   (', ' + wilds_string if wilds_string != '' else '') + ')')
        else:
            return (
                'Input(' +
                repr(getattr(self, self._prop_names[0], None)) + ')')
