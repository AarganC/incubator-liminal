import xgboost as xgb
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import LongType
from sklearn.metrics import precision_score
from sklearn.model_selection import train_test_split

spark = None


def init_spark():
    global spark
    spark = SparkSession.builder.appName('Spark ETL').enableHiveSupport().getOrCreate()


def load_data(path):
    return (spark
            .read
            .format('csv')
            .option("header", "true")
            .option("inferSchema", "true")
            .load(path)
            )


def transform_column_names(data):
    # UDF for converting labels to indexes
    def cnvt_species(s):
        species = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
        return species.index(s)

    cnvt_species_udf = udf(cnvt_species, LongType())

    renamed = (data.withColumnRenamed("SepalLengthCm", 'sepal_length')
               .withColumnRenamed("SepalWidthCm", 'sepal_width')
               .withColumnRenamed("PetalLengthCm", 'petal_length')
               .withColumnRenamed("PetalWidthCm", 'petal_width')
               .withColumnRenamed('Species', 'species')
               )

    return renamed.select("sepal_length", "sepal_width", "petal_length", "petal_width",
                          cnvt_species_udf("species")).withColumnRenamed('cnvt_species(species)', 'species')


def train(data):
    xgtrain = xgb.DMatrix(data[["sepal_length", "sepal_width", "petal_length", "petal_width"]].values, data['species'])
    param = {'max_depth': 2,
             'objective': 'multi:softmax',
             'num_class': 3,
             'nthread': 8}
    return xgb.train(param, xgtrain, 10)


def predict(model, test_data):
    dtest = xgb.DMatrix(test_data[["sepal_length", "sepal_width",
                                   "petal_length", "petal_width"]].values)
    return model.predict(dtest)


if __name__ == '__main__':
    init_spark()
    data = load_data('data/iris.csv')

    data = transform_column_names(data)

    training_data, testing_data = train_test_split(data.toPandas())

    bst = train(training_data)

    ypred = predict(bst, testing_data)

    # Calculate accuracy score
    p_score = precision_score(testing_data["species"], ypred, average='micro')

    print("XGBoost Model Precision Score:", p_score)
