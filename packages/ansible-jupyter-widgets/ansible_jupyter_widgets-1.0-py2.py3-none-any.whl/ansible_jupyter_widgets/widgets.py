import ipywidgets as widgets
from traitlets import Unicode, HasTraits


class VarNamed(HasTraits):
    var_name = Unicode('widget').tag(sync=True)


class Button(widgets.Button, VarNamed):
    pass


class FloatText(widgets.FloatText, VarNamed):
    pass


class BoundedFloatText(widgets.BoundedFloatText, VarNamed):
    pass


class FloatSlider(widgets.FloatSlider, VarNamed):
    pass


class FloatProgress(widgets.FloatProgress, VarNamed):
    pass


class FloatRangeSlider(widgets.FloatRangeSlider, VarNamed):
    pass


class IntText(widgets.IntText, VarNamed):
    pass


class BoundedIntText(widgets.BoundedIntText, VarNamed):
    pass


class IntSlider(widgets.IntSlider, VarNamed):
    pass


class IntProgress(widgets.IntProgress, VarNamed):
    pass


class IntRangeSlider(widgets.IntRangeSlider, VarNamed):
    pass


class ColorPicker(widgets.ColorPicker, VarNamed):
    pass


class DatePicker(widgets.DatePicker, VarNamed):
    pass


class RadioButtons(widgets.RadioButtons, VarNamed):
    pass


class ToggleButtons(widgets.ToggleButtons, VarNamed):
    pass


class Dropdown(widgets.Dropdown, VarNamed):
    pass


class Select(widgets.Select, VarNamed):
    pass


class SelectionSlider(widgets.SelectionSlider, VarNamed):
    pass


class SelectMultiple(widgets.SelectMultiple, VarNamed):
    pass


class SelectionRangeSlider(widgets.SelectionRangeSlider, VarNamed):
    pass


class Text(widgets.Text, VarNamed):
    pass


class Textarea(widgets.Textarea, VarNamed):
    pass


class Password(widgets.Password, VarNamed):
    pass
