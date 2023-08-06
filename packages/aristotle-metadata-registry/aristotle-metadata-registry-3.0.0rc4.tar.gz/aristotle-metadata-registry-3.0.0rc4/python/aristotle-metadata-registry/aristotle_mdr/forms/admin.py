from django import VERSION as django_version
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

import aristotle_mdr.models as MDR
import aristotle_mdr.widgets.widgets as widgets
from aristotle_mdr.contrib.autocomplete.widgets import ConceptAutocompleteSelectMultiple
from aristotle_mdr.perms import user_can_edit
from aristotle_mdr.utils import concept_to_clone_dict
from aristotle_mdr.forms.creation_wizards import WorkgroupVerificationMixin, ConceptForm


def MembershipField(model, name):
    return forms.ModelMultipleChoiceField(
        queryset=model.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(name, False)
    )


class AristotleProfileForm(forms.ModelForm):
    steward_in = MembershipField(MDR.Workgroup, _('workgroups'))
    submitter_in = MembershipField(MDR.Workgroup, _('workgroups'))
    viewer_in = MembershipField(MDR.Workgroup, _('workgroups'))
    workgroup_manager_in = MembershipField(MDR.Workgroup, _('workgroups'))

    organization_manager_in = MembershipField(MDR.Organization, 'organizations')
    registrar_in = MembershipField(MDR.RegistrationAuthority, _('registration authorities'))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # if self.instance and self.instance.user.count() == 1: # and self.instance.user.exists():
        try:
            self.fields['registrar_in'].initial = self.instance.user.registrar_in.all()
            self.fields['organization_manager_in'].initial = self.instance.user.organization_manager_in.all()

            self.fields['workgroup_manager_in'].initial = self.instance.user.workgroup_manager_in.all()
            self.fields['steward_in'].initial = self.instance.user.steward_in.all()
            self.fields['submitter_in'].initial = self.instance.user.submitter_in.all()
            self.fields['viewer_in'].initial = self.instance.user.viewer_in.all()
        except get_user_model().DoesNotExist:
            pass

    def save_memberships(self, user, *args, **kwargs):
        if "workgroup_manager_in" in self.cleaned_data.keys():
            user.workgroup_manager_in = self.cleaned_data['workgroup_manager_in']
        if "submitter_in" in self.cleaned_data.keys():
            user.submitter_in = self.cleaned_data['submitter_in']
        if "steward_in" in self.cleaned_data.keys():
            user.steward_in = self.cleaned_data['steward_in']
        if "viewer_in" in self.cleaned_data.keys():
            user.viewer_in = self.cleaned_data['viewer_in']

        if "organization_manager_in" in self.cleaned_data.keys():
            user.organization_manager_in = self.cleaned_data['organization_manager_in']
        if "registrar_in" in self.cleaned_data.keys():
            user.registrar_in = self.cleaned_data['registrar_in']


class AdminConceptForm(ConceptForm, WorkgroupVerificationMixin):
    # Thanks: http://stackoverflow.com/questions/6034047/one-to-many-inline-select-with-django-admin
    # Although concept is an abstract class, we still need this to have a reverse one-to-many edit field.
    class Meta:
        model = MDR._concept
        fields = "__all__"
        exclude = ["superseded_by_items", "superseded_items"]

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request', None)
        clone = self.request.GET.get("clone", None)
        name_suggest_fields = kwargs.pop('name_suggest_fields', [])
        separator = kwargs.pop('separator', '-')
        if clone:
            item_to_clone = MDR._concept.objects.filter(id=clone).first().item
            kwargs['initial'] = concept_to_clone_dict(item_to_clone)

        super().__init__(*args, **kwargs)
        if self.instance and not clone:
            self.itemtype = self.instance.__class__

        if name_suggest_fields:
            self.fields['name'].widget = widgets.NameSuggestInput(name_suggest_fields=name_suggest_fields, separator=separator)
        self.fields['workgroup'].queryset = self.request.user.profile.editable_workgroups.all()
        # self.fields['workgroup'].initial = self.request.user.profile.activeWorkgroup


class StatusInlineForm(forms.ModelForm):
    registrationAuthority = forms.ModelChoiceField(
        label='Registration Authority',
        queryset=MDR.RegistrationAuthority.objects.filter(active=0),
        widget=widgets.RegistrationAuthoritySelect
    )

    class Meta:
        model = MDR.Status
        fields = "__all__"
