# cover-song-identification-platform
Platform for cover song identification

# How to install
The app is tested on Ubuntu (using a GCP VM). Due to the Essentia library, it may be tricky to set it up on a Mac (at least I haven't succeeded)

You need to have the following installed to deploy the app:
* Docker
* Mongo DB running on localhost (default port)
* Node Js and npm
* Python 3.9 and virtualenv

Install the backend:

```shell
cd CSI_BE
virtualenv -p python3.9 venv
. venv/bin/activate
pip3 install -r requirements.txt
```

Install the frontend:
```shell
cd csi_fe
npm install
```

# How to run

From the root of the repo run 
```shell
docker compose up -d
```
To bring up the nginx reverse proxy

Then execute:
```shell
. start.sh
```

After that open you browser in http://localhost and you should see the dashboard.
The app uses ports 80, 3000 and 5000 so make sure they are not allocated
