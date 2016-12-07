#!/usr/bin/python

from linear_regress import ContestRegression

import csv
import math
import sys

class NorthCarolinaLoader(ContestRegression):
  def _GetDelimiter(self):
    return '\t'

  def _IsValidRow(self, row):
    return len(row) == 14

  def _IsValidParty(self, row):
    return row[7] == self._party

  def _GetVotes(self, row):
    if not row[13] or int(row[13]) < self._GetMinVotes():
      return None
    return math.log(int(row[13]))

  def _GetPrecinctName(self, row):
    precinct = '%s:%s' % (row[0], row[2])
    return precinct.replace(' ', '_')

  def _GetContestName(self, row):
    return row[5]

  def _GetCountyName(self, row):
    return row[0]


def main(argv=None):
  if argv is None:
    argv = sys.argv
  if len(argv) != 5 and len(argv) != 6:
    print('Usage: %s <datafile> <party> <indep_contest> <dep_contest> [<county>]' %(argv[0]))
    return 1
  county = None
  if len(argv) == 6:
    county = argv[5]
  nc = NorthCarolinaLoader(argv[2], argv[3], argv[4], county)
  nc.Load(argv[1])
  nc.Regress()
  return 0

if __name__ == '__main__':
  sys.exit(main())
