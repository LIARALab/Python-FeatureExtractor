# Python FeatureExtractor

[![Languages](https://img.shields.io/badge/languages-En-green.svg)]()
[![Licence Apache2](https://img.shields.io/hexpm/l/plug.svg)](http://www.apache.org/licenses/LICENSE-2.0)

## Description

This project is a **Python3 application** designed to be used with CSV files.
It extracts features from any given dataset recorded with inertial sensors like _Accelerometer_, _Gyroscope_ or _Magnetometer_.
This library is adaptable to be able to extract features from any amount of devices with any amount of axes (accelerometer 2-axes and gyroscope 3-axes, or a single accelerometer 3-axes for example).

## Features

Any instance of the **FeatureExtractor** object has an instance of **FeatureManagement** containing the features.
For each sensor, the following features can be extracted :

    AVERAGE                     = 0x01
    AVERAGE_TOTAL               = 0x02
    STANDARD_DEVIATION          = 0x04
    STANDARD_DEVIATION_TOTAL    = 0x08
    SKEWNESS                    = 0x10
    SKEWNESS_TOTAL              = 0x20
    KURTOSIS                    = 0x40
    KURTOSIS_TOTAL              = 0x80
    ZERO_CROSSING_RATE          = 0x100
    ZERO_CROSSING_RATE_TOTAL    = 0x200
    CORRELATION                 = 0x400
    CORRELATION_TOTAL           = 0x800
    DC_COMPONENT                = 0x1000
    DC_COMPONENT_TOTAL          = 0x2000
    ENERGY                      = 0x4000
    ENERGY_TOTAL                = 0x8000
    ENTROPY                     = 0x10000
    ENTROPY_TOTAL               = 0x20000

Every features activated results in a single number easily understandable with binary reading.
The management of these features is really simple : Just use the method "Add" or "Remove" to do so !
Also, if a feature need its first form to be computed and it is not activated, it won't be computed (for example _ENERGY_ to compute _ENERGY_TOTAL_ ; if _ENERGY_ is disabled, _ENERGY_TOTAL_ is also disabled).

Check this following example to see how it is managed !
```python
from Feature import Feature, ReturnType
from FeatureExtractor import FeatureExtractor

Extractor = FeatureExtractor()

print(Extractor.FeatureManagement.GetAll(return_type=ReturnType.BIN))
>>> 0b111111111111111111

Extractor.FeatureManagement.Remove(Feature.DC_COMPONENT_TOTAL)
Extractor.FeatureManagement.Remove(Feature.ENERGY_TOTAL)
Extractor.FeatureManagement.Remove(Feature.ENTROPY_TOTAL)

print(Extractor.FeatureManagement.GetAll(return_type=ReturnType.BIN))
>>> 0b010101111111111111

Extractor.FeatureManagement.Add(Feature.ENTROPY_TOTAL)

print(Extractor.FeatureManagement.GetAll(return_type=ReturnType.BIN))
>>> 0b110101111111111111
```

Is is good to notice that 3 features come from the frequential domain, needing FFT Data (increase of computation number).
If you want to spare them, just **Remove** them as presented in the previous example !

## Installation

Here is the list of dependencies needed to make the library work :

 * Python3 ([https://www.python.org/](https://www.python.org/))
 * Numpy ([http://www.numpy.org/](http://www.numpy.org/))

To install this library, just clone this Git Repo using this command :

    git clone https://github.com/kevinchapron/Python-FeatureExtractor.git

## Usage

To run `example.py`, we use the dataset of activities created by the [LIARA Laboratory](https://github.com/LIARALab).
The example will automatically download the dataset from the Git repo.

The FeatureExtractor class has many methods :

```python
Extractor.AddDevice({"name":"Accelerometer","tab":["ax","ay","az"]})
```

* **name** is the full name of the sensor
* **tab** is a list containing the columns associated with the device

```python
DATA = {"c1":[0,1,2,3],"c2":[1,2,3,4],"c3":[2,3,4,5]}
Extractor.ExtractFeatures(DATA)
```

DATA is a formatted dict containing each column name as key, and data related to this column in it.<br />
The "DATA" variable is an example of structure for this CSV File :

| c1  | c2  | c3  |
| --- | --- | --- |
|  0  |  1  |  2  |
|  1  |  2  |  3  |
|  2  |  3  |  4  |
|  3  |  4  |  5  |

```python
Extractor.ExtractDataFromFile(FILENAME)
```
The result of this method is the CSV Data formatted as used in this library (can be combined with ExtractFeatures !!)

```python
Extractor.ExtractFeaturesFromFolder(FOLDER,output_file=None,class_added=None)
```

* This method returns a **CSV-Like** dataset with every features asked (one line is computed from one file).
* FOLDER is the full path to the folder containing every CSV files.
* output_file is optional, and has three possible values :<br />
    - **"None"** &rarr; Output file won't be created.<br />
    - **"auto"** &rarr; Output file will be created in "output" folder, with the name of the folder.
    - **"custom_string"** &rarr; Output file will be created at the location specified.
* class_added is optional, and has two possible values : <br />
    - **"None"** &rarr; Class won't be added.<br />
    - **"custom_string"** &rarr; Class will be added at the end of the resulting data with this custom string as value and **"class"** as column name.

```python
Extractor.MergeFiles(FOLDER,output_file=None)
```
* This method returns a **CSV-Like** dataset with the merge of the files in specified folder.
* FOLDER is the full path to the folder containing every CSV files.
* output_file is optional, and has three possible values :<br />
    - **"None"** &rarr; Output file won't be created.<br />
    - **"auto"** &rarr; Output file will be created in the folder specified, with the name `"merging.csv"`.
    - **"custom_string"** &rarr; Output file will be created at the location specified.

## More information

This project has been created to extract features of real-time data, in the **[LIARA](http://liara.uqac.ca/)** laboratory
(_Laboratoire d'Intelligence Ambiante pour la Reconnaissance d'Activités_), at the
« Université du Québec À Chicoutimi (**[UQAC](http://www.uqac.ca/)**) »

## Author

**[Kévin CHAPRON](mailto:kevin.chapron1@uqac.ca)** - _2018_

## License

    Copyright 2016 Kévin Chapron

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.


