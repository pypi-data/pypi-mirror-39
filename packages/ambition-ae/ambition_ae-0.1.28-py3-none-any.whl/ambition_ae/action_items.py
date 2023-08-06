from ambition_prn.constants import DEATH_REPORT_ACTION
from ambition_subject.constants import BLOOD_RESULTS_ACTION
from django.utils.safestring import mark_safe
from edc_action_item import HIGH_PRIORITY, ActionWithNotification, site_action_items
from edc_constants.constants import CLOSED, DEAD, LOST_TO_FOLLOWUP, YES
from edc_reportable import GRADE3
from edc_visit_schedule.models.subject_schedule_history import SubjectScheduleHistory
from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from .constants import AE_FOLLOWUP_ACTION, AE_INITIAL_ACTION
from .constants import AE_TMG_ACTION, RECURRENCE_OF_SYMPTOMS_ACTION
from .constants import GRADE4, GRADE5
from .email_contacts import email_contacts


class BaseNonAeInitialAction(ActionWithNotification):
    parent_reference_model_fk_attr = 'ae_initial'
    show_link_to_changelist = True
    admin_site_name = 'ambition_ae_admin'
    priority = HIGH_PRIORITY


class AeTmgAction(BaseNonAeInitialAction):
    name = AE_TMG_ACTION
    display_name = 'TMG AE Report pending'
    notification_display_name = 'TMG AE Report'
    parent_action_names = [
        AE_INITIAL_ACTION,
        AE_FOLLOWUP_ACTION,
        AE_TMG_ACTION]
    reference_model = 'ambition_ae.aetmg'
    related_reference_model = 'ambition_ae.aeinitial'
    related_reference_fk_attr = 'ae_initial'
    create_by_user = False
    color_style = 'info'
    show_link_to_changelist = True
    admin_site_name = 'ambition_ae_admin'
    instructions = mark_safe(
        f'This report is to be completed by the TMG only.')

    def close_action_item_on_save(self):
        return self.reference_obj.report_status == CLOSED


class AeFollowupAction(BaseNonAeInitialAction):
    name = AE_FOLLOWUP_ACTION
    display_name = 'Submit AE Followup Report'
    notification_display_name = 'AE Followup Report'
    parent_action_names = [
        AE_INITIAL_ACTION,
        AE_FOLLOWUP_ACTION]
    reference_model = 'ambition_ae.aefollowup'
    related_reference_model = 'ambition_ae.aeinitial'
    related_reference_fk_attr = 'ae_initial'
    create_by_user = False
    show_link_to_changelist = True
    admin_site_name = 'ambition_ae_admin'
    instructions = mark_safe(
        f'Upon submission the TMG group will be notified '
        f'by email at <a href="mailto:{email_contacts.get("tmg")}">'
        f'{email_contacts.get("tmg")}</a>')

    def get_offschedule_action_cls(self):
        """Returns the action class for the offschedule model.
        """
        action_cls = None
        for onschedule_model_obj in SubjectScheduleHistory.objects.onschedules(
                subject_identifier=self.subject_identifier,
                report_datetime=self.reference_obj.report_datetime):
            _, schedule = site_visit_schedules.get_by_onschedule_model(
                onschedule_model=onschedule_model_obj._meta.label_lower)
            offschedule_model = schedule.offschedule_model
            action_cls = site_action_items.get_by_model(
                model=offschedule_model)
        return action_cls

    def get_next_actions(self):
        next_actions = []

        # add next AE followup
        next_actions = self.append_to_next_if_required(
            next_actions=next_actions,
            action_name=self.name,
            required=self.reference_obj.followup == YES)

        # add next AeTmg if severity increased
        next_actions = self.append_to_next_if_required(
            next_actions=next_actions,
            action_name=AE_TMG_ACTION,
            required=self.reference_obj.ae_grade in [GRADE4])

        # add next Death report if G5/Death
        next_actions = self.append_to_next_if_required(
            next_actions=next_actions,
            action_name=DEATH_REPORT_ACTION,
            required=(
                self.reference_obj.outcome == DEAD
                or self.reference_obj.ae_grade == GRADE5))

        # add next AE TMG if G5/Death
        next_actions = self.append_to_next_if_required(
            next_actions=next_actions,
            action_name=AE_TMG_ACTION,
            required=(
                self.reference_obj.outcome == DEAD
                or self.reference_obj.ae_grade == GRADE5))

        # add next Study termination if LTFU
        offschedule_action_cls = self.get_offschedule_action_cls()
        if offschedule_action_cls:  # TODO: fix for tests - only None in tests
            next_actions = self.append_to_next_if_required(
                next_actions=next_actions,
                action_name=offschedule_action_cls.name,
                required=self.reference_obj.outcome == LOST_TO_FOLLOWUP)
        return next_actions


class AeInitialAction(ActionWithNotification):
    name = AE_INITIAL_ACTION
    display_name = 'Submit AE Initial Report'
    notification_display_name = 'AE Initial Report'
    parent_action_names = [BLOOD_RESULTS_ACTION]
    reference_model = 'ambition_ae.aeinitial'
    show_link_to_changelist = True
    show_link_to_add = True
    admin_site_name = 'ambition_ae_admin'
    instructions = 'Complete the initial AE report'
    priority = HIGH_PRIORITY

    def get_next_actions(self):
        """Returns next actions.

        1. Add death report action if death
        2.
        """
        next_actions = []
        deceased = (
            self.reference_obj.ae_grade == GRADE5
            or self.reference_obj.sae_reason == DEAD)

        # add next AeFollowup if not deceased
        if not deceased:
            next_actions = self.append_to_next_if_required(
                action_name=AE_FOLLOWUP_ACTION,
                next_actions=next_actions)

        # add next Death report if G5/Death
        next_actions = self.append_to_next_if_required(
            next_actions=next_actions,
            action_name=DEATH_REPORT_ACTION,
            required=deceased)
        # add next AE Tmg if G5/Death
        next_actions = self.append_to_next_if_required(
            next_actions=next_actions,
            action_name=AE_TMG_ACTION,
            required=deceased)
        # add next AeTmgAction if G4
        next_actions = self.append_to_next_if_required(
            next_actions=next_actions,
            action_name=AE_TMG_ACTION,
            required=self.reference_obj.ae_grade == GRADE4)
        # add next AeTmgAction if G3 and is an SAE
        next_actions = self.append_to_next_if_required(
            next_actions=next_actions,
            action_name=AE_TMG_ACTION,
            required=(self.reference_obj.ae_grade == GRADE3
                      and self.reference_obj.sae == YES))
        # add next Recurrence of Symptoms if YES
        next_actions = self.append_to_next_if_required(
            next_actions=next_actions,
            action_name=RECURRENCE_OF_SYMPTOMS_ACTION,
            required=self.reference_obj.ae_cm_recurrence == YES)
        return next_actions


class RecurrenceOfSymptomsAction(ActionWithNotification):
    name = RECURRENCE_OF_SYMPTOMS_ACTION
    display_name = 'Submit Recurrence of Symptoms Report'
    notification_display_name = 'Recurrence of Symptoms Report'
    parent_action_names = [AE_INITIAL_ACTION]
    reference_model = 'ambition_ae.recurrencesymptom'
    show_link_to_changelist = True
    admin_site_name = 'ambition_ae_admin'
    priority = HIGH_PRIORITY
    create_by_user = False
    help_text = 'This document is triggered by AE Initial'


site_action_items.register(AeInitialAction)
site_action_items.register(AeTmgAction)
site_action_items.register(AeFollowupAction)
site_action_items.register(RecurrenceOfSymptomsAction)
