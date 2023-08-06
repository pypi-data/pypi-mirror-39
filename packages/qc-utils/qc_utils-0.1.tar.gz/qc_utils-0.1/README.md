# qc-utils
QC infrastructure common to several pipelines

For now contains two classes `QCMetric` and `QCMetricRecord` that can be used for representing pipeline quality control metrics.

## Installation

`pip install qc-utils`

## Usage

`from qc_utils.qcmetric import QCMetric, QCMetricRecord`

Creating metric objects is done by  `new_metric = QCMetric('metric name', {'metric1' : value1, 'metric2' : value2})`. The name and content can be accessed as properties of the object. The content is stored as an `OrderedDict` and the content is sorted by names when object is created. These properties can be now accessed as `new_metric.name` and `new_metric.content`. 

`QCMetricRecord` objects can be created by making an empty record `record = QCMetricRecord()` and then using `add` method to add `QCMetric` objects into the record. Another way is to initialize record from a list of `QCMetric` objects `record = QCMetricRecord([qc_metric1, qc_metric2])`, and possibly using `add` to complement the record later. Names of `QCMetric` objects in a record have to be distinct and an attempt to add a metric with existing name into a `QCMetricRecord` will cause an error. 

