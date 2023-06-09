![Reservation alert](https://github.com/Johanwv/reservation-alert/actions/workflows/build.yaml/badge.svg)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

Instructions
========================================

Build image
------------

```bash
docker build -t alert-reservation .
```

Run container
------------

```bash
docker run -e GMAIL_USER=gmailuser@gmail.com -e GMAIL_PASSWORD=password -e MAIL_RECIPIENTS=recipient@gmail,recipient2@gmail.com alert-reservation
```

Optionally you can also pass `ALWAYS_SEND_EMAIL=true` to test that an email is actually send

`INTEVERAL=60` is the interval in seconds between each check for available slots. Default is 300 sec.

```bash
docker run -e GMAIL_USER=gmailuser@gmail.com -e GMAIL_PASSWORD=password -e MAIL_RECIPIENTS=recipient@gmail.com -e ALWAYS_SEND_EMAIL=true alert-reservation
```
