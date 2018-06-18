import math
import numpy
import os
import csv

from Feature import FeatureManagement, Feature

class FeatureExtractor():
    devices = []

    headers = []
    features = {}

    avg = {}
    deviation = {}
    skewness = {}
    kurtosis = {}
    zcr = {}
    correlations = {}

    fft_data = {}
    fft_dc = {}
    fft_energy = {}
    fft_entropy = {}

    TOTAL_NAME = "Total"
    FeatureManagement = None

    def __init__(self,feature_management= None):
        if feature_management is None:
            self.FeatureManagement = FeatureManagement()


    def AddDevice(self,obj):
        self.devices.append(obj["name"])
        self.headers.append(obj["tab"])

    def ExtractFeaturesFromFolder(self,folder,output_file=None,class_added=None):
        files = os.listdir(folder)
        if output_file is not None and output_file == "auto":
            last_name = folder.split("/")
            if len(last_name[len(last_name)-1]) == 0:
                last_name = last_name[len(last_name)-2]
            else:
                last_name = last_name[len(last_name)-1]
            output_file = "output/"+last_name+".csv"

        data_combined = []

        for file in files:
            full_path_file = folder + file
            data = self.ExtractDataFromFile(full_path_file)
            data_combined.append(self.ExtractFeatures(data).copy())


        returning_headers = list(data_combined[0].keys())
        if class_added is not None:
            returning_headers += ["class"]
        returning_data = []
        returning_data.append(returning_headers)

        for data in data_combined:
            t = []
            for header in returning_headers:
                if class_added is not None and header == "class":
                    continue
                t.append(data[header])
            if class_added is not None:
                t.append(class_added)

            returning_data.append(t)

        if output_file is not None:
            with open(output_file,"w+", newline='') as filename:
                writer = csv.writer(filename)
                writer.writerows(returning_data)
        return returning_data

    def ExtractDataFromFile(self,file):
        return self._get_data_from_file(file)

    def ExtractFeatures(self,data):
        self.features.clear()

        for device_id in range(0,len(self.devices)):
            device = self.devices[device_id]
            obj = {}
            for column_id in range(0,len(self.headers[device_id])):
                column = self.headers[device_id][column_id]
                obj[column] = data[column]

            if self.FeatureManagement.Has(Feature.AVERAGE):
                self._extract_avg(obj,device_id,device)
            if self.FeatureManagement.Has(Feature.STANDARD_DEVIATION):
                self._extract_deviation(obj,device_id,device)
            if self.FeatureManagement.Has(Feature.SKEWNESS):
                self._extract_skewness(obj,device_id,device)
            if self.FeatureManagement.Has(Feature.KURTOSIS):
                self._extract_kurtosis(obj,device_id,device)
            if self.FeatureManagement.Has(Feature.ZERO_CROSSING_RATE):
                self._extract_zcr(obj,device_id,device)
            if self.FeatureManagement.Has(Feature.CORRELATION):
                self._extract_correlations(obj,device_id,device)

            if self.FeatureManagement.Has(Feature.DC_COMPONENT) or self.FeatureManagement.Has(Feature.ENERGY) or self.FeatureManagement.Has(Feature.ENTROPY):
                self._extract_fft(obj,device_id)
                if self.FeatureManagement.Has(Feature.DC_COMPONENT):
                    self._extract_dc(self.fft_data,device_id,device)
                if self.FeatureManagement.Has(Feature.ENERGY):
                    self._extract_energy(self.fft_data,device_id,device)
                if self.FeatureManagement.Has(Feature.ENTROPY):
                    self._extract_entropy(self.fft_data,device_id,device)

        self._build_features()
        return self.features

    def _get_data_from_file(self,filename):
        headers = []
        data = {}
        with open(filename,"r") as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if len(headers) == 0:
                    headers = row
                    for column in row:
                        data[column] = []
                    continue
                for i in range(0,len(row)):
                    data[headers[i]].append(float(row[i]))
        return data

    def _extract_avg(self,data,column_id,device):
        avg = {}
        columns = self.headers[column_id]
        if self.FeatureManagement.Has(Feature.AVERAGE_TOTAL):
            tot = 0
        for column in columns:
            _avg = sum(data[column]) / len(data[column])
            avg[column] = _avg
            if self.FeatureManagement.Has(Feature.AVERAGE_TOTAL):
                tot += _avg
        if self.FeatureManagement.Has(Feature.AVERAGE_TOTAL):
            avg[device+"_"+self.TOTAL_NAME] = (tot/len(data))

        for key in avg:
            self.avg[key] = avg[key]

    def _extract_deviation(self,data,column_id,device):
        deviation = {}
        columns = self.headers[column_id]
        if self.FeatureManagement.Has(Feature.STANDARD_DEVIATION_TOTAL):
            tot = 0
        for column in columns:
            avg = self.avg[column]
            _deviation = 0
            for item in data[column]:
                _deviation += math.pow((item-avg),2)
            _deviation = math.sqrt(_deviation / len(data[column]))
            deviation[column] = _deviation
            if self.FeatureManagement.Has(Feature.STANDARD_DEVIATION_TOTAL):
                tot += _deviation

        if self.FeatureManagement.Has(Feature.STANDARD_DEVIATION_TOTAL):
            deviation[device+"_"+self.TOTAL_NAME] = (tot/len(data))

        for key in deviation:
            self.deviation[key] = deviation[key]

    def _extract_skewness(self, data, column_id, device):
        skewness = {}
        columns = self.headers[column_id]
        if self.FeatureManagement.Has(Feature.SKEWNESS_TOTAL):
            tot = 0
        for column in columns:
            avg = self.avg[column]
            deviation = self.deviation[column]

            _skewness = 0
            for item in data[column]:
                _skewness += (math.pow((item - avg), 3) / math.pow(deviation,3))
            _skewness = _skewness * (len(data[column])/((len(data[column])-1)*(len(data[column])-2)))
            skewness[column] = _skewness
            if self.FeatureManagement.Has(Feature.SKEWNESS_TOTAL):
                tot += _skewness

        if self.FeatureManagement.Has(Feature.SKEWNESS_TOTAL):
            skewness[device + "_"+self.TOTAL_NAME] = (tot / len(data))

        for key in skewness:
            self.skewness[key] = skewness[key]

    def _extract_kurtosis(self, data, column_id, device):
        kurtosis = {}
        columns = self.headers[column_id]
        if self.FeatureManagement.Has(Feature.KURTOSIS_TOTAL):
            tot = 0
        for column in columns:
            avg = self.avg[column]
            deviation = self.deviation[column]

            _kurtosis = 0
            for item in data[column]:
                _kurtosis += (math.pow((item - avg), 4) / math.pow(deviation,4))
            _kurtosis = _kurtosis * (len(data[column])/((len(data[column])-1)*(len(data[column])-2)))
            _kurtosis = _kurtosis - (3*math.pow(len(data[column])-1,2))/((len(data[column])-2)*(len(data[column])-3))
            
            kurtosis[column] = _kurtosis
            if self.FeatureManagement.Has(Feature.KURTOSIS_TOTAL):
                tot += _kurtosis

        if self.FeatureManagement.Has(Feature.KURTOSIS_TOTAL):
            kurtosis[device + "_"+self.TOTAL_NAME] = (tot / len(data))

        for key in kurtosis:
            self.kurtosis[key] = kurtosis[key]

    def _extract_zcr(self,data,column_id,device):
        zcr = {}
        columns = self.headers[column_id]
        if self.FeatureManagement.Has(Feature.ZERO_CROSSING_RATE_TOTAL):
            tot = 0

        for column in columns:
            _zcr = 0
            previous_value = None
            for value in data[column]:
                if previous_value is None:
                    previous_value = value
                    continue

                if value * previous_value < 0:
                    _zcr += 1
                previous_value = value
            _zcr /= len(data[column])
            zcr[column] = _zcr
            if self.FeatureManagement.Has(Feature.ZERO_CROSSING_RATE_TOTAL):
                tot += _zcr
        if self.FeatureManagement.Has(Feature.ZERO_CROSSING_RATE_TOTAL):
            zcr[device+"_"+self.TOTAL_NAME] = (tot/len(data))

        for key in zcr:
            self.zcr[key] = zcr[key]

    def _extract_correlations(self, data, column_id, device):
        correlations = {}
        couples = []
        headers = self.headers[column_id]
        if self.FeatureManagement.Has(Feature.CORRELATION_TOTAL) and self.FeatureManagement.Has(Feature.AVERAGE_TOTAL) and self.FeatureManagement.Has(Feature.STANDARD_DEVIATION_TOTAL):
            _headers = headers + [self.TOTAL_NAME]
        else:
            _headers = headers

        for i in range(0,len(_headers)):
            for j in range(i+1,len(_headers)):
                couples.append([_headers[i],_headers[j]])

        for duo in couples:
            _correlation = 0
            if duo[1] == self.TOTAL_NAME:
                _correlation = self._extract_correlation_total(data,duo[0],headers,device)
            else:
                _correlation = self._extract_correlation_single(data,duo[0],duo[1])
            correlations['-'.join(duo)] = _correlation

        for key in correlations:
            self.correlations[key] = correlations[key]

    def _extract_correlation_single(self, data, column_id1, column_id2):
        length = len(data[column_id1])
        mult = 0
        for value_id in range(0,length):
            v1 = data[column_id1][value_id]
            v2 = data[column_id2][value_id]
            mult += (v1 * v2)
        mult /= length

        cov = mult - (self.avg[column_id1]*self.avg[column_id2])
        std = self.deviation[column_id1] * self.deviation[column_id2]
        return cov / std

    def _extract_correlation_total(self,data,column_id,headers,device):
        length = len(data[column_id])
        mult = 0

        for value_id in range(0,length):
            v1 = data[column_id][value_id]
            v2 = 0
            for header in headers:
                v2 += data[header][value_id]
            mult += (v1 * v2)

        mult /= length

        cov = mult - (self.avg[column_id]*self.avg[device+"_"+self.TOTAL_NAME])
        std = self.deviation[column_id] * self.deviation[device+"_"+self.TOTAL_NAME]
        return cov / std

    def _extract_fft(self,data,column_id):
        fft = {}
        columns = self.headers[column_id]
        for column in columns:
            fft[column] = numpy.fft.fft([d for d in data[column]])
        self.fft_data = fft

    def _extract_dc(self, data, column_id, device):
        dc = {}
        columns = self.headers[column_id]
        if self.FeatureManagement.Has(Feature.DC_COMPONENT_TOTAL):
            tot = 0
        for column in columns:
            _dc = 0

            for value in data[column]:
                _dc += math.pow(numpy.real(value),2)
            _dc /= len(data[column])

            dc[column] = _dc
            if self.FeatureManagement.Has(Feature.DC_COMPONENT_TOTAL):
                tot += _dc
        if self.FeatureManagement.Has(Feature.DC_COMPONENT_TOTAL):
            dc[device+"_"+self.TOTAL_NAME] = (tot/len(data))

        for key in dc:
            self.fft_dc[key] = dc[key]

    def _extract_energy(self, data, column_id, device):
        energy = {}
        columns = self.headers[column_id]
        if self.FeatureManagement.Has(Feature.ENERGY_TOTAL):
            tot = 0
        for column in columns:
            _energy = 0

            for value in data[column]:
                _energy += (math.pow(numpy.real(value),2) + math.pow(numpy.imag(value),2))
            _energy /= len(data[column])

            energy[column] = _energy
            if self.FeatureManagement.Has(Feature.ENERGY_TOTAL):
                tot += _energy

        if self.FeatureManagement.Has(Feature.ENERGY_TOTAL):
            energy[device + "_" + self.TOTAL_NAME] = (tot / len(data))

        for key in energy:
            self.fft_energy[key] = energy[key]
            
    def _extract_entropy(self, data, column_id, device):
        entropy = {}
        columns = self.headers[column_id]
        if self.FeatureManagement.Has(Feature.ENTROPY_TOTAL):
            tot = 0
        for column in columns:
            _entropy = 0

            for value in data[column]:
                _entropy += self._entropy_subcomputation(value,len(data[column]),self.fft_energy[column])
            _entropy *= -1

            entropy[column] = _entropy
            if self.FeatureManagement.Has(Feature.ENTROPY_TOTAL):
                tot += _entropy

        if self.FeatureManagement.Has(Feature.ENTROPY_TOTAL):
            entropy[device + "_" + self.TOTAL_NAME] = (tot / len(data))

        for key in entropy:
            self.fft_entropy[key] = entropy[key]

    def _entropy_subcomputation(self,cplx,N,Energy):
        return (math.pow(numpy.real(cplx),2) + math.pow(numpy.imag(cplx),2)) / (N - Energy )

    def _build_features(self):
        items = []

        if self.FeatureManagement.Has(Feature.AVERAGE):
            items.append({"name":"Average","tab":self.avg})
        if self.FeatureManagement.Has(Feature.STANDARD_DEVIATION):
            items.append({"name":"Deviation","tab":self.deviation})
        if self.FeatureManagement.Has(Feature.SKEWNESS):
            items.append({"name":"Skewness","tab":self.skewness})
        if self.FeatureManagement.Has(Feature.KURTOSIS):
            items.append({"name":"Kurtosis","tab":self.kurtosis})
        if self.FeatureManagement.Has(Feature.ZERO_CROSSING_RATE):
            items.append({"name":"ZCR","tab":self.zcr})
        if self.FeatureManagement.Has(Feature.CORRELATION):
            items.append({"name":"Correlation","tab":self.correlations})


        if self.FeatureManagement.Has(Feature.DC_COMPONENT):
            items.append({"name":"DC_Component","tab":self.fft_dc})
        if self.FeatureManagement.Has(Feature.ENERGY):
            items.append({"name":"Energy","tab":self.fft_energy})
        if self.FeatureManagement.Has(Feature.ENTROPY):
            items.append({"name":"Entropy","tab":self.fft_entropy})

        for item in items:
            for attr in item["tab"]:
                self.features[item["name"]+"_"+attr] = item["tab"][attr]

    def MergeFiles(self, folder,output_file=None):
        list_files = os.listdir(folder)
        headers = []
        data = []
        for file in list_files:
            full_path = folder + file
            with open(full_path,"r") as filename:
                reader = csv.reader(filename)
                start = True
                for row in reader:
                    if start:
                        if len(headers)==0:
                            headers = row
                        start = False
                        continue
                    data.append(row)

        full_data = [headers] + data

        if output_file is not None:
            if output_file == "auto":
                output_file = folder+"merging.csv"

            with open(output_file,"w+",newline='') as filename:
                writer = csv.writer(filename)
                writer.writerows(full_data)

        return full_data