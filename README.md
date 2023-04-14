
## Running System

First, open the console and clone the project using `git` (or you can simply download the project) and then to the directory of the quickstart you want to run, e.g. `zio-quickstart-restful-webservice`:

```scala
git clone https://github.com/SilverM/zioFxStream.git
cd zio2
```

Once you are inside the project directory, run the application:

```scala
sbt run
```

Following that you can test steaming data via 
```scala
curl by calling curl -d [POST data] https://<localhost>/download/stream/quotes 
```
