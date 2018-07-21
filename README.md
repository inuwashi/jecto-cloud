# jecto-cloud

## Google Cloud deployment

1. Clone project code in a folder.
1. Create a google cloud project with:
  1. A CloudSQL PostgreSQL instance and a DB.
  1. A Storage bucket to hold static files.
  1. Make sure billing is enabled.
* To run in gcloud:
  1. Copy app.yaml.inst to app.yaml and set the following values based on your new project:
    1. BASE_URL : Should be identical to the gcloud project name. The app will be available at http://BASE_URL.appspot.com
    1. SECRET_KEY : [Django secret key](https://docs.djangoproject.com/en/dev/ref/settings/#secret-key).
    1. CLOUD_SQL_CONNECTION_STRING : Can be found by running `gcloud sql instances describe CLOUD-SQL-INSTANCE-ID | grep connectionName`. Required twice in the file.
    1. DB_NAME : The name of the DB in the CloudSQL instance.
    1. DB_USER : The username of the PostgreSQL user you want to use.
    1. DB_PASSWORD : Password for said user.
    1. STATIC_BUCKET_NAME : The name of the bucket your created for he static files.
    1. STORAGE_BUCKET_URL : The URL of the storage bucket you created. you can find this by running `gsutil ls`.
  1. Configure your gcloud profile to work with the new project and deploy.
  1. Load static files:
    1. Load local settings by running `chmod +x ./set_env_vars.sh; source ./set_env_vars.sh`
    1. Run `python manage.py collectstatic`. This will create a folder called jecto_static in parallel to BASE_DIR and collect all the static files there.
    1. Create the static folder in the bukcet and upload the collected static files by running `gsutil rsync -r ../jecto_static/ gs://STATIC_BUCKET_NAME/static`.
    1. Set permission on the new bucket by running `gsutil acl ch -r -u AllUsers:R gs://BUCKET_NAME/static`
  1. Run `gcloud app deploy`.
* To run locally:
  1. Copy set_env_vars.sh.inst to set_env_vars.sh.
    1. Set the values in the file using a local PostgreSQL DB or the [CloudSQL Proxy](https://cloud.google.com/sql/docs/mysql/sql-proxy).
    1. Note that DEBUG has to be set True to run locally.
    1. Run `chmod +x ./set_env_vars.sh; source ./set_env_vars.sh` to load the settings.
  1. If you are connecting to the CloudSQL from the local setup:
    1. Download the CloudSQL proxy.
    1. Authenticate the application by running `gcloud auth application-default login`.
    1. Activate the proxy by running `cloud_sql_proxy -instances="CLOUD_SQL_INSTANCE_CONNECTION_STRING"=tcp:PROXY_PORT`
    1. Update the environment variables to match.
  1. Run `python manage.py makemigrations`
  1. Run `python manage.py migrate`
  1. Run `python manage.py runserver`
