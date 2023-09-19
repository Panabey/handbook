from logging import getLogger

from django.db import router, transaction
from django.db.models import F, Value
from django.db.models.functions import Concat

from axes.attempts import clean_expired_user_attempts

from axes.conf import settings
from axes.helpers import (
    get_client_str,
    get_client_username,
    get_failure_limit,
    get_lockout_parameters,
    get_query_str,
)
from axes.models import AccessAttempt, AccessFailureLog
from axes.signals import user_locked_out

from axes.handlers.database import AxesDatabaseHandler

log = getLogger(__name__)


class AxesCustomHandler(AxesDatabaseHandler):
    def user_login_failed(self, sender, credentials: dict, request=None, **kwargs):
        """Переопределено чтобы избежать получения лишних данных в GET и POST form.

        Оригинальный код: https://github.com/jazzband/django-axes/blob/master/axes/handlers/database.py
        """

        if request is None:
            log.error(
                "AXES: AxesDatabaseHandler.user_login_failed does not function without a request."  # noqa: E501
            )
            return
        clean_expired_user_attempts(request.axes_attempt_time)

        username = get_client_username(request, credentials)
        client_str = get_client_str(
            username,
            request.axes_ip_address,
            request.axes_user_agent,
            request.axes_path_info,
            request,
        )

        if (
            not settings.AXES_RESET_COOL_OFF_ON_FAILURE_DURING_LOCKOUT
            and request.axes_locked_out
        ):
            request.axes_credentials = credentials
            user_locked_out.send(
                "axes",
                request=request,
                username=username,
                ip_address=request.axes_ip_address,
            )
            return

        if not settings.AXES_CLEAR_DATA:
            get_data = get_query_str(request.GET).replace("\0", "0x00")
            post_data = get_query_str(request.POST).replace("\0", "0x00")

        if self.is_whitelisted(request, credentials):
            log.info("AXES: Login failed from whitelisted client %s.", client_str)
            return

        lockout_parameters = get_lockout_parameters(request, credentials)
        if lockout_parameters == ["username"] and username is None:
            log.warning(
                "AXES: Username is None and username is the only one lockout parameter, new record will NOT be created."  # noqa: E501
            )
        else:
            with transaction.atomic(using=router.db_for_write(AccessAttempt)):
                (
                    attempt,
                    created,
                ) = AccessAttempt.objects.select_for_update().get_or_create(
                    username=username,
                    ip_address=request.axes_ip_address,
                    user_agent=request.axes_user_agent,
                    defaults={
                        "get_data": get_data if not settings.AXES_CLEAR_DATA else "",
                        "post_data": post_data if not settings.AXES_CLEAR_DATA else "",
                        "http_accept": request.axes_http_accept,
                        "path_info": request.axes_path_info,
                        "failures_since_start": 1,
                        "attempt_time": request.axes_attempt_time,
                    },
                )

                if created:
                    log.warning(
                        "AXES: New login failure by %s. Created new record in the database.",  # noqa: E501
                        client_str,
                    )

                else:
                    if not settings.AXES_CLEAR_DATA:
                        separator = "\n---------\n"

                        attempt.get_data = Concat(
                            "get_data", Value(separator + get_data)
                        )
                        attempt.post_data = Concat(
                            "post_data", Value(separator + post_data)
                        )
                    else:
                        attempt.get_data = ""
                        attempt.post_data = ""

                    attempt.http_accept = request.axes_http_accept
                    attempt.path_info = request.axes_path_info
                    attempt.failures_since_start = F("failures_since_start") + 1
                    attempt.attempt_time = request.axes_attempt_time
                    attempt.save()

                    log.warning(
                        "AXES: Repeated login failure by %s. Updated existing record in the database.",  # noqa: E501
                        client_str,
                    )

        failures_since_start = self.get_failures(request, credentials)
        request.axes_failures_since_start = failures_since_start

        if (
            settings.AXES_LOCK_OUT_AT_FAILURE
            and failures_since_start >= get_failure_limit(request, credentials)
        ):
            log.warning(
                "AXES: Locking out %s after repeated login failures.", client_str
            )

            request.axes_locked_out = True
            request.axes_credentials = credentials
            user_locked_out.send(
                "axes",
                request=request,
                username=username,
                ip_address=request.axes_ip_address,
            )

        if settings.AXES_ENABLE_ACCESS_FAILURE_LOG:
            with transaction.atomic(using=router.db_for_write(AccessFailureLog)):
                AccessFailureLog.objects.create(
                    username=username,
                    ip_address=request.axes_ip_address,
                    user_agent=request.axes_user_agent,
                    http_accept=request.axes_http_accept,
                    path_info=request.axes_path_info,
                    attempt_time=request.axes_attempt_time,
                    locked_out=request.axes_locked_out,
                )
                self.remove_out_of_limit_failure_logs(username=username)
