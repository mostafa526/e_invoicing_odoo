from odoo import models
import requests
import logging
from datetime import datetime
from odoo import fields



_logger = logging.getLogger(__name__)


class AccountMove(models.Model):

    _inherit = "account.move"



    def action_post(self):
        # Call the original post method (invoice validation)
        res = super(AccountMove, self).action_post()

        for move in self:
            if move.state == 'posted' and move.move_type in ['out_invoice', 'out_refund']:  # Only customer invoices/credit notes
                self._send_invoice_to_api(move)

            else:
                print('notntonrnijrdojgdogdpppppppppppppppppppppppppppppppppp')

        return res

    def _send_invoice_to_api(self, move):
        """Prepare and send invoice data to external API"""


        url = (
            "https://ap-local-server.orchida-einvoice.com/dashboard/api/sales/invoices/AddSalesInvoice"
            "?fromDate=2023-01-01&toDate=2026-12-31&format=uaeDefault"
        )


        token ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiIzIiwiZW1haWwiOiJuYWJpbC5tb2todGFyQG9yY2hpZGEtc29mdC5jb20iLCJ1bmlxdWVfbmFtZSI6Im5hYmlsIiwianRpIjoiNmU4YTc4Y2EtZDE0Ny00NDNiLWE2MWItM2JmZDFjNzVlNWYwIiwiaWF0IjoxNzYxMzE2NTk0LCJDb21wYW55SWQiOiI0IiwiUm9sZSI6IlVzZXIiLCJuYmYiOjE3NjEzMTY1OTQsImV4cCI6MTc2MTM0NTM5NCwiaXNzIjoiT3JjaGlkYS1UYXggZGFzaGJvYXJkIiwiYXVkIjoiT3JjaGlkYS1UYXggaG9ub3JhYmxlIGNsaWVudHMifQ.XVuBij1ExL_FxUmXrgYGL8TpoSwEawDLzwx0IVRkrmw"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }


        payload = {
            "internalCode": "testb2005" ,
            "type": "I",
            "dateTimeIssued": move.invoice_date and move.invoice_date.strftime("%Y-%m-%dT%H:%M") or datetime.now().strftime("%Y-%m-%dT%H:%M"),
            "buyerId": "1",
            "currency": move.currency_id.name ,
            "currRate": move.currency_id._get_conversion_rate(
                move.currency_id, move.company_id.currency_id, move.company_id, move.invoice_date or fields.Date.today()
             ),
            "note": move.narration or "",
            "refCode": "",
            "total": move.amount_total,
            "prepaid": "0",
            "OrderReferenceID": "",
            "SalesOrderID": "",
            "rounding": 0,
            "allowances": [
                {
                    "Indicator": "false",
                    "ReasonCode": "",
                    "Reason": "",
                    "Amount": "0",
                    "TaxCatID": "",
                    "TaxPercent": "0",
                    "ExemptionCode": "",
                    "ExemptionReason": "",
                }
            ],
            "PaymentMeans": [
                {
                    "Code": "10"  # Cash
                }
            ],
            "lines": [],
        }


        for line in move.invoice_line_ids:
            payload["lines"].append({
                "Description": line.name or line.product_id.display_name or "",
                "Name": line.product_id.name or "Unknown",
                "itemID": str(line.product_id.id or 0),
                "Note": "",
                "itemDiscountAmount": 0,
                "Quantity": line.quantity,
                "UnitValue": line.price_unit,
                "UnitCode": "",  # Default unit
                "lineVATRate": 0,
                "lineVATSubtype": "",
                "lineVATReason": "",
                "lineVATReasonDesc": "",
            })





        response = requests.post(url, json=payload, headers=headers, timeout=30)
        print(response)
        if response.status_code not in [200, 201]:
            raise ValueError(f"API error {response.status_code}: {response.text}")
