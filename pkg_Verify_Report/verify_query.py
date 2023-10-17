from pkg_SQL.database import SQL

class verify_query:
    """
    For verification report, execute query to MS-SQL

    """
    def __init__(self, sorted_param, selected_measSSId, report_term, selected_probeId):
        self.sorted_param = sorted_param,
        self.selected_measSSId = selected_measSSId,
        self.report_term = report_term,
        self.selected_probeId = selected_probeId

