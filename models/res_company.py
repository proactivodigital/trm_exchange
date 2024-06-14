from odoo import api, fields, models
import requests
import logging

_logger = logging.getLogger(__name__)

class ResCompany(models.Model):
    _inherit = 'res.company'

    currency_provider = fields.Selection(
        selection_add=[('custom_exchange', 'Custom Exchange')],
    )

    @api.model
    def _update_currency_rates(self):
        for company in self.search([]):
            if company.currency_provider != 'custom_exchange':
                continue

            url = f"https://www.datos.gov.co/resource/32sa-8pi3.json"
            
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise error for bad responses (4xx or 5xx)
                data = response.json()
                
                if not data:
                    _logger.error(f"No data received from API for company {company.name}")
                    continue
                
                # Extract the 'valor' field from the first element in the JSON
                trm = float(data[0]['valor'])

                # Get the USD currency
                usd_currency = self.env['res.currency'].search([('name', '=', 'USD'), ('active', '=', True)], limit=1)
                
                if not usd_currency:
                    _logger.error(f"USD currency not found or not active for company {company.name}")
                    continue

                # Calculate the rate (USD to COP)
                rate = 1.0 / trm

                # Check for existing rate for today
                existing_rate = self.env['res.currency.rate'].search([
                    ('currency_id', '=', usd_currency.id),
                    ('name', '=', fields.Date.today()),
                    ('company_id', '=', company.id)
                ])

                if existing_rate:
                    existing_rate.write({'rate': rate})
                else:
                    self.env['res.currency.rate'].create({
                        'currency_id': usd_currency.id,
                        'rate': rate,
                        'name': fields.Date.today(),
                        'company_id': company.id,
                    })

                _logger.info(f"Currency rates updated successfully for company {company.name}")

            except requests.RequestException as e:
                _logger.error(f"Failed to fetch currency rates for company {company.name}: {str(e)}")
            except Exception as e:
                _logger.error(f"An error occurred while updating currency rates for company {company.name}: {str(e)}")

