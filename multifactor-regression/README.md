Quick Usage
===========

The program attempts to perform a multivariate linear regression in order to
predict the number of votes a candidate received based on several factors. In
most cases those factors will be:

1. **00INT** - The intercept (i.e., a constant value);
2. **PCTCOLLEGE** - The percent of adults with a college degree;
3. **PCTWHITE** - The percent of adults who are white; and
4. **RES2012** - The results of the 2012 election.

Best practices are to use the log of the number of votes, both for input and
predicted values, since jurisdiction (i.e., county) sizes aren't normally
distributed. Here's the sample output using some data that's in the repo.

```
bash:~$ python ./nc_regress.py D data/NC2016_P.tsv
                            OLS Regression Results
==============================================================================
Dep. Variable:             log(Votes)   R-squared:                       0.997
Model:                            OLS   Adj. R-squared:                  0.997
Method:                 Least Squares   F-statistic:                 1.249e+04
Date:                Wed, 07 Dec 2016   Prob (F-statistic):          2.86e-124
Time:                        18:22:12   Log-Likelihood:                 139.56
No. Observations:                 100   AIC:                            -271.1
Df Residuals:                      96   BIC:                            -260.7
Df Model:                           3
Covariance Type:            nonrobust
==============================================================================
                 coef    std err          t      P>|t|      [99.0% Conf. Int.]
------------------------------------------------------------------------------
00INT         -0.3405      0.076     -4.478      0.000        -0.540    -0.141
PCTCOLLEGE     0.6967      0.098      7.136      0.000         0.440     0.953
PCTWHITE      -0.1078      0.041     -2.657      0.009        -0.214    -0.001
RES2012        1.0214      0.008    134.117      0.000         1.001     1.041
==============================================================================
Omnibus:                        7.481   Durbin-Watson:                   1.827
Prob(Omnibus):                  0.024   Jarque-Bera (JB):                7.705
Skew:                          -0.481   Prob(JB):                       0.0212
Kurtosis:                       3.961   Cond. No.                         174.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
ALAMANCE            	  26924	  29817	 0.1075	   2893
[...]
```

This is a bit dense, but there are a few things to examine. The first is whether
or not the model is a good fit for the data. Check the R-squared value at the
top-right; the closer this is to 1.0, the better. A value of 0.997 is
*extremely* good. The next set of values to check are the confidence intervals
for each factor, or the last two values on the rows in the middle block. If both
ends of the confidence interval have the same sign (i.e., positive or negative)
then we can be almost positive that that factor is correlated with a non-zero
effect on the vote totals. Just remember that [correlation is not
necessarily causation](https://xkcd.com/552/).

In this sample output, each factor is significant at p<0.01. We're attempting to
predict the number of votes the Democratic candidate received, so it's not
surprising that increased levels of college education boost support, while
increases in the share of the population that is white (i.e., fewer minorities)
correlates with less support for Clinton.

After the summary are per-county statistics. The columns are

1. County name;
2. Predicted number of votes, per the model;
3. Actual number of votes;
4. The percent error; and 
5. The magnitude of the error.

For both (4) and (5), a positive number indicates that the candidate
overperformed their prediction, while a negative number indicates that the
candidate underperformed their prediction.

Custom Parsers
==============
It's possible to build a new parser for a state. You simply have to:

1. Create a new subclass of FactorRegression;
2. Override the following functions:
  * \_GetCollegePercent(self, row)
  * \_GetColumns(self)
  * \_GetJurisdiction(self, row)
  * \_GetVotes(self, row, year, party)
  * \_GetWhitePercent(self, row)
  * \_IsValidRow(self, row)
  * main(argv)
3. Collect the data in a CSV or TSV.

There are examples for NC and WI.
