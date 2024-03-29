package assignment

import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.rdd.RDD
import annotation.tailrec
import scala.reflect.ClassTag

import java.io.StringReader
import com.opencsv.CSVReader

import java.util.Date
import java.text.SimpleDateFormat
import Math._

import java.io.StringWriter
import com.opencsv.CSVWriter
import scala.collection.JavaConversions._
import java.io.FileWriter
import java.io.BufferedWriter

// import org.apache.spark.ml.clustering.KMeans

case class Photo(id: String,
                 latitude: Double,
                 longitude: Double)

//datetime: Date)

object Flickr extends Flickr {

  @transient lazy val conf: SparkConf = new SparkConf().setMaster("local").setAppName("NYPD")
  @transient lazy val sc: SparkContext = new SparkContext(conf)

  /** Main function */
  def main(args: Array[String]): Unit = {

    val lines = sc.textFile("src/main/resources/photos/flickrDirtySimple.csv").mapPartitionsWithIndex { (idx, iter) => if (idx == 0) iter.drop(1) else iter }
    val raw = rawPhotos(lines)
    val initialMeans = lines.flatMap(l => {
        val a = l.split(", ");
        try {
          Some(a(1).toDouble, a(2).toDouble)
        }
        catch {
          case e: Exception => None
        }
      })
    val size = initialMeans.collect().length

    val means = kmeans(initialMeans.takeSample(false, kmeansKernels), raw)
    means.foreach(println)

    val out = new BufferedWriter(new FileWriter("src/main/resources/photos/result.csv"))
    val writer = new CSVWriter(out, '\n')
    writer.writeNext(means.map(v => v._1.toString + ", " + v._2.toString), false)
    out.close()

  }
}

class Flickr extends Serializable {

  /** K-means parameter: Convergence criteria */
  def kmeansEta: Double = 20.0D

  /** K-means parameter: Number of clusters */
  def kmeansKernels = 16

  /** K-means parameter: Maximum iterations */
  def kmeansMaxIterations = 50

  //(lat, lon)
  def distanceInMeters(c1: (Double, Double), c2: (Double, Double)) = {
    val R = 6371e3
    val lat1 = toRadians(c1._1)
    val lon1 = toRadians(c1._2)
    val lat2 = toRadians(c2._1)
    val lon2 = toRadians(c2._2)
    val x = (lon2 - lon1) * Math.cos((lat1 + lat2) / 2);
    val y = (lat2 - lat1);
    Math.sqrt(x * x + y * y) * R;
  }

  /** Return the index of the closest mean */
  def findClosest(p: (Double, Double), centers: Array[(Double, Double)]): Int = {
    var bestIndex = 0
    var closest = Double.PositiveInfinity
    for (i <- 0 until centers.length) {
      val tempDist = distanceInMeters(p, centers(i))
      if (tempDist < closest) {
        closest = tempDist
        bestIndex = i
      }
    }
    bestIndex
  }

  //  /** Average the vectors */
  //  def averageVectors(ps: Iterable[Photo]): (Double, Double) = ???

  def rawPhotos(lines: RDD[String]): RDD[Photo] = {
    val rawPhotosList = lines.flatMap(l => {
      val a = l.split(", ");
      try {
        Some(Photo(a(0), a(1).toDouble, a(2).toDouble))
      }
      catch {
        case e: Exception => None
      }
    })
    rawPhotosList
  }

  @tailrec final def kmeans(means: Array[(Double, Double)], vectors: RDD[Photo], iter: Int = 1): Array[(Double, Double)] = {
    var distance_flag = 1
    val num = iter + 1

    val closest_center_for_photos = vectors
      .map(v => (findClosest((v.latitude, v.longitude), means), (1, v.latitude, v.longitude))).sortByKey() // (index,(1,lat,lon,id))
    val new_centers = closest_center_for_photos.reduceByKey((v1, v2) => (v1._1 + v2._1, v1._2 + v2._2, v1._3 + v2._3))
      .mapValues(v => (v._2 / v._1, v._3 / v._1)).sortByKey() // (index,(avg-lat,avg-lon))
    val new_centers_arr = new_centers.collect() // rdd to array (index,(avg-lat,avg-lon))

    // filling missing centers
    val new_means = means.clone()
    for (i <- 0 to new_centers_arr.length - 1) {
      new_means(new_centers_arr(i)._1) = new_centers_arr(i)._2
    }

    def check_distance(): Unit = {
      for (i <- 0 to kmeansKernels - 1) {
        if (distanceInMeters(means(i), new_means(i)) > kmeansEta) {
          distance_flag = 0
        }
      }
    }

    check_distance()

    if (num > kmeansMaxIterations + 1 || distance_flag == 1) {
      new_means
    }
    else {
      kmeans(new_means, vectors, num)
    }
  }

}
