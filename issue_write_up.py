import logging

logging.basicConfig(
    level=logging.DEBUG,  # capture debug and above
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

logger = logging.getLogger(__name__)
import fiona


schema={'properties': {'Anode': 'int32', 'Bnode': 'int32', 'LinkID': 'float', }, 'geometry': 'LineString'}

crs = "EPSG:4326"

coordinates = [(115.638812, -32.62857), (115.637933, -32.631091)]

records = [fiona.Feature(geometry=fiona.Geometry(coordinates=coordinates, type='LineString'), id='23998', 
                         properties=fiona.Properties(Anode=25194, Bnode=25196, LinkID=2519425196))]


with fiona.open(
    "test_links.gpkg",
    "w",
    driver='GPKG',
    crs=crs,
    schema=schema,
) as f:
    print(records)
    # works on 1.9.6 (writes LinkID as a float)
    # at ea24f55bb0b7f5f160f9a1742b2b88c6258f9787 write NULL for LinkID WARNING - fiona.ogrext - Skipping field LinkID: invalid type (2, 0, 'int')
    # at b6e62ccecf31d533d79edc3ad29754197fb9f4b8 fails, OverflowError: value too large to convert to int
    # fails on 1.10.0 
    f.writerecords(records)


# Unexpected behaviour part 2 - dtypes action at a distance
schema2={'properties': {'Anode': 'int64', 'Bnode': 'int32', 'LinkID': 'float', }, 'geometry': 'LineString'}

with fiona.open(
    "test_links2.gpkg",
    "w",
    driver='GPKG',
    crs=crs,
    schema=schema2,
) as f:
    # This works on 1.10.x because setting Anode =int64 triggers all int fields to be int64
    # Setting feature property: key='LinkID', value=2519425196, i=2, setter=<fiona.ogrext.Integer64Field object at 0x73d5bce7dbc0>
    f.writerecords(records)

    


 named field types=
{'int32': <class 'fiona.schema.FionaIntegerType'>, 
 'bool': <class 'fiona.schema.FionaBooleanType'>, 
 'int16': <class 'fiona.schema.FionaInt16Type'>, 
 'int': <class 'fiona.schema.FionaInteger64Type'>, 
 'int64': <class 'fiona.schema.FionaInteger64Type'>, 
 'float': <class 'fiona.schema.FionaRealType'>, 
 'float64': <class 'fiona.schema.FionaRealType'>, 
 'str': <class 'fiona.schema.FionaStringType'>, 
 'date': <class 'fiona.schema.FionaDateType'>, 
 'time': <class 'fiona.schema.FionaTimeType'>, 
 'datetime': <class 'fiona.schema.FionaDateTimeType'>, 
 'bytes': <class 'fiona.schema.FionaBinaryType'>, 
 'List[str]': <class 'fiona.schema.FionaStringListType'>, 
 'list[str]': <class 'fiona.schema.FionaStringListType'>, 
 'json': <class 'fiona.schema.FionaJSONType'>}
ftmap2={
    <class 'fiona.schema.FionaIntegerType'>: (0, 0), 
    <class 'fiona.schema.FionaBooleanType'>: (0, 1), 
    <class 'fiona.schema.FionaInt16Type'>: (0, 2), 
    <class 'fiona.schema.FionaInteger64Type'>: (12, 0), 
    <class 'fiona.schema.FionaRealType'>: (2, 0), 
    <class 'fiona.schema.FionaStringType'>: (4, 0), 
    <class 'fiona.schema.FionaDateType'>: (9, 0), 
    <class 'fiona.schema.FionaTimeType'>: (10, 0), 
    <class 'fiona.schema.FionaDateTimeType'>: (11, 0), 
    <class 'fiona.schema.FionaBinaryType'>: (8, 0), 
    <class 'fiona.schema.FionaStringListType'>: (5, 0), 
    <class 'fiona.schema.FionaJSONType'>: (4, 4)}, 
field_key=(0, 0, 'int')