#!/usr/bin/env python

import json
import StringIO
import unittest

from csvkit.exceptions import NonUniqueKeyColumnException
from csvkit.utilities.csvjson import CSVJSON

class TestCSVJSON(unittest.TestCase):
    def test_simple(self):
        args = ['examples/dummy.csv']
        output_file = StringIO.StringIO()

        utility = CSVJSON(args, output_file)
        utility.main()

        self.assertEqual(output_file.getvalue(), '[{"a": "1", "c": "3", "b": "2"}]')

    def test_indentation(self):
        args = ['-i', '4', 'examples/dummy.csv']
        output_file = StringIO.StringIO()

        utility = CSVJSON(args, output_file)
        utility.main()

        self.assertEqual(output_file.getvalue(), '[\n    {\n        "a": "1", \n        "c": "3", \n        "b": "2"\n    }\n]')

    def test_keying(self):
        args = ['-k', 'a', 'examples/dummy.csv']
        output_file = StringIO.StringIO()
        
        utility = CSVJSON(args, output_file)
        utility.main()

        self.assertEqual(output_file.getvalue(), '{"1": {"a": "1", "c": "3", "b": "2"}}')

    def test_duplicate_keys(self):
        args = ['-k', 'a', 'examples/dummy3.csv']
        output_file = StringIO.StringIO()
        
        utility = CSVJSON(args, output_file)

        self.assertRaises(NonUniqueKeyColumnException, utility.main)

    def test_geojson(self):
        args = ['--lat', 'latitude', '--lon', 'longitude', 'examples/test_geo.csv']
        output_file = StringIO.StringIO()
        
        utility = CSVJSON(args, output_file)
        utility.main()

        geojson = json.loads(output_file.getvalue())

        self.assertEqual(geojson['type'], 'FeatureCollection')
        self.assertEqual(len(geojson['features']), 17)

        for feature in geojson['features']:
            self.assertEqual(feature['type'], 'Feature')
            self.assertFalse('id' in feature)
            self.assertEqual(len(feature['properties']), 10)
            
            geometry = feature['geometry']

            self.assertEqual(len(geometry['coordinates']), 2)
            self.assertTrue(isinstance(geometry['coordinates'][0], float))
            self.assertTrue(isinstance(geometry['coordinates'][1], float))

    def test_geojson_with_id(self):
        args = ['--lat', 'latitude', '--lon', 'longitude', '-k', 'slug', 'examples/test_geo.csv']
        output_file = StringIO.StringIO()
        
        utility = CSVJSON(args, output_file)
        utility.main()

        geojson = json.loads(output_file.getvalue())

        self.assertEqual(geojson['type'], 'FeatureCollection')
        self.assertEqual(len(geojson['features']), 17)

        for feature in geojson['features']:
            self.assertEqual(feature['type'], 'Feature')
            self.assertTrue('id' in feature)
            self.assertEqual(len(feature['properties']), 9)
            
            geometry = feature['geometry']

            self.assertEqual(len(geometry['coordinates']), 2)
            self.assertTrue(isinstance(geometry['coordinates'][0], float))
            self.assertTrue(isinstance(geometry['coordinates'][1], float))

