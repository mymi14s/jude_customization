# import frappe
#
#
# @frappe.whitelist()
# def compute_salary_slip_paye_on_form(name):
#     doc = frappe.get_doc("Salary Slip", name)
#     # frappe.msgprint(_(event))
#     # for i in doc.earnings:
#     #     print(i.name, i.salary_component, i.abbr)
#     annual_gross_pay = doc.gross_pay * 12
#     annual_pension = sum([i.amount for i in doc.earnings if i.salary_component.upper() in ["BASIC SALARY", "HOUSING ALLOWANCE", 'TRANSPORT ALLOWANCE']]) * 12
#     annual_pension_08 = annual_pension * 0.08
#     if((annual_gross_pay * 0.01) > 200000):consolidated_relief_allowance=(annual_gross_pay * 0.2) + (annual_gross_pay * 0.01)
#     else:consolidated_relief_allowance=(annual_gross_pay * 0.2 + (200000))
#
#     # other reliefs
#     other_reliefs = sum([i.amount for i in doc.earnings if i.abbr.upper() in ["NHF", "NHIS"]]) * 12
#     non_taxable_annual = consolidated_relief_allowance + annual_pension_08 + other_reliefs
#     taxable_annual = annual_gross_pay - non_taxable_annual
#
#     def tax_band_calculator(taxable):
#         band_list = [
#             {'amount':300000, 'per':0.07},
#             {'amount':300000, 'per':0.11},
#             {'amount':500000, 'per':0.15},
#             {'amount':500000, 'per':0.19},
#             {'amount':1600000, 'per':0.21},
#             # {'amount':3200000, 'per':0.0},
#         ]
#         tax_to_pay = 0
#         if(taxable>3200000):tax_to_pay=((taxable-3200000)*0.24) + 560000
#         else:
#             taxable_copy = taxable
#             for i, val in enumerate(band_list):
#                 if((taxable_copy<val['amount']) and taxable_copy>0):
#                     tax_to_pay += taxable_copy * val['per']
#                     break
#                 elif(taxable_copy<0):
#                     break
#                 else:
#                     taxable_copy -= val['amount']
#                     tax_to_pay += val['amount'] * val['per']
#                     # if(taxable_copy<0):
#                     #     break
#         return tax_to_pay
#
#     # get taxable_annual
#     tax_to_pay_annually = tax_band_calculator(taxable_annual)
#     if((tax_to_pay_annually/12)<(0.01*doc.gross_pay)):tax_to_pay_monthly=0.01*doc.gross_pay
#     else:tax_to_pay_monthly = tax_to_pay_annually/12
#
#     return ({
#         'response_status':200,
#         'tax_to_pay_monthly':tax_to_pay_monthly,
#         'total_in_words':frappe.utils.money_in_words(doc.rounded_total-tax_to_pay_monthly),
#         'doc': doc
#         })
#
#     # create new PAYE
#     # check PAYE
#     # checker = False
#     # doc_total_deductions = 0
#     # for i in doc.deductions:
#     #     if i.salary_component == "PAYE Tax":
#     #         checker = True
#     #         i.amount = tax_to_pay_monthly
#     #         i.default_amount = tax_to_pay_monthly
#     #         # doc.save()
#     # if checker:
#     #     doc.total_deduction = ((annual_pension/12)/12) + tax_to_pay_monthly
#     #     doc.net_pay = doc.gross_pay - doc.total_deduction
#     #     doc.rounded_total = round(doc.net_pay, 2)
#     #     doc.total_in_words = frappe.utils.money_in_words(doc.rounded_total)
#     #
#     # if not checker:
#     #     newdoc = frappe.new_doc("Salary Detail")
#     #     newdoc.parent = doc.name
#     #     newdoc.parenttype = 'Salary Slip'
#     #     newdoc.parentfield = 'deductions'
#     #     newdoc.salary_component = 'PAYE Tax'
#     #     newdoc.abbr = 'PAYE'
#     #     newdoc.amount = tax_to_pay_monthly
#     #     newdoc.insert(ignore_permissions=True)
#     #     # print(newdoc.amount)
#     #     doc.reload()
