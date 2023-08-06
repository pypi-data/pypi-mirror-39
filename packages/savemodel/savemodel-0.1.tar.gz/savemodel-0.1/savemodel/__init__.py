from clipper_admin.deployers.deployer_utils import save_python_function
import os
import re
import pyspark
import json
import sys
from tensorflow import Session
import tensorflow as tf
import shutil
import glob
import keras
import h2o
import subprocess
import sys


class saveModel():
    def modelsave(name, func, sc, pyspark_model):
        model_class = re.search("pyspark.*'",
                                str(type(pyspark_model))).group(0).strip("'")
        if model_class is None:
            print("pyspark_model argument was not a pyspark object")

        # save predict function
        serialization_dir = save_python_function(name, func)
        # save Spark model
        spark_model_save_loc = os.path.join(serialization_dir,
                                            "pyspark_model_data")
        try:
            if isinstance(pyspark_model,
                          pyspark.ml.pipeline.PipelineModel) or isinstance(
                pyspark_model, pyspark.ml.base.Model):
                pyspark_model.save(spark_model_save_loc)
            else:
                pyspark_model.save(sc, spark_model_save_loc)
        except Exception as e:
            print("Error saving spark model: %s" % e)
            raise e

        # extract the pyspark class name. This will be something like
        # pyspark.mllib.classification.LogisticRegressionModel
        with open(os.path.join(serialization_dir, "metadata.json"),
                  "w") as metadata_file:
            json.dump({"model_class": model_class}, metadata_file)
        # command = "hadoop fs -put " + serialization_dir + " /clipper/"
        # print(command)
        # os.system(command)
        p = subprocess.Popen(["hadoop", "fs", "-put", serialization_dir, "/clipper/"], stdout=subprocess.PIPE)
        output, error = p.communicate()
        if p.returncode != 0:
            print(error)
            print(output)
            sys.exit("Save model to HDFS failed %d %s %s" % (p.returncode, output, error))

        tempPath = os.path.basename(os.path.normpath(serialization_dir))
        print("Spark model saved on HDFS at : /clipper/" + tempPath)
        py_minor_version = (sys.version_info.major, sys.version_info.minor)
        # print(py_minor_version)
        # Check if Python 2 or Python 3 image
        base_image = "default"
        if base_image == "default":
            if py_minor_version < (3, 0):
                # print("Using Python 2 base image")
                a = 2
                # base_image = "{}/pyspark-container:{}".format(
                #   __registry__, __version__)
            elif py_minor_version == (3, 5):
                # print("Using Python 3.5 base image")
                a = 3.5
                # base_image = "{}/pyspark35-container:{}".format(
                #   __registry__, __version__)
            elif py_minor_version == (3, 6):
                # print("Using Python 3.6 base image")
                a = 3.6
                # base_image = "{}/pyspark36-container:{}".format(
                #    __registry__, __version__)
        return a


    def modelpysave(name, func):
        # save predict function
        serialization_dir = save_python_function(name, func)
        # command = "hadoop fs -put " + serialization_dir + " /clipper/"
        # print(command)
        # os.system(command)
        p = subprocess.Popen(["hadoop", "fs", "-put", serialization_dir, "/clipper/"], stdout=subprocess.PIPE)
        output, error = p.communicate()
        if p.returncode != 0:
            print(error)
            print(output)
            sys.exit("Save model to HDFS failed %d %s %s" % (p.returncode, output, error))


        tempPath = os.path.basename(os.path.normpath(serialization_dir))
        print("Python model saved on HDFS at : /clipper/" + tempPath)
        py_minor_version = (sys.version_info.major, sys.version_info.minor)
        base_image = "default"
        if base_image == "default":
            if py_minor_version < (3, 0):
                # print("Using Python 2 base image")
                a = 2
                # base_image = "{}/pyspark-container:{}".format(
                #   __registry__, __version__)
            elif py_minor_version == (3, 5):
                # print("Using Python 3.5 base image")
                a = 3.5
                # base_image = "{}/pyspark35-container:{}".format(
                #   __registry__, __version__)
            elif py_minor_version == (3, 6):
                # print("Using Python 3.6 base image")
                a = 3.6
                # base_image = "{}/pyspark36-container:{}".format(
                #    __registry__, __version__)
        return a


    def modeltfsave(name, func, tf_sess_or_saved_model_path):
        # save predict function
        serialization_dir = save_python_function(name, func)
        # save Tensorflow session or copy the saved model into the image
        if isinstance(tf_sess_or_saved_model_path, Session):
            tf_sess_save_loc = os.path.join(serialization_dir,
                                            "tfmodel/model.ckpt")
            try:
                saver = tf.train.Saver()
                save_path = saver.save(tf_sess_or_saved_model_path,
                                       tf_sess_save_loc)
            except Exception as e:
                print("Error saving Tensorflow model: %s" % e)
                raise e
                print("TensorFlow model saved at: %s " % save_path)
        else:
            # Check if its a frozen Graph or a saved tensorflow Model

            # A typical Tensorflow model contains 4 files:
            #  model-ckpt.meta: This contains the complete graph.
            #                   [This contains a serialized MetaGraphDef protocol buffer.
            #  model-ckpt.data-0000-of-00001: This contains all the values of variables(weights, biases,
            #                                 placeholders,gradients, hyper-parameters etc).
            #  model-ckpt.index: metadata.
            #  checkpoint: All checkpoint information

            # Frozen Graph
            # Single encapsulated file(.pb extension) without un-necessary meta-data, gradients and
            # un-necessary training variables

            if os.path.isdir(tf_sess_or_saved_model_path):
                # Directory - Check for Frozen Graph or a Saved Tensorflow Model
                is_frozen_graph = glob.glob(
                    os.path.join(tf_sess_or_saved_model_path, "*.pb"))
                if (len(is_frozen_graph) > 0):
                    try:
                        shutil.copytree(tf_sess_or_saved_model_path,
                                        os.path.join(serialization_dir, "tfmodel"))
                    except Exception as e:
                        print(
                            "Error copying Frozen Tensorflow model: %s" % e)
                        raise e
                else:
                    # Check if all the 4 files are present
                    suffixes = [os.path.join(tf_sess_or_saved_model_path, suffix) \
                                for suffix in ("*.meta", "*.index", "checkpoint", "*.data*")]
                    if sum([1 for suffix in suffixes if glob.glob(suffix)]) == 4:
                        try:
                            shutil.copytree(tf_sess_or_saved_model_path,
                                            os.path.join(serialization_dir,
                                                         "tfmodel"))
                        except Exception as e:
                            print("Error copying Tensorflow model: %s" % e)
                            raise e
                    else:
                        print(
                            "Tensorflow Model: %s not found or some files are missing"
                            % tf_sess_or_saved_model_path)
                        raise (
                            "Frozen Tensorflow Model: %s not found or some files are missing "
                            % tf_sess_or_saved_model_path)
            else:
                # File provided ...check if file exists and a frozen model
                # Check if a frozen model exists or else error out
                if (os.path.isfile(tf_sess_or_saved_model_path)
                    and tf_sess_or_saved_model_path.lower().endswith(('.pb'))):
                    os.makedirs(os.path.join(serialization_dir, "tfmodel"))
                    try:
                        shutil.copyfile(
                            tf_sess_or_saved_model_path,
                            os.path.join(
                                serialization_dir, "tfmodel/" +
                                                   os.path.basename(tf_sess_or_saved_model_path)))
                    except Exception as e:
                        print(
                            "Error copying Frozen Tensorflow model: %s" % e)
                        raise e
                else:
                    print("Tensorflow Model: %s not found" %
                          tf_sess_or_saved_model_path)
                    raise ("Frozen Tensorflow Model: %s not found "
                           % tf_sess_or_saved_model_path)
            print("TensorFlow model copied to: tfmodel ")

        py_minor_version = (sys.version_info.major, sys.version_info.minor)
        base_image = "default"
        if base_image == "default":
            if py_minor_version < (3, 0):
                # print("Using Python 2 base image")
                a = 2
                # base_image = "{}/pyspark-container:{}".format(
                #   __registry__, __version__)
            elif py_minor_version == (3, 5):
                # print("Using Python 3.5 base image")
                a = 3.5
                # base_image = "{}/pyspark35-container:{}".format(
                #   __registry__, __version__)
            elif py_minor_version == (3, 6):
                # print("Using Python 3.6 base image")
                a = 3.6
                # base_image = "{}/pyspark36-container:{}".format(
                #    __registry__, __version__)
        # coping Model To HDFS

        # command = "hadoop fs -put " + serialization_dir + " /clipper/"
        # print(command)
        # os.system(command)
        p = subprocess.Popen(["hadoop", "fs", "-put", serialization_dir, "/clipper/"], stdout=subprocess.PIPE)
        output, error = p.communicate()
        if p.returncode != 0:
            print(error)
            print(output)
            sys.exit("Save model to HDFS failed %d %s %s" % (p.returncode, output, error))


        tempPath = os.path.basename(os.path.normpath(serialization_dir))
        print("TF model saved on HDFS at : /clipper/" + testPath)
        return a


    def modelkerassave(name, func, model_path_or_object):
        serialization_dir = save_python_function(name, func)
        # save Keras model or copy the saved model into the image
        if isinstance(model_path_or_object, keras.Model):
            model_path_or_object.save(os.path.join(serialization_dir, "keras_model.h5"))
        elif os.path.isfile(model_path_or_object):
            try:
                shutil.copy(model_path_or_object,
                            os.path.join(serialization_dir, "keras_model.h5"))
            except Exception as e:
                print("Error copying keras model: %s" % e)
                raise e
        else:
            print(
                "%s should be wither a Keras Model object or a saved Model ('.h5')" % model_path_or_object)
            raise
        py_minor_version = (sys.version_info.major, sys.version_info.minor)
        # Check if Python 2 or Python 3 image
        base_image = "default"
        if base_image == "default":
            if py_minor_version < (3, 0):
                # logger.info("Using Python 2 base image")
                # base_image = "{}/keras-container:{}".format(__registry__, __version__)
                a = 2
            elif py_minor_version == (3, 5):
                # logger.info("Using Python 3.5 base image")
                # base_image = "{}/keras35-container:{}".format(__registry__,
                #                                              __version__)
                a = 3.5
            elif py_minor_version == (3, 6):
                # logger.info("Using Python 3.6 base image")
                # base_image = "{}/keras36-container:{}".format(__registry__,
                #                                              __version__)
                a = 3.6
            # command = "hadoop fs -put " + serialization_dir + " /clipper/"
            # print(command)
            # os.system(command)
        p = subprocess.Popen(["hadoop", "fs", "-put", serialization_dir, "/clipper/"], stdout=subprocess.PIPE)
        output, error = p.communicate()
        if p.returncode != 0:
            print(error)
            print(output)
            sys.exit("Save model to HDFS failed %d %s %s" % (p.returncode, output, error))
        tempPath = os.path.basename(os.path.normpath(serialization_dir))
        print("Keras model saved on HDFS at : /clipper/" + tempPath)
        return a


    def modelh2osave(name, func, model_path_or_object):
        serialization_dir = save_python_function(name, func)
        # save H2O model or copy the saved model into the image
        try:
            modelPath = h2o.save_model(model=model_path_or_object, path=serialization_dir, force=True)
            shutil.copy(modelPath, os.path.join(serialization_dir, "h2o_model"))
        except Exception as e:
            print("Error copying keras model: %s" % e)
            raise e

        py_minor_version = (sys.version_info.major, sys.version_info.minor)
        # Check if Python 2 or Python 3 image
        base_image = "default"
        if base_image == "default":
            if py_minor_version < (3, 0):
                # logger.info("Using Python 2 base image")
                # base_image = "{}/keras-container:{}".format(__registry__, __version__)
                a = 2
            elif py_minor_version == (3, 5):
                # logger.info("Using Python 3.5 base image")
                # base_image = "{}/keras35-container:{}".format(__registry__,
                #                                              __version__)
                a = 3.5
            elif py_minor_version == (3, 6):
                # logger.info("Using Python 3.6 base image")
                # base_image = "{}/keras36-container:{}".format(__registry__,
                #                                              __version__)
                a = 3.6
            # command = "hadoop fs -put " + serialization_dir + " /clipper/"
            # print(command)
            # os.system(command)
        p = subprocess.Popen(["hadoop", "fs", "-put", serialization_dir, "/clipper/"], stdout=subprocess.PIPE)
        output, error = p.communicate()
        if p.returncode != 0:
            print(error)
            print(output)
            sys.exit("Save model to HDFS failed %d %s %s" % (p.returncode, output, error))
        # modelPath=str(serialization_dir).split['/'][-1]
        tempPath = os.path.basename(os.path.normpath(serialization_dir))
        print("H2O model saved on HDFS at : /clipper/" + tempPath)
        return a
