#!/usr/bin/python

from linear_regress import ContestRegression

import csv
import math
import sys

class PennsylvaniaLoader(ContestRegression):
  def _GetDelimiter(self):
    return '\t'

  def _IsValidRow(self, row):
    return len(row) == 9

  def _IsValidParty(self, row):
    return row[4][0:3] == self._party

  def _GetVotes(self, row):
    if not row[5] or int(row[5]) < self._GetMinVotes():
      return None
    return math.log(int(row[5]))

  def _GetPrecinctName(self, row):
    precinct = '%s:%s' % (row[2], row[3])
    return precinct.replace(' ', '_')

  def _GetContestName(self, row):
    return row[1]

  def _GetCountyName(self, row):
    return [0]


def main(argv=None):
  if argv is None:
    argv = sys.argv
  if len(argv) != 5 and len(argv) != 6:
    print('Usage: %s <datafile> <party> <indep_contest> <dep_contest> [<county>]' %(argv[0]))
    return 1
  county = None
  if len(argv) == 6:
    county = argv[5]
  pa = PennsylvaniaLoader(argv[2], argv[3], argv[4], county)
  pa.Load(argv[1])
  pa.Regress()
  return 0

if __name__ == '__main__':
  sys.exit(main())
