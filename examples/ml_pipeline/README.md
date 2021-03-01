# ML Pipeline - basic example
In this example, we demonstrate a fully fledged ML training and serving pipeline over Apache Liminal.
The ML logic used is basic, but the pipeline exemplifies many common pieces of the framework.

## Preparation
* Create a test bucket ```s3://liminal-ml-demo```
* Place the data/iris.csv file in a the path ```s3://liminal-ml-demo/data/iris.csv```
* Ensure EMR is enabled for your project
* Set up EKS and EFS as per the example in X

## ML tasks
### Preprocessing and splitting datasets

In this task, we load and pre-process the Iris dataset using pyspark.
The processing logic includes basic column renames and label manipulation.

In this case, Liminal will provision an EMR cluster, and initialize it with the right python libraries needed.

It will then submit a pyspark job to the cluster, resulting in two output directories:
```s3://liminal-ml-demo/preprocessed/train/YYYYMMDD```
```s3://liminal-ml-demo/preprocessed/test/YYYYMMDD```

### Training
Train the model using xgboost.
The training will be performed as a liminal python task.
The task will receive the path to the train dataset from the previous phase.
The best model will be stored in s3 path under:
```s3://liminal-ml-demo/preprocessed/model/YYYYMMDD```

### Predict
Predict on the test set.
Prediction will be performed as a liminal python task.
The task will receive the path to the model file from the previous phase.
The output of the predictions will be stored in s3 path under:
```s3://liminal-ml-demo/preprocessed/predict/YYYYMMDD```

### Evaluate
Evaluate the metrics for the predictions vs. the ground truth
Evaluation will be performed as a liminal python task.
The task will receive the paths :
```s3://liminal-ml-demo/preprocessed/test/YYYYMMDD```
```s3://liminal-ml-demo/preprocessed/predict/YYYYMMDD```

The result of the evaluation will be stored in s3 under:
```s3://liminal-ml-demo/preprocessed/model/YYYYMMDD/eval.csv```

### (Conditional) deploy
If the evaluation passed a certain criteria, the best model will be deployed to run as a Flask service.
The logic for the decision will be expressed as a python task.
The service will be deployed as a flask container in kubernetes (how to configure ingress?)
The deployment process will involve making a post request to the flask service, which will contain the S3 path to the new
model file.

The flask container will load the model file and start serving requests with it.

### Serve
The URL for the service will be published here (TODO:)
Requests should be of the format (TODO:)

## Testing the pipeline locally
Processing:
* local liminal spins up EMR clusters -> credential management
* local liminal spins up local spark -> where do we store data?

Storage:
* How to allow docker tasks to access S3? do we mount s3 using s3fs?
