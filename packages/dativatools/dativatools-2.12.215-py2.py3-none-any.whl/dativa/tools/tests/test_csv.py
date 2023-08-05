import unittest
import warnings
import os
import tempfile
import shutil
import logging
from pandas.util.testing import assert_frame_equal
from dativa.tools.aws import S3Client
from dativa.tools.pandas import CSVHandler, FpCSVEncodingError

logger = logging.getLogger("dativa.tools.csv.tests")


class CSVFileTests(unittest.TestCase):
    s3_bucket = "gd.dativa.test"
    saved_suffix = ".saved"
    root_prefix = "csvhandler"
    s3 = None
    local_base_path = None

    @classmethod
    def setUpClass(cls):

        # Original test data location
        cls.orig_base_path = "{0}/test_data/".format(
            os.path.dirname(os.path.abspath(__file__)))

        # Upload test data to s3
        cls.s3 = S3Client()
        cls.s3.delete_files(cls.s3_bucket, cls.root_prefix)
        cls.s3.put_folder(cls.orig_base_path + cls.root_prefix,
                          cls.s3_bucket, destination=cls.root_prefix)
        cls.s3_base_path = "s3://{}/".format(cls.s3_bucket)

        # Save test data to local folder
        cls.local_base_path = tempfile.mkdtemp() + '/'
        os.mkdir(cls.local_base_path + cls.root_prefix)

    @classmethod
    def tearDownClass(cls):
        # Delete uploaded/created files
        cls.s3.delete_files(cls.s3_bucket, cls.root_prefix)
        shutil.rmtree(cls.local_base_path)

    def _run_file_tests(self, location):

        warnings.simplefilter("ignore", ResourceWarning)

        # Test file location
        test_path = self.root_prefix + '/' + location
        os.mkdir(self.local_base_path + test_path)

        # Get list of the files
        files = self.s3.list_files(
            self.s3_bucket, prefix=test_path, suffix='.csv')

        # Create the handlers
        csv_orig = CSVHandler(base_path=self.orig_base_path,
                              detect_parameters=True)
        csv_s3 = CSVHandler(base_path=self.s3_base_path,
                            detect_parameters=True)
        csv_local = CSVHandler(base_path=self.local_base_path,
                               detect_parameters=True)
        csv_empty = CSVHandler(detect_parameters=True)

        # Alternate how the path is split
        use_empty_base = True

        for file in files:

            logger.info("testing file {0}".format(file))

            # Read file from S3
            if use_empty_base:
                df1 = csv_empty.load_df(self.s3_base_path + file)
            else:
                df1 = csv_s3.load_df(file)

            # Write file to S3
            if use_empty_base:
                csv_empty.save_df(df1, self.s3_base_path +
                                  file + self.saved_suffix)
            else:
                csv_s3.save_df(df1, file + self.saved_suffix)

            # Check DataFrames match
            if use_empty_base:
                df2 = csv_empty.load_df(
                    self.s3_base_path + file + self.saved_suffix)
            else:
                df2 = csv_s3.load_df(file + self.saved_suffix)
            assert_frame_equal(df1, df2)

            # Check strings match
            str1 = csv_s3.df_to_string(df1)
            str2 = csv_s3.df_to_string(df2)
            self.assertMultiLineEqual(str1, str2)

            # Read file locally
            if use_empty_base:
                df3 = csv_empty.load_df(self.orig_base_path + file)
            else:
                df3 = csv_orig.load_df(file)

            # Write file locally
            if use_empty_base:
                csv_empty.save_df(df3, self.local_base_path +
                                  file + self.saved_suffix)
            else:
                csv_local.save_df(df3, file + self.saved_suffix)

            # Check DataFrames match
            if use_empty_base:
                df4 = csv_empty.load_df(
                    self.local_base_path + file + self.saved_suffix)
            else:
                df4 = csv_local.load_df(file + self.saved_suffix)
            assert_frame_equal(df3, df4)

            # Check strings match
            str3 = csv_orig.df_to_string(df3)
            str4 = csv_local.df_to_string(df4)
            self.assertMultiLineEqual(str3, str4)

            use_empty_base = not use_empty_base

    def test_anonymization_files(self):

        self._run_file_tests('anonymization')

    def test_date_files(self):

        self._run_file_tests('date')

    def test_generic_files(self):

        self._run_file_tests('generic')

    def test_lookup_files(self):

        self._run_file_tests('lookup')

    def test_number_files(self):

        self._run_file_tests('number')

    def test_session_files(self):

        self._run_file_tests('session')

    def test_string_files(self):

        self._run_file_tests('string')

    def test_unique_files(self):

        self._run_file_tests('unique')


class CSVOtherTests(unittest.TestCase):

    local_base_path = None



    @classmethod
    def setUpClass(cls):
        # Original test data location
        cls.orig_base_path = "{0}/test_data/csvhandler/".format(
            os.path.dirname(os.path.abspath(__file__)))

        cls.local_base_path = tempfile.mkdtemp() + '/'

    @classmethod
    def tearDownClass(cls):
        # Delete uploaded/created files
        shutil.rmtree(cls.local_base_path)

    def test_encoding_error(self):

        with self.assertRaises(FpCSVEncodingError):
            csv = CSVHandler(base_path=self.orig_base_path)
            csv.load_df("lookup/test_cities_reference1252.csv")

    def test_csv_parameter(self):
        csv = CSVHandler(base_path=self.orig_base_path)
        csv.load_df("lookup/test_cities_reference1252.csv",
                    csv_encoding="Windows-1252")

    def test_invalid_compression(self):
        with self.assertRaises(ValueError):
            CSVHandler(base_path=self.orig_base_path, compression="garbage")

    def test_quoting_error(self):
        with self.assertRaises(ValueError):
            CSVHandler(base_path=self.orig_base_path, quoting=-1)

    def test_no_header(self):
        csv = CSVHandler(base_path=self.orig_base_path)
        df=csv.load_df("lookup/test_cities_reference1252.csv",
                       csv_encoding="Windows-1252",
                       header=-1,
                       nan_values=["NaN"],
                       force_dtype=str)

        csv2 = CSVHandler(base_path=self.local_base_path,
                          header=-1)
        csv2.save_df(df, "banana.csv")
        df2 = csv2.load_df("banana.csv",
                           force_dtype=str)

        assert_frame_equal(df,
                           df2,
                           check_index_type=False)

    def test_sniffer(self):
        csv = CSVHandler(base_path=self.orig_base_path)
        csv._sniff_parameters("generic/email_test.csv")
