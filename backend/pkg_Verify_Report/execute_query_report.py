from pkg_SQL.database import SQL

class Execute_Query_Report:
    """
    For verification report, execute query to MS-SQL

    """
    def __init__(self, sorted_param, selected_measSSId, report_term, selected_probeId):
        self.sorted_param = sorted_param
        self.selected_measSSId = selected_measSSId
        self.report_term = report_term
        self.selected_probeId = selected_probeId


    def parsing(self):

        param = ''.join(map(str, self.sorted_param))
        measSSId = ''.join(map(str, self.selected_measSSId))
        term = ''.join(map(str, self.report_term))
        probeId = self.selected_probeId

        connect = SQL(command=8, sorted_param=param, selected_measSSId=measSSId, report_term=term, selected_probeId=probeId)
        self.df = connect.sql_get()

        return self.df
