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
docker run -e GMAIL_USER=gmailuser@gmail.com -e GMAIL_PASSWORD=password -e MAIL_RECIPIENT=recipient@gmail alert-reservation
```

Optionally you can also pass `ALWAYS_SEND_EMAIL=true` to test that an email is actually send

```bash 
docker run -e GMAIL_USER=gmailuser@gmail.com -e GMAIL_PASSWORD=password -e MAIL_RECIPIENT=recipient@gmail -e ALWAYS_SEND_EMAIL=true alert-reservation
```