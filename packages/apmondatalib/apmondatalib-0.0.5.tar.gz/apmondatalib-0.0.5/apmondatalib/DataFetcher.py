import sys
import pymongo
import datetime
from enum import IntEnum


def create_mongodb_connection(host, port):
    return pymongo.MongoClient('mongodb://%s:%d/' % (host, port))


class SensorType(IntEnum):
    Humidity = 1
    Temperature = 2
    Light = 3
    Motion = 4


def create_raw_data_fetcher(host, port, database, sensor_id, default_page_size, time_offset=9):
    return SensorRawDataFetcher(host, port, database, sensor_id, default_page_size, time_offset)


def create_daily_summary_fetcher(host, port, database, sensor_id, default_page_size, time_offset=9):
    return DailyDataFetcher(host, port, database, sensor_id, default_page_size, time_offset)


class RawData:
    id = ""
    sensor_id = ""
    type = 0
    value = 0.0
    timestamp = None

    def __init__(self, sensor_id, type, json):
        self.sensor_id = sensor_id
        self.type = type
        self.id = json["_id"]
        self.value = json["value"]
        self.timestamp = json["timestamp"]

    def __str__(self):
        return "{ RawData: _id = %s, sensor_id = %s, type = %s, value = %f, timestamp = %s }" % (
            self.id, self.sensor_id, self.type, self.value, self.timestamp)

    def __repr__(self):
        return "{ RawData: _id = %s, sensor_id = %s, type = %s, value = %f, timestamp = %s }" % (
            self.id, self.sensor_id, self.type, self.value, self.timestamp)


class DailySummary:
    id = ""
    sensor_id = ""
    sensor_type = 0
    year = 0
    month = 0
    day = 0
    average = 0
    min = 0
    max = 0
    data_set = []

    def __init__(self, sensor_id, sensor_type, json=None):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type

        if json is not None:
            self.id = json["_id"]
            self.year = json["year"]
            self.month = json["month"]
            self.day = json["day"]
            self.average = json["average"]
            self.min = json["min"]
            self.max = json["max"]

            data_set = json["dataSet"]
            for h in range(0, 24):
                key = str(h)
                if key in data_set:
                    self.data_set.append(HourlySummary(data_set[key]))
                else:
                    self.data_set.append(create_empty_hourly_summary(h))

    def __str__(self) -> str:
        return "{ DailySummary: id = %s, sensor_id = %s, sensor_type = %d, " \
               "year = %d, month = %d, day = %d, " \
               "min = %d, max = %d, average = %d, " \
               "count(dataSet) = %d }" % (
                   self.id, self.sensor_id, self.sensor_type,
                   self.year, self.month, self.day,
                   self.min, self.max, self.average,
                   len(self.data_set))

    def __str__(self) -> str:
        return "{ DailySummary: id = %s, sensor_id = %s, sensor_type = %d, " \
               "year = %d, month = %d, day = %d, " \
               "min = %d, max = %d, average = %d, " \
               "count(data_set) = %d }" % (
                   self.id, self.sensor_id, self.sensor_type,
                   self.year, self.month, self.day,
                   self.min, self.max, self.average,
                   len(self.data_set))


def create_empty_hourly_summary(hour):
    return HourlySummary({"hour": hour, "min": -1, "max": -1, "average": -1})


class HourlySummary:
    hour = 0
    average = 126
    min = 0
    max = 0

    def __init__(self, json):
        self.hour = json["hour"]
        self.average = json["average"]
        self.min = json["min"]
        self.max = json["max"]

    def __str__(self) -> str:
        return "{ HourlySummary: hour = %d, min = %f, max = %f, average = %f }" % (
            self.hour, self.min, self.max, self.average)

    def __repr__(self) -> str:
        return "{ HourlySummary: min = %s, max = %f, average = %s }" % (
            self.min, self.max, self.average)


def convert_cursor_to_raw_data(sensor_id, sensor_type, cursor):
    result = []
    for x in cursor:
        result.append(RawData(sensor_id, sensor_type, x))

    return result


def calculate_skip_position(page_number, page_size):
    return page_size * (page_number - 1)


