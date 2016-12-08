#!/usr/bin/python

from factor_regression import FactorRegression

import csv
import math
import numpy as np
import sys

class NorthCarolinaPredictor(FactorRegression):
  def _GetColumns(self):
    return ['00INT', 'RES2012', 'PCTWHITE', 'PCTCOLLEGE']

  def _IsValidRow(self, row):
    if len(row) != 11:
      print(len(row))
      return False
    if not row[0] or row[0].startswith('County'):
      return False
    return True

  def _GetJurisdiction(self, row):
    return row[0]

  def _GetCollegePercent(self, row):
    return float(row[9]) / 100.0

  def _GetWhitePercent(self, row):
    return float(row[10]) / 100.0

  def _GetVotes(self, row, year, party):
    idx = None
    if year == 2012:
      if party == 'D':
        idx = 2
      elif party == 'R':
        idx = 1
    elif year == 2016:
      if party == 'D':
        idx = 5
      elif party == 'R':
        idx = 4
    if idx is None:
      return None
    return self._GetVotesFromString(row[idx])


def main(argv=None):
  if argv is None:
    argv = sys.argv
  if len(argv) != 3:
    print('Usage: %s <mode> <tsv_file>' % (argv[0]))
    return 1
  np.set_printoptions(edgeitems=20)
  vp = NorthCarolinaPredictor()
  assert vp.IsValidMode(argv[1])
  vp.LoadResults(argv[2], argv[1])
  model = vp.Regress(False)
  return 0

if __name__ == '__main__':
  sys.exit(main())
