from odoo import models
import requests
import logging

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):

    _inherit = "account.move"



    def action_post(self):
        # Call the original post method (invoice validation)
        res = super(AccountMove, self).action_post()

        for move in self:
            if move.state == 'posted' and move.move_type in ['out_invoice', 'out_refund']:  # Only customer invoices/credit notes
                try:
                    self._send_invoice_to_api(move)
                except Exception as e:
                    print("Failed to send invoice %s to API: %s", move.name, str(e))
            else:
                print('notntonrnijrdojgdogdpppppppppppppppppppppppppppppppppp')

        return res

    def _send_invoice_to_api(self, move):
        """Prepare and send invoice data to external API"""
        url = "https://example.com/api/invoices"  # Replace with your API endpoint
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer YOUR_API_KEY"  # Replace with actual auth
        }
        payload = {
            "company_name": move.company_id.name ,
            "company_tax_number": move.company_id.vat,
            "invoice_number": move.name,
            "partner": move.partner_id.name,
            "date": str(move.invoice_date),
            "amount_total": move.amount_total,
            "currency": move.currency_id.name,
            "lines": [
                {
                    "product": line.product_id.name,
                    "quantity": line.quantity,
                    "price_unit": line.price_unit,
                    "subtotal": line.price_subtotal,
                }
                for line in move.invoice_line_ids
            ]
        }
        print(payload)

        response = requests.post(url, json=payload, headers=headers, timeout=30)

        if response.status_code not in [200, 201]:
            raise ValueError(f"API error {response.status_code}: {response.text}")

        _logger.info("Invoice %s successfully sent to API", move.name)