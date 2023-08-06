#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
File:   __init__.py
Author: Lijiacai (v_lijiacai@baidu.com)
Date: 2018-12-17
Description:
    This package implements the conversion between CSV files and Excel files.
    dictorder provide ordered Dictionaries and return a Dictionaries too.

    e.g1:
        from DDT.CSV_EXCEL import DataToCsv
        dtc = DataToCsv("test")
        headers = ["姓名", "年龄", "爱好"]
        data = [u"xiaoming", "12", "basketball"]
        dtc.write("test.csv", data, headers=headers, mode="ab+")
        dtc.write("test.csv", data, headers=headers)
        dtc.nullline("test.csv", nulldata=[""])
        dtc.write("test.csv", data, headers=headers)
    e.g2:
        from DDT.CSV_EXCEL import CsvToExcel
        cte = CsvToExcel(dir_path="excel_test")
        cte.convertToExcel("test", "test/test.csv", merge_cells=False, drop_colume=[u"爱好"])
    e.g3:
        from DDT.CSV_EXCEL import CsvMergeSheet
        cms = CsvMergeSheet("csv_sheet")
        cms.merge_sheet("test/test.csv", "1")
    e.g4:
        from DDT.CSV_EXCEL import ExcelToCsv
        etc = ExcelToCsv("etc")
        etc.convertToCsv("csv_sheet/test.xlsx", sheet_name="11", csvfile="test.csv")
    e.g5:
        from DDT.dictorder import sorted_dict
        data = {"a":"11", "c":"123", "b": "321"}
        new_data = sorted_dict(data)
"""
