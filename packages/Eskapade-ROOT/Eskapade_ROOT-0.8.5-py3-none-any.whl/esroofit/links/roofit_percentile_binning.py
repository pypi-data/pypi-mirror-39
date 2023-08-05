"""Project: Eskapade - A python-based package for data analysis.

Class: RooFitPercentileBinning

Created: 2017/06/28

Description:
    Algorithm to evaluate percentile binning for given set
    of roofit observables. The binning configuration is stored
    in the observable(s)

Authors:
    KPMG Advanced Analytics & Big Data team, Amstelveen, The Netherlands

Redistribution and use in source and binary forms, with or without
modification, are permitted according to the terms listed in the file
LICENSE.
"""

import ROOT
import numpy as np
import pandas as pd

from eskapade import process_manager, Link, DataStore, StatusCode
from esroofit import data_conversion, roofit_utils, RooFitManager

class RooFitPercentileBinning(Link):
    """Evaluate percentile binning for given variable set."""

    def __init__(self, **kwargs):
        """Initialize link instance.

        :param str name: name of link
        :param str read_key: key of input data to read from data store; either a RooDataSet or pandas DataFrame
        :param bool from_ws: if true, pick up input roodataset from workspace, not datastore (default is False)
        :param dict var_number_of_bins: number of percentile bins per observable
        :param dict var_binning: existing binning dict, to append binnings to.
        :param str binning_name: name of binning configuration to assign to percentile binning. Also key for datastore.
        :param dict var_min_value: min value for certain variable (optional)
        :param dict var_max_value: max value for certain variable (optional)
        :param float min_value: min value for all variables. Default is None (optional)
        :param float max_value: max value for all variables. Default is None (optional)
        :param bool non_central_binning: if false, use regular RooBinning class. Default is RooNonCentralBinning.
        :param list columns: list of columns to make percentile bins for. picks up default number of bins (optional).
        :param int default_number_of_bins: default number of bins for continuous observables. Default setting is 10.
        """
        # initialize link and process arguments
        Link.__init__(self, kwargs.pop('name', 'RooFitPercentileBinning'))
        self._process_kwargs(kwargs, read_key='', from_ws=False, binning_name='percentile', var_number_of_bins={}, var_binning={},
                             var_min_value={}, var_max_value={}, min_value=None, max_value=None, non_central_binning=True,
                             default_number_of_bins=10, columns=[])
        self.check_extra_kwargs(kwargs)

    def initialize(self):
        """Initialize the link.."""
        # check input arguments
        self.check_arg_types(read_key=str, binning_name=str, default_number_of_bins=int)
        self.check_arg_types(recurse=True, allow_none=False, columns=str)
        self.check_arg_vals('read_key', 'binning_name', 'var_number_of_bins')

        # make sure Eskapade RooFit library is loaded for the RooNonCentralBinning class
        roofit_utils.load_libesroofit()

        return StatusCode.Success

    def execute(self):
        """Execute the link."""
        ds = process_manager.service(DataStore)
        ws = process_manager.service(RooFitManager).ws

        # basic checks on contensts of the data frame
        if self.from_ws:
            data = ws.data(self.read_key)
            if data is None:
                raise RuntimeError('No data with key "{}" in workspace.'.format(self.read_key))
        else:
            if self.read_key not in ds:
                raise KeyError('Key "{}" not found in datastore.'.format(self.read_key))
            data = ds[self.read_key]

        # add self.columns to var_number_of_bins, which are processed below
        for col in self.columns:
            if col not in self.var_number_of_bins:
                self.var_number_of_bins[col] = self.default_number_of_bins

        # check presence of all columns; check data type
        columns = list(self.var_number_of_bins.keys())
        if isinstance(data, ROOT.RooDataSet):
            if data.numEntries() == 0:
                raise AssertionError('RooDataSet "{}" is empty.'.format(self.read_key))
            varset = data.get(0)
            for col in self.var_number_of_bins:
                if not varset.find(col):
                    raise AssertionError('Column "{}" not found in input roodataset.'.format(col))
            df = data_conversion.rds_to_df(data, columns, ignore_lost_records=True)
        elif isinstance(data, pd.DataFrame):
            if len(data.index) == 0:
                raise AssertionError('RooDataSet "{}" is empty.'.format(self.read_key))
            for col in self.var_number_of_bins:
                if col not in data.columns:
                    raise AssertionError('Column "{}" not found in input dataframe.'.format(col))
            df = data[columns]
        else:
            raise TypeError('Object "{0:s}" not of type RooDataSet/DataFrame (got "{1!s}").'
                            .format(self.read_key, type(data)))
        # continuing below with df

        # evaluate and set quantiles per observable
        for col, nbins in self.var_number_of_bins.items():
            self.logger.debug('Creating {n:d} percentile bins for column "{col}".', n=nbins, col=col)
            qs = np.linspace(0, 1, nbins + 1).tolist()
            bin_edges = df[col].quantile(qs).values
            # column variable is a RooRealVar
            col_var = ws.var(col) if ws.var(col) else data.get(0).find(col) if isinstance(data, ROOT.RooDataSet) else None
            if col_var and not ws.var(col):
                # add variables to workspace if they don't exist there yet. useful for consistent use.
                ws.put(col_var)
                col_var = ws.var(col)
            if col_var:
                # determine if variable has predefined range, that is also not infinity
                range_min = col_var.getMin() if col_var.getMin() != -ROOT.RooNumber.infinity() else None
                range_max = col_var.getMax() if col_var.getMax() != ROOT.RooNumber.infinity() else None
                # if range exists, use it to *replace* outer quantiles if further away
                # this avoids min and max quantiles very close to edges of range
                if range_min and range_min < bin_edges[0]:
                    bin_edges[0] = range_min
                if range_max and range_max > bin_edges[-1]:
                    bin_edges[-1] = range_max
            # has a manual range been set? if so, overwrite existing range
            # this means an update the final bin_edges - may have changed b/c of user var_min and var_max
            # i.e. no guarantuee then that first and last bin are correct quantiles
            var_min = self.var_min_value.get(col, self.min_value if self.min_value else bin_edges[0])
            var_max = self.var_max_value.get(col, self.max_value if self.max_value else bin_edges[-1])
            if col_var:
                col_var.setRange(var_min, var_max)
            binning = ROOT.RooNonCentralBinning() if self.non_central_binning else ROOT.RooBinning()
            binning.setRange(var_min, var_max)
            for i in range(0, nbins+1):
                bv = bin_edges[i]
                binning.addBoundary(bv)
            if self.non_central_binning:
                # evaluate average value of each bin, from data
                for i in range(binning.numBins()):
                    keep = df[col].between(binning.binLow(i), binning.binHigh(i))
                    bc = df[keep][col].mean()
                    binning.setBinCenter(i, bc)
            # try adding binning to corresponding variables in workspace
            if col_var:
                col_var.setBinning(binning, self.binning_name)
            self.var_binning[col] = binning

        # cleanup of temporary df
        if isinstance(data, ROOT.RooDataSet):
            del df

        # storage
        ds[self.binning_name] = self.var_binning

        return StatusCode.Success
