# Reddit 4060 Laptop Alert Bot
This bot searches [/r/laptopdeals](https://www.reddit.com/r/laptopdeals) for laptops that have a 4060 for less than a specified price.

## Needed Secrets
- `secrets/from_email.txt` - The email sending text alerts from
- `secrets/to_email.txt` - The email to send the alert to
- `secrets/reddit_app_token.txt` - Reddit App token [link](https://www.reddit.com/prefs/apps)
- `secrets/reddit_app_id.txt` - Reddit App ID [link](https://www.reddit.com/prefs/apps)
- `secrets/app_password.txt` - Google App password, not super secure don't attach to main account.

## Raspberry Pi Config
systemd tutorial created using [ref](https://www.thedigitalpictureframe.com/ultimate-guide-systemd-autostart-scripts-raspberry-pi/)


The following systemd config should start a service on boot, and keep it running indefinitely.
```
[Unit]
Description=Startup service for python program.
Requires=network.target

[Service] 
Type=idle
WorkingDirectory={path/to/workdir}
ExecStart= {path/to/python/executable} {path/to/workdir/main.py}
user={username}
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```