class SensorRawDataFetcher:
    mongo = None
    collection = None

    sensor_id = ""
    default_page_size = 0
    time_offset = 0

    default_field_visibility = {"_id": 1, "value": 1, "timestamp": 1}

    def __init__(self, host, port, database, sensor_id, default_page_size, time_offset):
        self.host = host
        self.port = port
        self.database = database
        self.mongo = create_mongodb_connection(host, port)
        self.collection = self.mongo[database]["sensor_data"]

        self.sensor_id = sensor_id
        self.default_page_size = default_page_size
        self.time_offset = time_offset

    def read(self, sensor_type, page_number, page_size=None):
        if page_size is None:
            page_size = self.default_page_size

        skips = calculate_skip_position(page_number, page_size)
        return convert_cursor_to_raw_data(
            self.sensor_id, sensor_type,
            self.collection.find({
                "$query": {"sensorId": self.sensor_id, "type": sensor_type.value},
                "$orderby": {"timestamp": 1}
            }, self.default_field_visibility).skip(skips).limit(page_size))

    def count(self, sensor_type):
        return self.collection.count({"sensorId": self.sensor_id, "type": sensor_type.value})

    def count_total_pages(self, sensor_type, page_size=None):
        if page_size is None:
            page_size = self.default_page_size

        total_count = self.count(sensor_type)
        page_count = total_count / page_size
        if total_count % page_size:
            page_count += 1
        return page_count

    # def read_in_range(self, sensor_type, date, page_number, page_size):
    #     print date.day
    #     skips = calculate_skip_position(page_number, page_size)
    #     return convert_cursor_to_raw_data(
    #         self.sensor_id, sensor_type,
    #         self.collection.find({"sensorId": self.sensor_id, "type": sensor_type.value},
    #                              self.default_field_visibility).skip(skips).limit(page_size))

    def read_humidity(self, page_number, page_size=None):
        if page_size is None:
            page_size = self.default_page_size

        return self.read(SensorType.Humidity, page_number, page_size)

    def read_temperature(self, page_number, page_size=None):
        if page_size is None:
            page_size = self.default_page_size

        return self.read(SensorType.Temperature, page_number, page_size)

    def read_light(self, page_number, page_size=None):
        if page_size is None:
            page_size = self.default_page_size

        return self.read(SensorType.Light, page_number, page_size)

    def read_motion(self, page_number, page_size=None):
        if page_size is None:
            page_size = self.default_page_size

        return self.read(SensorType.Motion, page_number, page_size)

    def count_humidity(self):
        return self.count(SensorType.Humidity)

    def count_temperature(self):
        return self.count(SensorType.Temperature)

    def count_light(self):
        return self.count(SensorType.Light)

    def count_motion(self):
        return self.count(SensorType.Motion)

    def count_total_humidity_pages(self, page_size):
        return self.count_total_pages(SensorType.Humidity, page_size)

    def count_total_temperature_pages(self, page_size):
        return self.count_total_pages(SensorType.Temperature, page_size)

    def count_total_light_pages(self, page_size):
        return self.count_total_pages(SensorType.Light, page_size)

    def count_total_motion_pages(self, page_size):
        return self.count_total_pages(SensorType.Motion, page_size)

    def read_in_range(self, sensor_type, from_date, to_date, page_number, page_size=None):
        if page_size is None:
            page_size = self.default_page_size

        from_date = from_date.astimezone(datetime.timezone.utc)
        to_date = to_date.astimezone(datetime.timezone.utc)

        skips = calculate_skip_position(page_number, page_size)
        return convert_cursor_to_raw_data(
            self.sensor_id, sensor_type,
            self.collection.find(
                {"$query": {"sensorId": self.sensor_id, "type": sensor_type.value,
                            "$and": [{"timestamp": {"$gte": from_date}}, {"timestamp": {"$lte": to_date}}]},
                 "$orderby": {"timestamp": 1}
                 },
                self.default_field_visibility).skip(skips).limit(page_size))

    def read_humidity_in_range(self, from_date, to_date, page_number, page_size=None):
        if page_size is None:
            page_size = self.default_page_size

        return self.read_in_range(SensorType.Humidity, from_date, to_date, page_number, page_size)

    def read_temperature_in_range(self, from_date, to_date, page_number, page_size=None):
        if page_size is None:
            page_size = self.default_page_size

        return self.read_in_range(SensorType.Temperature, from_date, to_date, page_number, page_size)

    def read_light_in_range(self, from_date, to_date, page_number, page_size):
        if page_size is None:
            page_size = self.default_page_size

        return self.read_in_range(SensorType.Light, from_date, to_date, page_number, page_size)

    def read_motion_in_range(self, from_date, to_date, page_number, page_size):
        if page_size is None:
            page_size = self.default_page_size

        return self.read_in_range(SensorType.Motion, from_date, to_date, page_number, page_size)


