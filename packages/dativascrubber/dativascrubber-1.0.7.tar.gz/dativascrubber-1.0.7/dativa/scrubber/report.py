# (c) 2012-2018 Dativa, all rights reserved
# -----------------------------------------
#  This code is licensed under MIT license (see license.txt for details)

import datetime
import pandas as pd


class ReportEntry:
    """
    An individual report entry.

    Parameters
    ----------
    rule: the name of the rule that produced this entry
    field: the field being processed when the entry was produced
    df: the DataFrame containing the invalid records
    category: the type of entry, one of:
        HistoryCategory.IGNORED - the records were not altered
        HistoryCategory.REPLACED - the records were replaced with other values
        HistoryCategory.REMOVED - the records have been removed
        HistoryCategory.MODIFIED - the records have been modified
        HistoryCategory.INSERTED - new records have been inserted
    description: a textual description of the changes made (if any)
    """

    date = ""
    field = ""
    df = None
    category = ""
    description = ""
    number_records = ""

    def __init__(self, rule, field, df, category, description):
        self.date = datetime.datetime.now()
        self.field = field
        self.df = pd.DataFrame(df)
        self.number_records = df.shape[0]
        self.category = category
        self.description = description
        self.rule = rule

    def __str__(self):
        return "{0}, Field {1}({2}): #{3} {4}/|{5}".format(self.date,
                                                           self.field,
                                                           self.rule,
                                                           self.number_records,
                                                           self.category,
                                                           self.description)

    def get_log_dict(self):
        """
        Returns a dict containing the log entries
        """
        return {"date": self.date,
                "field": self.field,
                "rule": self.rule,
                "number_records": self.number_records,
                "category": self.category,
                "description": self.description}

    def get_records(self):
        """
        returns the DataFrame containing the values
        """
        return self.df


class DefaultReportWriter:
    """
    A default implementation of the ReportWriter that stores ReportEntries
    and returns them.
    """

    report = []

    def reset_report(self):
        self.report = []

    def log_history(self,
                    rule,
                    field,
                    df,
                    category,
                    description
                    ):
        """
        Logs a report entry
        """

        if isinstance(df, pd.Series):
            df = df.to_frame()

        self.report.append(ReportEntry(rule=rule,
                                       field=field,
                                       df=df,
                                       category=category,
                                       description=description
                                       ))

        return

    def get_report(self):
        """
        Returns an array of all ReportEntries created
        """
        return self.report
