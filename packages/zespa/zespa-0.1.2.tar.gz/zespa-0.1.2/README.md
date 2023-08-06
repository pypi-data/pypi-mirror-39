# ZenHub-SP-Aggregator
Aggregate issue StoryPoint(Estimate) by labels and time.

Calculate sum of estimate point in specific duration for the repository.

## Install

```
$ pip install zespa
```

# Usage

for initial configuration, you need to get GitHub API Token and ZenHub API Token.

```
$ zespa configure
$ zespa aggregate 2018/10/01 2018/10/31  --labels Bug Refactoring  # all issues / issues labeled `Bug` or `Refactoring`
+--------------------+
| Bug or Refactoring |
+--------------------+
|         110        |
+--------------------+
+------------------------+
| Not Bug or Refactoring |
+------------------------+
|          262           |
+------------------------+

(and export CSV file which shows individual issue title and estimate point.)
```
