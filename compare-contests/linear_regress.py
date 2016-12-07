#!/usr/bin/python

from scipy import stats

import csv
import math

class ContestRegression(object):
  def __init__(self, party, independent, dependent, county):
    self._party = party
    self._independent = independent
    self._dependent = dependent
    self._county = county
    self._independent_data = dict()
    self._dependent_data = dict()
    self._county_idata = dict()
    self._county_ddata = dict()

  def Load(self, filename):
    with open(filename, 'r') as fp:
      csvreader = csv.reader(fp, delimiter=self._GetDelimiter())
      for row in csvreader:
        self._ProcessOneLine(row)
#    print('%4d %4d %4d %4d' % (len(self._independent_data),
#      len(self._dependent_data), len(self._county_idata), len(self._county_ddata)))

  def Regress(self):
    if len(self._independent_data) == 0:
      print('Loaded no data for contest "%s" party "%s"' % (self._independent, self._party))
      return
    if len(self._dependent_data) == 0:
      print('Loaded no data for contest "%s" party "%s"' % (self._dependent, self._party))
      return
    y = []
    x = []
    for precinct,votes in self._independent_data.iteritems():
      if precinct not in self._dependent_data:
        continue
      x.append(votes)
      y.append(self._dependent_data[precinct])
    if not x or len(x) != len(y):
      print('Mismatched or empty data')
      return
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    print('Slope=%6.4f Intercept=%6.4f R^2=%.4f p=%.6f' % (slope, intercept,
      r_value**2, p_value))
    self._PrintResiduals(slope, intercept)

  def _ProcessOneLine(self, row):
    if not self._IsValidRow(row):
      return
    if not self._IsValidParty(row):
      return
    votes = self._GetVotes(row)
    if votes is None:
      return
    precinct = self._GetPrecinctName(row)
    if precinct is None:
      return
    contest_name = self._GetContestName(row)
    county_name = self._GetCountyName(row)
    if contest_name is None or county_name is None:
      return
    if contest_name == self._independent:
      if county_name != self._county:
        self._independent_data[precinct] = votes
      else:
        self._county_idata[precinct] = votes
    elif contest_name == self._dependent:
      if county_name != self._county:
        self._dependent_data[precinct] = votes
      else:
        self._county_ddata[precinct] = votes

  def _PrintResiduals(self, slope, intercept):
    independent_dict = None
    dependent_dict = None
    if len(self._county_idata) > 0 and len(self._county_ddata) > 0:
      independent_dict = self._county_idata
      dependent_dict = self._county_ddata
    else:
      independent_dict = self._independent_data
      dependent_dict = self._dependent_data
    for precinct,logvotes in sorted(independent_dict.iteritems()):
      if precinct not in dependent_dict:
        continue
      actual = int(math.e**dependent_dict[precinct])
      predict_exponent = intercept + slope*logvotes
      predict = int(math.e**predict_exponent)
      diff = actual - predict
      pct_error = (1.0 * diff) / predict
      print('%-38s\t%7d\t%7d\t%7d\t%7.4f' % (precinct, actual, predict, diff, pct_error))

  """Override the rest of these functions in the subclasses."""
  def _GetDelimiter(self):
    return ','

  def _GetMinVotes(self):
    return 20

  def _IsValidRow(self, row):
    return False

  def _IsValidParty(self, row):
    return False

  def _GetVotes(self, row):
    return None

  def _GetPrecinctName(self, row):
    return None

  def _GetContestName(self, row):
    return None

  def _GetCountyName(self, row):
    return None
