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
                 longitude: Double,
                 date: Date)

object Flickr extends Flickr {

  @transient lazy val conf: SparkConf = new SparkConf().setMaster("local").setAppName("NYPD")
  @transient lazy val sc: SparkContext = new SparkContext(conf)

  /** Main function */
  def main(args: Array[String]): Unit = {
    // This function removes the dirty lines using regular expressions
    def removeDirtyLines(lines: RDD[String], withDate: Boolean): RDD[String] = {
      var pattern = "(\\d+)\\, (\\d+\\.\\d+)\\, (\\d+\\.\\d+)".r
      if(withDate) {
        pattern = "(\\d+)\\, (\\d+\\.\\d+)\\, (\\d+\\.\\d+)\\, (201\\d:\\d+:\\d+ \\d+:\\d+:\\d+)".r
      }
      lines.map(l => pattern.findAllMatchIn(l).toList).filter(l => (l.length > 0)).map(l => l.get(0).toString())
    }

    var lines = sc.textFile("src/main/resources/photos/elbow.csv").mapPartitionsWithIndex { (idx, iter) => if (idx == 0) iter.drop(1) else iter }
    // Removing dirty data
    lines = removeDirtyLines(lines, true)
    val raw = rawPhotos(lines)
    // Creating a new instance for formatting dates
    val date_formatter = new java.text.SimpleDateFormat("yyyy:MM:dd HH:mm:ss")
    // Preprations for making CSV file
    val distance_errors_file = new BufferedWriter(new FileWriter("src/main/resources/photos/result_elbow_distances.csv"))
    val writer2 = new CSVWriter(distance_errors_file, '\n')
    // An array with size of 12 which assigns a value to different months base on the season they are in.
    val seasons = Array(0, 0, 33.33, 33.33, 33.33, 66.66, 66.66, 66.66, 100, 100, 100, 0)
    // A bad way of making an array with length of, for example 22; so we can store error rate for each i number of kernels.
    var errorDistance_for_kernels = Array((0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0),
      (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0),
      (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0))

    // A function for getting the season value for a specific month.
    def getSeason(month: Int): Double = {
      seasons(month)
    }

    // number of iterations is set to 100
    val num_repetition = 100
    for (j <- 1 to num_repetition) {
      // number of kernels
      for (i <- 2 to kmeansKernels) {

        // Sampling and removing dirty data(again!) for the samples
        val initialMeans = lines.takeSample(false, i)
          .flatMap(l => {
            val a = l.split(", ");
            try {
              Some(a(1).toDouble, a(2).toDouble, getSeason(date_formatter.parse(a(3)).getMonth))
            }
            catch {
              case e: Exception => None
            }
          })
        // Normalizing values of Latitude and Longitude and map them between 0 to 100
        val min_latitude_means = initialMeans.map(v => v._1).min
        val max_latitude_means = initialMeans.map(v => v._1).max
        val min_longitude_means = initialMeans.map(v => v._2).min
        val max_longitude_means = initialMeans.map(v => v._2).max
        val normalized_seasonal_means = initialMeans.map(v => (100 * (v._1 - min_latitude_means) / max_latitude_means,
          100 * (v._2 - min_longitude_means) / max_longitude_means,
          v._3))
        // Receiving calculated new centers and the error rate corresponding to these new centers.
        var (means_tmp, error_rate) = kmeans(normalized_seasonal_means, raw)
        // Mapping String of seasons to the calculated value
        val means = means_tmp.map(v => ((max_latitude_means * v._1 / 100) + min_latitude_means,
          max_longitude_means * (v._2) / 100 + min_longitude_means,
          v._3 match {
            case x if x < 16 => "Winter"
            case x if x >= 16 && x < 50 => "Spring"
            case x if x >= 50 && x < 84 => "Summer"
            case _ => "Fall"
          }))

        // Summing up the error rates together for all the kernel centers
        errorDistance_for_kernels(initialMeans.length) = sum_up(errorDistance_for_kernels(initialMeans.length), error_rate)

        def sum_up(error_num_pair: (Double, Double), error_rate: Double): (Double, Double) = {
          (error_num_pair._1 + error_rate, error_num_pair._2 + 1)
        }
      }
    }
    // Getting the avarage error rate by deviding the sum by the number of repetition of it.
    errorDistance_for_kernels = errorDistance_for_kernels.map(v => (v._1 / v._2, v._2))
    // Writing to the file
    for (i <- 0 to 19) {
      writer2.writeNext(Array("KernelNum: " + i.toString + ", AvgDistance: " + errorDistance_for_kernels(i)._1.toString + ", RepTimes: " + errorDistance_for_kernels(i)._2.toString), false)
    }
    distance_errors_file.close()
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
  def EuclideanDistance(c1: (Double, Double, Double), c2: (Double, Double, Double)) = {
    val R = 6371e3
    val lat1 = toRadians(c1._1)
    val lon1 = toRadians(c1._2)
    val lat2 = toRadians(c2._1)
    val lon2 = toRadians(c2._2)
    val x = (lon2 - lon1) * Math.cos((lat1 + lat2) / 2)
    val y = (lat2 - lat1)
    val z = (c1._3 - c2._3)
    // Ecludian Distance for 3 dimensions of two points
    Math.sqrt(x * x + y * y + z * z)
  }

  /** Return the index of the closest mean */
  def findClosest(p: (Double, Double, Double), centers: Array[(Double, Double, Double)]): Int = {
    var bestIndex = 0
    var closest = Double.PositiveInfinity
    for (i <- 0 until centers.length) {
      val tempDist = EuclideanDistance(p, centers(i))
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
    val date_formatter = new java.text.SimpleDateFormat("yyyy:MM:dd HH:mm:ss")
    // Cleaning dirty lines(again!)
    val rawPhotosList = lines.flatMap(l => {
      val a = l.split(", ");
      try {
        Some(Photo(a(0), a(1).toDouble, a(2).toDouble, date_formatter.parse(a(3))))
      }
      catch {
        case e: Exception => None
      }
    })
    rawPhotosList
  }

  @tailrec final def kmeans(means: Array[(Double, Double, Double)], vectors: RDD[Photo], iter: Int = 1): (Array[(Double, Double, Double)], Double) = {
    import java.util.Calendar
    var cal = Calendar.getInstance
    var distance_flag = 1
    val num = iter + 1
    // for normalisation of values of photos
    val min_latitude_vectors = vectors.map(v => v.latitude).min()
    val max_latitude_vectors = vectors.map(v => v.latitude).max()
    val min_longitude_vectors = vectors.map(v => v.longitude).min()
    val max_longitude_vectors = vectors.map(v => v.longitude).max()
    val seasons = Array(0, 0, 33.33, 33.33, 33.33, 66.66, 66.66, 66.66, 100, 100, 100, 0)

    def getSeason(month: Int): Double = {
      seasons(month)
    }

    // mapping photos values to normalised ones.
    val vectors_3D = vectors.map(v => (100 * (v.latitude - min_latitude_vectors) / max_latitude_vectors,
      100 * (v.longitude - min_longitude_vectors) / max_longitude_vectors,
      getSeason((v.date).getMonth)))

    // Finding the closest center to each photo and saving the index for that center
    val closest_center_for_photos = vectors_3D
      .map(v => (findClosest((v._1, v._2, v._3), means), (1, v._1, v._2, v._3))).sortByKey() // (index,(1,lat,lon,season_code))

    // calculating new center positions
    val new_centers = closest_center_for_photos
      .reduceByKey((v1, v2) => (v1._1 + v2._1, v1._2 + v2._2, v1._3 + v2._3, v1._4 + v2._4))
      .mapValues(v => (v._2 / v._1, v._3 / v._1, (v._4 / v._1).toDouble)).sortByKey() // (index,(avg-lat, avg-lon, avg-season))

    // rdd to array (index,(avg-lat,avg-lon))
    val new_centers_arr = new_centers.collect()

    // filling missing centers
    val new_means = means.clone()
    for (i <- 0 to new_centers_arr.length - 1) {
      new_means(new_centers_arr(i)._1) = new_centers_arr(i)._2
    }

    // calculating error rate
    val error_rate = closest_center_for_photos
      .map(v => (EuclideanDistance(new_means(v._1), (v._2._2, v._2._3, v._2._4)))).reduce((v1, v2) => v1 + v2)

    // if the centers have not moved so much, so the new centers are found and we should return from this function
    def check_distance(): Unit = {
      for (i <- 0 to means.length - 1) {
        if (EuclideanDistance(means(i), new_means(i)) > kmeansEta) {
          distance_flag = 0
        }
      }
    }

    check_distance()

    // if everything is ok return the new positions for kernels(centers) and the error rate for these centers.
    if (num > kmeansMaxIterations + 1 || distance_flag == 1) {
      (new_means, error_rate)
    }
    else {
      kmeans(new_means, vectors, num)
    }
  }

}
