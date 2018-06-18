from enum import Enum

class ReturnType(Enum):
    BIN = 0
    HEX = 1
    TAB = 2

class Feature(Enum):
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

    @staticmethod
    def GetAll():
        return (Feature.ENTROPY_TOTAL.value*2)-1

    @staticmethod
    def GetEveryFeature():
        return [
            Feature.AVERAGE,Feature.AVERAGE_TOTAL,
            Feature.STANDARD_DEVIATION,Feature.STANDARD_DEVIATION_TOTAL,
            Feature.SKEWNESS,Feature.SKEWNESS_TOTAL,
            Feature.KURTOSIS,Feature.KURTOSIS_TOTAL,
            Feature.ZERO_CROSSING_RATE,Feature.ZERO_CROSSING_RATE_TOTAL,
            Feature.CORRELATION,Feature.CORRELATION_TOTAL,
            Feature.DC_COMPONENT,Feature.DC_COMPONENT_TOTAL,
            Feature.ENERGY,Feature.ENERGY_TOTAL,
            Feature.ENTROPY,Feature.ENTROPY_TOTAL,
        ]

class FeatureManagement():
    value = 0

    def __init__(self):
        self.value = Feature.GetAll()

    def Add(self,feature):
        try:
            f = feature.value
        except AttributeError:
            f = feature

        self.value = (self.value | f)
        if f == Feature.AVERAGE_TOTAL:
            self.Add(Feature.AVERAGE)
        if f == Feature.STANDARD_DEVIATION_TOTAL:
            self.Add(Feature.STANDARD_DEVIATION)
        if f == Feature.SKEWNESS_TOTAL:
            self.Add(Feature.SKEWNESS)
        if f == Feature.KURTOSIS_TOTAL:
            self.Add(Feature.KURTOSIS)
        if f == Feature.ZERO_CROSSING_RATE_TOTAL:
            self.Add(Feature.ZERO_CROSSING_RATE)
        if f == Feature.CORRELATION_TOTAL:
            self.Add(Feature.CORRELATION)

        if f == Feature.DC_COMPONENT_TOTAL:
            self.Add(Feature.DC_COMPONENT)
        if f == Feature.ENERGY_TOTAL:
            self.Add(Feature.ENERGY)
        if f == Feature.ENTROPY_TOTAL:
            self.Add(Feature.ENTROPY)

    def Remove(self,feature):
        try:
            f = feature.value
        except AttributeError:
            f = feature

        self.value = (self.value ^ f)

        if f == Feature.AVERAGE:
            self.Remove(Feature.AVERAGE_TOTAL)
        if f == Feature.STANDARD_DEVIATION:
            self.Remove(Feature.STANDARD_DEVIATION_TOTAL)
        if f == Feature.SKEWNESS:
            self.Remove(Feature.SKEWNESS_TOTAL)
        if f == Feature.KURTOSIS:
            self.Remove(Feature.KURTOSIS_TOTAL)
        if f == Feature.ZERO_CROSSING_RATE:
            self.Remove(Feature.ZERO_CROSSING_RATE_TOTAL)
        if f == Feature.CORRELATION:
            self.Remove(Feature.CORRELATION_TOTAL)

        if f == Feature.DC_COMPONENT:
            self.Remove(Feature.DC_COMPONENT_TOTAL)
        if f == Feature.ENERGY:
            self.Remove(Feature.ENERGY_TOTAL)
        if f == Feature.ENTROPY:
            self.Remove(Feature.ENTROPY_TOTAL)

    def GetAll(self,return_type=ReturnType.BIN):
        if return_type == ReturnType.HEX:
            return hex(self.value)
        if return_type == ReturnType.BIN:
            return bin(self.value)
        if return_type == ReturnType.TAB:
            d = []
            alls = Feature.GetEveryFeature()
            for a in alls:
                if self.Has(a):
                    d.append(a)
            return d

    def Has(self, a):
        return (self.value & a.value)


