# (c) 2012-2018 Dativa, all rights reserved
# -----------------------------------------
#  This code is licensed under MIT license (see license.txt for details)

from csv import QUOTE_MINIMAL, QUOTE_ALL, QUOTE_NONNUMERIC, QUOTE_NONE
import pandas as pd
import logging
from io import StringIO, BytesIO
from csv import Sniffer, Error
from chardet.universaldetector import UniversalDetector
import boto3
import s3fs

logger = logging.getLogger("dativa.tools.pandas.csv")


class FpCSVEncodingError(Exception):
    def __init__(self, message="CSV Encoding Error"):
        self.message = message


class CSVHandler:
    """
    A wrapper for pandas CSV handling to read and write dataframes
    that is provided in pandas with consistent CSV parameters and
    sniffing the CSV parameters automatically.
    Includes reading a CSV into a dataframe, and writing it out to a string.

    Parameters
    ----------
    base_path: the base path for any CSV file read, if passed as a string
    detect_parameters: whether the encoding of the CSV file should be automatically detected
    encoding: the encoding of the CSV files, defaults to UTF-8
    delimiter: the delimeter used in the CSV, defaults to ,
    header: the index of the header row, or -1 if there is no header
    skiprows: the number of rows at the beginning of file to skip
    quotechar: the quoting character to use, defaults to ""
    include_index: specifies whether the index should be written out, default to False
    compression: specifies whether the data should be encoded, default to 'infer'
    nan_values: an array of possible NaN values, the first of which is used when writign out, defaults to None
    line_terminator: the line terminator to be used
    quoting: the level of quoting, defaults to QUOTE_MINIMAL
    decimal: the decimal character, defaults to '.'
    chunksize: if specified the CSV is written out in chunks


    """

    base_path = ""
    DEFAULT_ENCODING = "UTF-8"
    DEFAULT_DELIMITER = ","
    DEFAULT_HEADER = 0
    DEFAULT_QUOTECHAR = "\""
    S3_PREFIX = "s3://"

    detect_parameters = False
    base_path = ""
    include_index = False
    compression = 'infer'
    nan_values = None
    line_terminator = None
    quoting = QUOTE_MINIMAL
    decimal = '.'
    chunksize = None
    encoding = DEFAULT_ENCODING
    delimiter = DEFAULT_DELIMITER
    header = DEFAULT_HEADER
    skiprows = 0
    quotechar = DEFAULT_QUOTECHAR

    def __init__(self,
                 **kwargs):

        self._process_kwargs(**kwargs)

        # validate if base path is a folder and exists
        # support file like objects

    def value_or_default(self, args, name):
        if name in args:
            setattr(self, name, args[name])
        elif "csv_{0}".format(name) in args:
            setattr(self, name, args["csv_{0}".format(name)])

    def _process_kwargs(self, **kwargs):

        self.value_or_default(kwargs, "detect_parameters")
        self.value_or_default(kwargs, "base_path")
        self.value_or_default(kwargs, "include_index")
        self.value_or_default(kwargs, "compression")
        self.value_or_default(kwargs, "nan_values")
        self.value_or_default(kwargs, "line_terminator")
        self.value_or_default(kwargs, "quoting")
        self.value_or_default(kwargs, "decimal")
        self.value_or_default(kwargs, "chunksize")
        self.value_or_default(kwargs, "encoding")
        self.value_or_default(kwargs, "delimiter")
        self.value_or_default(kwargs, "header")
        self.value_or_default(kwargs, "skiprows")
        self.value_or_default(kwargs, "quotechar")

        if self.compression not in ['gzip', 'bz2', 'zip', 'xz', None, 'infer']:
            raise ValueError("Invalid value for compression parameter")

        if self.quoting not in [QUOTE_MINIMAL, QUOTE_ALL, QUOTE_NONNUMERIC, QUOTE_NONE]:
            raise ValueError("Invalid value for quoting parameter")

    @property
    def _has_header(self):
        """
        Returns whether the CSV file has a header or not
        """
        if self.header == -1:
            return False
        else:
            return True

    @property
    def _default_nan(self):
        if self.nan_values is None:
            return ''
        else:
            return self.nan_values[0]

    def _is_s3_file(self, file):
        if type(file) is str:
            return (self.base_path + file).startswith(self.S3_PREFIX)
        else:
            return False

    def _get_file(self, file):
        return self.base_path + file

    def _get_df_from_raw(self, file, force_dtype):
        """
        Returns a dataframe from a passed file
        """

        if self.line_terminator is not None:
            df = pd.read_csv(self._get_file(file),
                             encoding=self.encoding,
                             sep=self.delimiter,
                             quotechar=self.quotechar,
                             header=self.header if self._has_header else None,
                             skiprows=self.skiprows,
                             skip_blank_lines=False,
                             dtype=force_dtype,
                             compression=self.compression,
                             na_values=self.nan_values,
                             lineterminator=self.line_terminator,
                             quoting=self.quoting,
                             decimal=self.decimal)
        else:
            df = pd.read_csv(self._get_file(file),
                             encoding=self.encoding,
                             sep=self.delimiter,
                             quotechar=self.quotechar,
                             header=self.header if self._has_header else None,
                             skiprows=self.skiprows,
                             skip_blank_lines=False,
                             dtype=force_dtype,
                             compression=self.compression,
                             na_values=self.nan_values,
                             quoting=self.quoting,
                             decimal=self.decimal)
        return df

    @staticmethod
    def _get_encoding(sample):
        detector = UniversalDetector()
        for line in BytesIO(sample).readlines():
            detector.feed(line)
            if detector.done:
                break
        detector.close()
        return detector.result["encoding"]

    def _sniff_parameters(self, file):
        # if we are using the default parameters, then attempt to guess them
        if (self.encoding == self.DEFAULT_ENCODING and
            self.delimiter == self.DEFAULT_DELIMITER and
            self.header == self.DEFAULT_HEADER and
                self.quotechar == self.DEFAULT_QUOTECHAR):
            logger.debug("sniffing file type")

            # create a sample...
            full_path = self._get_file(file)
            if full_path.startswith(self.S3_PREFIX):
                # This is an S3 location
                logger.debug("s3 location")
                fs = s3fs.S3FileSystem(anon=False)
                with fs.open(full_path, "rb") as f:
                    sample = f.read(1024 * 1024)
            else:
                with open(full_path, mode="rb") as f:
                    sample = f.read(1024 * 1024)

            # get the encoding...
            self.encoding = self._get_encoding(sample)
            if self.encoding is None:
                self.encoding = 'windows-1252'

            # now decode the sample
            try:
                sample = sample.decode(self.encoding)
            except UnicodeDecodeError:
                self.encoding = "windows-1252"
                try:
                    sample = sample.decode(self.encoding)
                except UnicodeDecodeError as e:
                    raise FpCSVEncodingError(e)

            # use the sniffer to detect the parameters...
            sniffer = Sniffer()
            try:
                dialect = sniffer.sniff(sample)
            except Error as e:
                raise FpCSVEncodingError(e)

            self.delimiter = dialect.delimiter
            if sniffer.has_header(sample):
                self.header = 0
            else:
                self.header = -1
            self.quotechar = dialect.quotechar

            if (self.encoding != self.DEFAULT_ENCODING or
                self.delimiter != self.DEFAULT_DELIMITER or
                self.header != self.DEFAULT_HEADER or
                    self.quotechar != self.DEFAULT_QUOTECHAR):
                logger.debug("Found file type {0}, {1}, {2}".format(self.encoding, self.delimiter, self.header))
                return True
            else:
                logger.debug("No new file type found")

        return False

    def _attempt_get_df_from_raw(self, file, force_dtype):

        try:
            return self._get_df_from_raw(file, force_dtype)
        except (UnicodeError, UnicodeDecodeError, pd.errors.ParserError) as e:
            if self.detect_parameters:
                if self._sniff_parameters(file):
                    logger.debug("second attempt to load")
                    return self._get_df_from_raw(file, force_dtype)
            raise FpCSVEncodingError(e)

    def load_df(self, file, force_dtype=None, **kwargs):
        """
        Synonym for 'get_dataframe' for consistency with 'save_df'
        """
        return self.get_dataframe(file, force_dtype, **kwargs)

    def get_dataframe(self, file, force_dtype=None, **kwargs):
        """
        Opens a CSV file using the specified configuration for the class
        and raises an exception if the encoding is unparseable
        """
        self._process_kwargs(**kwargs)

        df = self._attempt_get_df_from_raw(file, force_dtype)

        return df

    def _to_csv(self, df, buffer):

        if self.line_terminator is not None:
            df.to_csv(buffer,
                      encoding=self.encoding,
                      sep=self.delimiter,
                      quotechar=self.quotechar,
                      header=self._has_header,
                      index=self.include_index,
                      compression=None if self.compression == 'infer' else self.compression,
                      na_rep=self._default_nan,
                      line_terminator=self.line_terminator,
                      quoting=self.quoting,
                      decimal=self.decimal,
                      chunksize=self.chunksize
                      )
        else:
            df.to_csv(buffer,
                      encoding=self.encoding,
                      sep=self.delimiter,
                      quotechar=self.quotechar,
                      header=self._has_header,
                      index=self.include_index,
                      compression=None if self.compression == 'infer' else self.compression,
                      na_rep=self._default_nan,
                      quoting=self.quoting,
                      decimal=self.decimal,
                      chunksize=self.chunksize
                      )

    def save_df(self, df, file, **kwargs):
        """
        Writes a formatted string from a DataFrame using the specified
        configuration for the class the file. Detects if base_path is
        an S3 location and saves data there if required.
        """

        self._process_kwargs(**kwargs)

        if self._is_s3_file(file):
            # This is an S3 location
            s3 = boto3.client('s3')
            buffer = StringIO()

            self._to_csv(df, buffer)

            buffer.seek(0)

            # Save buffered data to file in S3 bucket
            from dativa.tools.aws import S3Location
            loc = S3Location(self._get_file(file))
            s3.put_object(Bucket=loc.bucket,
                          Key=loc.key,
                          ContentEncoding=self.encoding,
                          ContentType="text/csv",
                          Body=buffer.read().encode(self.encoding))

        else:
            self._to_csv(df, self._get_file(file))

    def df_to_string(self, df, **kwargs):
        """
        Returns a formatted string from a dataframe using the specified
        configuration for the class
        """

        self._process_kwargs(**kwargs)

        buffer = StringIO()
        self._to_csv(df, buffer)

        return buffer.getvalue()
