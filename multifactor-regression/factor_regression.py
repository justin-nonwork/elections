#!/usr/bin/python3

import csv
import math
import numpy as np
import re
import statsmodels.api as sm
import sys

class FactorRegression(object):
  def __init__(self):
    self._REGRESS_COLUMNS = self._GetColumns()
    self._rows = dict()
    self._values = dict()

  def _GetColumns(self):
    return None

  def LoadResults(self, filename, mode):
    with open(filename, 'r') as filep:
      csvp = csv.reader(filep, delimiter=self._GetDelimiter())
      for row in csvp:
        self._ProcessOneRow(row, mode)

  def IsValidMode(self, mode):
    return mode == 'D' or mode == 'R'

  def _ProcessOneRow(self, row, mode):
    if not self._IsValidRow(row):
      return
    rowvals = dict.fromkeys(self._REGRESS_COLUMNS)
    juris = self._NormalizeJurisdictionName(self._GetJurisdiction(row))
    # Contant (intercept) column
    rowvals['00INT'] = 1
    rowvals['PCTCOLLEGE'] = self._GetCollegePercent(row)
    rowvals['PCTWHITE'] = self._GetWhitePercent(row)
    rowvals['RES2012'] = self._GetVotes(row, 2012, mode)
    self._values[juris] = self._GetVotes(row, 2016, mode)
    self._rows[juris] = rowvals

  def _NormalizeJurisdictionName(self, name):
    if name is None or not name:
      return name
    return re.sub(r'\\s+', '_', name.upper())

  def Regress(self, print_data):
    a = np.ndarray(shape=(len(self._rows), len(self._REGRESS_COLUMNS)))
    b = np.zeros(shape=(len(self._rows)))
    rn = 0
    if print_data:
      print('Found %d rows' % (len(self._rows)))
      print('Columns')
      print('\t'.join(sorted(self._REGRESS_COLUMNS)))
    for juris,cols in self._rows.iteritems():
      if not self._IsValidInputData(cols):
        continue
      b[rn] = self._values[juris]
      cn = 0
      for c in sorted(self._REGRESS_COLUMNS):
        a[rn,cn] = cols[c]
        cn += 1
      if print_data:
        print('\t'.join(str(x) for x in a[rn:rn+1,][0].tolist()))
      rn += 1
    a.resize((rn, len(self._REGRESS_COLUMNS)))
    b.resize(rn)
    if print_data:
      print('LogValue')
      print('\n'.join(str(x) for x in b.tolist()))
    results = sm.OLS(b, a).fit()
    print(results.summary(yname='log(Votes)',
      xname=sorted(self._REGRESS_COLUMNS), alpha=0.01))
    i = 0
    for juris,cols in sorted(self._rows.iteritems()):
      p = []
      for c in sorted(self._REGRESS_COLUMNS):
        p.append(cols[c])
      pred = results.predict(p)
      diff = math.e**self._values[juris] - math.e**pred
      print('%-20s\t%7d\t%7d\t%7.4f\t%7d' % (juris, math.e**pred,
        math.e**self._values[juris], diff / math.e**pred, diff))
    return results

  def _GetVotesFromString(self, value):
    if not value:
      return None
    votes = int(value.replace(',', ''))
    if votes < self._GetMinVotes():
      return None
    return math.log(votes)

  def _IsValidInputData(self, rowdict):
    for k,v in rowdict.iteritems():
      if v is None or math.isnan(v):
        print('Invalid value in row')
        print(v)
        return False
    return True

  """Override these functions to control behavior."""
  def _GetDelimiter(self):
    return '\t'

  def _GetMinVotes(self):
    return 20

  def _IsValidRow(self, row):
    return False

  def _GetJurisdiction(self, row):
    return None

  def _GetCollegePercent(self, row):
    return None

  def _GetWhitePercent(self, row):
    return None

  def _GetVotes(self, row, year, party):
    return None


