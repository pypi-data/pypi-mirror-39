# pointpy
Small api client for point. More info at https://api.minut.com/v1/docs/

Code heavily inspired from https://github.com/plamere/spotipy

## Usage

```
import pointpy

client_id = 'xxxx'
client_secret = 'yyyy'

username = 'zzzz@aaaa.bbb'
password = 'ccccc'

client_credentials_manager = pointpy.PointCredentialsManager(
    client_id, client_secret, username, password)
point = pointpy.Point(client_credentials_manager=client_credentials_manager)

point.devices()
```
