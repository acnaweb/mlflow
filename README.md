# MLFlow

MLFlow - Model registry

## Usage

```sh
mlflow server --backend-store-uri mysql+pymysql://${MYSQL_USER}:${MYSQL_PASSWORD}@mlflow-db.csifmnnguh7c.us-east-2.rds.amazonaws.com:3306/${MYSQL_DATABASE} 
```

### Run server using S3

- Environment

```sh
export MLFLOW_S3_ENDPOINT_URL=http://localhost:9000
export ARTIFACT_REPOSITORY=s3://mlflow
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
``` 

- Run Server

```sh
mlflow server --host 0.0.0.0 --artifacts-destination ${ARTIFACT_REPOSITORY} 
```

- Web UI

    http://0.0.0.0:5000/


## References

- https://mlflow.org/

