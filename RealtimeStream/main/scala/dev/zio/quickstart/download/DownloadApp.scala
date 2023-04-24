package dev.zio.quickstart.download

import zhttp.http.*
import zio.*
import zio.stream.ZStream
import zio.stream.ZPipeline
/**
 * An http app that: 
 *   - Accepts a `Request` and returns a `Response` 
 *   - May fail with type of `Throwable`
 *   - Does not require any environment
 */
object DownloadApp:
  def apply(): Http[Any, Throwable, Request, Response] =
    Http.collectHttp[Request] {
      // GET /download
      case Method.GET -> !! / "download" =>
        val fileName = "file.txt"
        Http.fromStream(ZStream.fromResource(fileName)).setHeaders(
          Headers(
            ("Content-Type", "application/octet-stream"),
            ("Content-Disposition", s"attachment; filename=${fileName}")
          )
        )

      // Download a large file using streams
      // GET /download/stream
      case Method.GET -> !! / "download" / "stream" =>
        val file = "bigfile.txt"
        Http.fromStream(
          ZStream.fromResource(file)
            .schedule(Schedule.spaced(50.millis))
        ).setHeaders(
          Headers(
            ("Content-Type", "application/octet-stream"),
            ("Content-Disposition", s"attachment; filename=${file}")
          )
        )

        // GET /download/stream/quotes
      case Method.GET -> !! / "download" / "stream" / "quotes" =>
        val file = "usdcad_2012_2022_short.csv"
        Http.fromStream(
          ZStream.fromResource(file)
            .schedule(Schedule.spaced(20.millis))
        ).setHeaders(
          Headers(
            ("Content-Type", "application/octet-stream"),
            ("Content-Disposition", s"attachment; filename=${file}")
          )
        )

        // GET /download/stream/codes
      case Method.GET -> !! / "download" / "stream" / "specific" / currencycode =>
        val file = s"$currencycode"
        Http.fromStream(
          ZStream.fromResource(file)
            .schedule(Schedule.spaced(20.millis))
        ).setHeaders(
          Headers(
            ("Content-Type", "application/octet-stream"),
            ("Content-Disposition", s"attachment; filename=${file}")
          )
        )

    }

//curl -i http://localhost:8080/download/stream
