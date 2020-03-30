import datetime
from ..factory import APIFactory
import dummydata_generator
import logging
import time

# ---------------------Benchmarking for stress testing-----------------
log_file = logging.FileHandler(filename='benchmarking_dummydata.log', mode='a', encoding='utf-8')
fmt = logging.Formatter()
log_file.setFormatter(fmt)
logger = logging.Logger(name='benchmarking', level=logging.INFO)
logger.addHandler(log_file)
logger.info(msg=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
logger.info(msg='Benchmarking start - Record code execution time :')
logger.info(msg='Method_name        wall_time    cpu_time')

if __name__ == "__main__":
    # Provides access to the condition database api
    factory = APIFactory()
    cdb_api = factory.construct_DB_API("conditionsDatabase/tests/test_mongodb/test_mongodb_config.yml")

    # Benchmarking adding one detector to the conditions database
    detector_and_parent = dummydata_generator.create_big_detectors(1, None, "SingleDetector", 0)
    detector_name = detector_and_parent[0]
    detector_parent = detector_and_parent[1]

    wall_time_start = time.time()
    cpu_time_start = time.clock()

    cdb_api.add_detector(detector_name, detector_parent)

    wall_time_end = time.time()
    cpu_time_end = time.clock()
    logger.info(msg='add One detector to the database%15.6f%13.6f' % (
        wall_time_end - wall_time_start, cpu_time_end - cpu_time_start))

    # Benchmarking adding high hierarchy of detectors, subdetctors and each has
    # one condition to the condition database
    group_detector_parent = []
    dummydata_generator.create_multilevel_detectors(5, 2, "detector", None, group_detector_parent)

    wall_time_start = time.time()
    cpu_time_start = time.clock()
    for detector_and_parent in group_detector_parent:
        detector_name = detector_and_parent[0]
        detector_parent = detector_and_parent[1]
        cdb_api.add_detector(detector_name, detector_parent)
        values = {"T853_MA_853": [814, 973, 65]}

        reconstructed_detector_id = ""
        if detector_parent is None:
            reconstructed_detector_id = detector_name
        else:
            reconstructed_detector_id = detector_parent + "/" + detector_name

        cdb_api.add_condition(reconstructed_detector_id,
                              "daniel",
                              "tag1",
                              datetime.datetime.now(),
                              values,
                              "calibration",
                              datetime.datetime.now(),
                              datetime.datetime.now())

    wall_time_end = time.time()
    cpu_time_end = time.clock()
    logger.info(
        msg='create Complex Structure%15.6f%13.6f' % (wall_time_end - wall_time_start, cpu_time_end - cpu_time_start))

    # Benchmarking adding a massive condition to a specific detector/subdetector
    # the conditions database when it has complex structure
    daniel = dummydata_generator.create_big_daniel()
    wall_time_start = time.time()
    cpu_time_start = time.clock()
    cdb_api.add_condition("detector1/subdetector1/subsubdetector1/subsubsubdetector1/subsubsubsubdetector1",
                          "daniel",
                          "tag2",
                          datetime.datetime.now(),
                          daniel,
                          "calibration",
                          datetime.datetime.now(),
                          datetime.datetime.now())
    wall_time_end = time.time()
    cpu_time_end = time.clock()
    logger.info(msg='add One massive Condition to the deepest level%15.6f%13.6f' % (
        wall_time_end - wall_time_start, cpu_time_end - cpu_time_start))

    # Benchmarking retrieveing a condition which is located in the deepest level of the hierarchy
    wall_time_start = time.time()
    cpu_time_start = time.clock()
    cdb_api.get_condition_by_name_and_tag(
        "detector1/subdetector1/subsubdetector1/subsubsubdetector1/subsubsubsubdetector1", "daniel", "tag2")
    wall_time_end = time.time()
    cpu_time_end = time.clock()
    logger.info(msg='add One massive Condition to the deepest level%15.6f%13.6f' % (
        wall_time_end - wall_time_start, cpu_time_end - cpu_time_start))

    # Benchmarking: retrieveing a condition which is located in the deepest level of the hierarchy
    wall_time_start = time.time()
    cpu_time_start = time.clock()
    cdb_api.get_conditions_by_tag(
        "detector1/subdetector1/subsubdetector1/subsubsubdetector1/subsubsubsubdetector1", "tag1")
    wall_time_end = time.time()
    cpu_time_end = time.clock()
    logger.info(msg='add One massive Condition to the deepest level%15.6f%13.6f' % (
        wall_time_end - wall_time_start, cpu_time_end - cpu_time_start))

    # Benchmarking: updating a condition which is located in the deepest level of the hierarchy
    wall_time_start = time.time()
    cpu_time_start = time.clock()
    cdb_api.update_condition_by_name_and_tag(
        "detector1/subdetector1/subsubdetector1/subsubsubdetector1/subsubsubsubdetector1",
        "daniel",
        "tag1",
        "2020-01-01")
    wall_time_end = time.time()
    cpu_time_end = time.clock()
    logger.info(msg='update a Condition at the deepest level%15.6f%13.6f' % (
        wall_time_end - wall_time_start, cpu_time_end - cpu_time_start))
