import unittest
import click

from metamodel.generators.shexgen import cli
from tests.test_scripts.clicktestcase import ClickTestCase

update_test_files = False


class GenShExTestCase(ClickTestCase):
    testdir = "genshex"
    click_ep = cli
    prog_name = "gen-shex"

    def test_help(self):
        self.do_test("--help", 'help', update_test_file=update_test_files)
        self.assertFalse(update_test_files, "Updating test files")

    def test_meta(self):
        self.maxDiff = None
        self.do_test(self.metamodel_file + ' -f json -C', 'metashex.json', update_test_file=update_test_files)
        self.do_test(self.metamodel_file + ' -f rdf', 'metashex.ttl', update_test_file=update_test_files)
        self.do_test(self.metamodel_file, 'metashex.shex', update_test_file=update_test_files)
        self.do_test(self.metamodel_file + ' -f shex', 'metashex.shex', update_test_file=update_test_files)
        self.do_test(self.metamodel_file + f' -f xsv', 'meta_error',
                     update_test_file=update_test_files, error=click.exceptions.BadParameter)
        self.do_test(self.metamodel_file + ' -f json -c', 'metashexnc.json', update_test_file=update_test_files)
        self.do_test(self.metamodel_file + ' -f rdf -c', 'metashexnc.ttl', update_test_file=update_test_files)
        self.do_test(self.metamodel_file + ' -c', 'metashexnc.shex', update_test_file=update_test_files)
        self.assertFalse(update_test_files, "Updating test files")

    # TODO: Need to add RDF difference or cannonical representation to do this test
    def test_biolink(self):
        self.maxDiff = None
        self.do_test(self.biolink_file, "biolink-modelshex.shex", update_test_file=update_test_files)
        self.do_test(self.biolink_file + " -f json", "biolink-modelshex.json", update_test_file=update_test_files)
        self.do_test(self.biolink_file + " -f rdf", "biolink-modelshex.ttl", update_test_file=update_test_files)
        self.do_test(self.biolink_file + " -c", "biolink-modelshexnc.shex", update_test_file=update_test_files)
        self.do_test(self.biolink_file + " -c -f json", "biolink-modelshexnc.json", update_test_file=update_test_files)
        self.do_test(self.biolink_file + " -c -f rdf", "biolink-modelshexnc.ttl", update_test_file=update_test_files)
        self.assertFalse(update_test_files, "Updating test files")


if __name__ == '__main__':
    unittest.main()
