
## Running System

First, open the console and clone the project using `git` (or you can simply download the project) and then to the directory of the quickstart you want to run, e.g. `zio-quickstart-restful-webservice`:

```scala
git clone https://github.com/SilverM/zioFxStream.git
cd zioFXStream
```

Once you are inside the project directory, run the application:

```scala
sbt run
```

Following that you can test steaming data through terminal by entering 
```scala
Example currency download: curl -i http://<localhost>/download/stream
Specific currency download (must be uploaded to resources folder): curl -i http://<localhost>/download/stream/specific/<file>
Example: curl -i http://localhost:8080/download/stream/specific/usdcad_2012_2022_short.csv
```