def calc_average(result):
    filtered = list(filter(lambda x: x.average >= 0, result))
    if len(filtered) == 0:
        return -1

    total = 0
    for x in filtered:
        total += x.average

    return total / len(filtered)


def find_max(result):
    max_value = 0
    for x in result:
        if max_value < x.max:
            max_value = x.max
    return max_value


def find_min(result):
    min_value = sys.maxsize
    for x in result:
        if min_value > x.min:
            min_value = x.min
    return min_value


class DailyDataFetcher:
    mongo = None
    collection = None

    sensor_id = ""
    default_page_size = 0
    time_offset = 0

    default_field_visibility = {
        "dataSet.0.rawDataLinks": 0,
        "dataSet.1.rawDataLinks": 0,
        "dataSet.2.rawDataLinks": 0,
        "dataSet.3.rawDataLinks": 0,
        "dataSet.4.rawDataLinks": 0,
        "dataSet.5.rawDataLinks": 0,
        "dataSet.6.rawDataLinks": 0,
        "dataSet.7.rawDataLinks": 0,
        "dataSet.8.rawDataLinks": 0,
        "dataSet.9.rawDataLinks": 0,
        "dataSet.10.rawDataLinks": 0,
        "dataSet.11.rawDataLinks": 0,
        "dataSet.12.rawDataLinks": 0,
        "dataSet.13.rawDataLinks": 0,
        "dataSet.14.rawDataLinks": 0,
        "dataSet.15.rawDataLinks": 0,
        "dataSet.16.rawDataLinks": 0,
        "dataSet.17.rawDataLinks": 0,
        "dataSet.18.rawDataLinks": 0,
        "dataSet.19.rawDataLinks": 0,
        "dataSet.20.rawDataLinks": 0,
        "dataSet.21.rawDataLinks": 0,
        "dataSet.22.rawDataLinks": 0,
        "dataSet.23.rawDataLinks": 0}

    def __init__(self, host, port, database, sensor_id, default_page_size, time_offset):
        self.host = host
        self.port = port
        self.database = database
        self.mongo = create_mongodb_connection(host, port)
        self.collection = self.mongo[database]["daily_summaries"]

        self.sensor_id = sensor_id
        self.default_page_size = default_page_size
        self.time_offset = time_offset

    def read(self, sensor_type, year, month, day):

        today_data = self.collection.find_one({
            "sensorId": self.sensor_id,
            "type": sensor_type,
            "year": year,
            "month": month,
            "day": day
        }, self.default_field_visibility)

        if self.time_offset == 0:
            return DailySummary(self.sensor_id, sensor_type, today_data)

        basis_day = datetime.datetime(year, month, day, 0, 0, 0, 0)
        start = 24 - self.time_offset

        days = []
        sets = []

        if self.time_offset > 0:
            prev_day = basis_day - datetime.timedelta(days=1)
            days.append(prev_day)
            days.append(basis_day)
        else:
            next_day = basis_day + datetime.timedelta(days=1)
            days.append(basis_day)
            days.append(next_day)

        for i in range(0, 2):
            t = self.collection.find_one({
                "sensorId": self.sensor_id,
                "type": sensor_type,
                "year": days[i].year,
                "month": days[i].month,
                "day": days[i].day
            }, self.default_field_visibility)

            if t is None:
                sets.append(None)
            else:
                sets.append(t["dataSet"])

        if sets[0] is None and sets[1] is None:
            return None

        result = []

        for i in range(start, 24):
            key = str(i)
            h = i - start
            if sets[0] is not None and key in sets[0]:
                hourly_data = HourlySummary(sets[0][key])
                hourly_data.hour = h
                result.append(hourly_data)
            else:
                result.append(create_empty_hourly_summary(h))

        for i in range(0, 24 - self.time_offset):
            key = str(i)
            h = i + self.time_offset
            if sets[1] is not None and key in sets[1]:
                hourly_data = HourlySummary(sets[1][key])
                hourly_data.hour = h
                result.append(hourly_data)
            else:
                result.append(create_empty_hourly_summary(h))

        summary = DailySummary(self.sensor_id, sensor_type)
        summary.year = year
        summary.month = month
        summary.day = day
        summary.min = find_min(result)
        summary.max = find_max(result)
        summary.average = calc_average(result)
        summary.data_set = result

        return summary
