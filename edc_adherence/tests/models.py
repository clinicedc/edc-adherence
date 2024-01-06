from django.db import models
from django.db.models import PROTECT
from edc_appointment.models import Appointment
from edc_crf.model_mixins import CrfModelMixin, CrfWithActionModelMixin
from edc_identifier.managers import SubjectIdentifierManager
from edc_list_data.model_mixins import ListModelMixin
from edc_metadata.model_mixins.creates import CreatesMetadataModelMixin
from edc_model import models as edc_models
from edc_model.models import BaseUuidModel
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin
from edc_screening.model_mixins import ScreeningModelMixin
from edc_sites.model_mixins import SiteModelMixin
from edc_utils import get_utcnow
from edc_visit_tracking.constants import SCHEDULED
from edc_visit_tracking.model_mixins import (
    SubjectVisitMissedModelMixin,
    VisitModelMixin,
)

from edc_adherence.model_mixins import MedicationAdherenceModelMixin


class DeathReport(edc_models.BaseUuidModel):
    subject_identifier = models.CharField(max_length=50)


class OffStudy(edc_models.BaseUuidModel):
    subject_identifier = models.CharField(max_length=50)

    offstudy_datetime = models.DateTimeField(default=get_utcnow)


class SubjectScreening(ScreeningModelMixin, BaseUuidModel):
    objects = SubjectIdentifierManager()


class SubjectConsent(UpdatesOrCreatesRegistrationModelMixin, edc_models.BaseUuidModel):
    subject_identifier = models.CharField(max_length=50)

    consent_datetime = models.DateTimeField()

    dob = models.DateTimeField(null=True)


class OnSchedule(SiteModelMixin, edc_models.BaseUuidModel):
    subject_identifier = models.CharField(max_length=50)

    onschedule_datetime = models.DateTimeField(default=get_utcnow)


class OffSchedule(SiteModelMixin, edc_models.BaseUuidModel):
    subject_identifier = models.CharField(max_length=50)

    offschedule_datetime = models.DateTimeField(default=get_utcnow)


class SubjectVisit(
    VisitModelMixin,
    CreatesMetadataModelMixin,
    SiteModelMixin,
    BaseUuidModel,
):
    appointment = models.OneToOneField(
        Appointment, on_delete=PROTECT, related_name="edc_adherence_appointment"
    )

    subject_identifier = models.CharField(max_length=50)

    reason = models.CharField(max_length=25, default=SCHEDULED)


class SubjectVisitMissedReasons(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Subject Missed Visit Reasons"
        verbose_name_plural = "Subject Missed Visit Reasons"


class SubjectVisitMissed(
    SubjectVisitMissedModelMixin,
    CrfWithActionModelMixin,
    BaseUuidModel,
):
    missed_reasons = models.ManyToManyField(
        SubjectVisitMissedReasons, blank=True, related_name="+"
    )

    class Meta(
        SubjectVisitMissedModelMixin.Meta,
        BaseUuidModel.Meta,
    ):
        verbose_name = "Missed Visit Report"
        verbose_name_plural = "Missed Visit Report"


class MedicationAdherence(
    MedicationAdherenceModelMixin, CrfModelMixin, edc_models.BaseUuidModel
):
    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Medication Adherence"
        verbose_name_plural = "Medication Adherence"
