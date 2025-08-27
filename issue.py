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
