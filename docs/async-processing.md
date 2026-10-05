# Asynchronous processing

Redis and Celery are used for work that should not block an HTTP request.

Typical jobs include:

- reservation confirmation emails
- payment confirmation notifications
- scheduled reminders
- cleanup/expiry tasks
- other background processing

A simplified task looks like:

~~~python
@celery_app.task
def send_reservation_confirmation(data: dict[str, str]) -> None:
    send_email(
        recipient=data["email"],
        template=data["template"],
        context=data,
    )
~~~

The important architectural property is that the API can commit its business transaction independently from slow external work. Notifications are queued after the relevant state transition so email delivery does not determine whether a reservation or payment succeeds.