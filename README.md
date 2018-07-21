# jecto-cloud

## Google Cloud deployment

1. Clone project code in a folder.
1. Create a google cloud project with:
  1. A CloudSQL PostgreSQL instance and a DB.
  1. A Storage bucket to hold static files.
  1. Make sure billing is enabled.
1. To run in gcloud:
  1. Copy app.yaml.inst to app.yaml and set the following values based on your new project:
    1. BASE_URL : Should be identical to the gcloud project name. The app will be available at http://BASE_URL.appspot.com
    1. SECRET_KEY : [Django secret key](https://docs.djangoproject.com/en/dev/ref/settings/#secret-key).
    1. CLOUD_SQL_CONNECTION_STRING : Can be found by running `gcloud sql instances describe CLOUD-SQL-INSTANCE-ID | grep connectionName`. Required twice in the file.
    1. DB_NAME : The name of the DB in the CloudSQL instance.
    1. DB_USER : The username of the PostgreSQL user you want to use.
    1. DB_PASSWORD : Password for said user.
    1. STORAGE_BUCKET_URL : The URL of the storage bucket you created.
  1. Configure your gcloud profile to work with the new project and deploy
  1. Run gcloud app deploy
1. To run locally:
