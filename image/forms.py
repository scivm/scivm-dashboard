# Copyright 2014 Science Automation
#
# This file is part of Science VM.
#
# Science VM is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# Science VM is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Science VM. If not, see <http://www.gnu.org/licenses/>.

from django import forms
from image.models import Image
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Button
from crispy_forms.bootstrap import FieldWithButtons, StrictButton, FormActions
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

class ImageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                None,
                'name',
                'description',
            ),
            FormActions(
                Submit('save', _('Add'), css_class="btn btn-lg btn-success"),
            )
        )
        self.helper.form_id = 'form-add-image'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_action = reverse('image.views.add_image')

    class Meta:
        model = Image
        fields = ('name', 'description')

#class EditImageForm(forms.Form):
#    name = forms.CharField(required=True)
#    description = forms.CharField(required=False)
#
#    def __init__(self, *args, **kwargs):
#        super(EditImageForm, self).__init__(*args, **kwargs)
#        self.helper = FormHelper()
#        self.helper.form_id = 'form-edit-image'
#        self.helper.form_class = 'form-horizontal'
#        self.helper.form_action = reverse('image.views.index')
#        self.helper.help_text_inline = True

class EditImageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditImageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                None,
                'name',
                'description',
            ),
            FormActions(
                Submit('save', _('Edit'), css_class="btn btn-lg btn-success"),
            )
        )
        self.helper.form_id = 'form-add-image'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_action = reverse('image.views.index')

    class Meta:
        model = Image
        fields = ('name', 'description')

