from odoo import api, fields, models
import requests
import logging

# Initialize the logger to capture logs
_logger = logging.getLogger(__name__)

class ResCompany(models.Model):
    _inherit = 'res.company'

    # Add a custom field to select the currency provider for the company
    currency_provider = fields.Selection(
        selection_add=[('custom_exchange', 'Custom Exchange')],  # Adds 'Custom Exchange' option to the currency provider field
    )

    @api.model
    def _update_currency_rates(self):
        """
        This method is used to fetch and update currency rates from a custom exchange API.
        It checks if the company's currency provider is set to 'custom_exchange' and
        updates the exchange rate for USD (from the custom API) into Odoo's currency rates.

        The method performs the following tasks:
        1. Fetches data from an external API (custom exchange rate source).
        2. Extracts the exchange rate (TRM).
        3. Finds the USD currency and calculates the exchange rate.
        4. Updates or creates the corresponding currency rate for USD.
        5. Handles errors and logs relevant information.
        """

        # Loop through all companies in the system
        for company in self.search([]):
            # Skip companies that do not use the 'custom_exchange' provider
            if company.currency_provider != 'custom_exchange':
                continue

            # API URL to fetch the custom exchange rates (TRM)
            url = f"https://www.datos.gov.co/resource/32sa-8pi3.json"
            
            try:
                # Fetch data from the custom exchange rates API
                response = requests.get(url)
                response.raise_for_status()  # Raise error for bad responses (4xx or 5xx)
                data = response.json()
                
                # If no data is returned, log the error and move to the next company
                if not data:
                    _logger.error(f"No data received from API for company {company.name}")
                    continue
                
                # Extract the 'valor' field from the JSON response (TRM value)
                trm = float(data[0]['valor'])

                # Find the USD currency in Odoo (assumes USD is available)
                usd_currency = self.env['res.currency'].search([('name', '=', 'USD'), ('active', '=', True)], limit=1)
                
                # If USD currency is not found or not active, log an error and move to the next company
                if not usd_currency:
                    _logger.error(f"USD currency not found or not active for company {company.name}")
                    continue

                # Calculate the exchange rate (1 USD to COP), assuming TRM is USD to COP rate
                rate = 1.0 / trm

                # Check if the exchange rate for USD to COP already exists for today
                existing_rate = self.env['res.currency.rate'].search([
                    ('currency_id', '=', usd_currency.id),
                    ('name', '=', fields.Date.today()),  # Today's date
                    ('company_id', '=', company.id)
                ])

                if existing_rate:
                    # If an existing rate is found, update the rate
                    existing_rate.write({'rate': rate})
                else:
                    # If no existing rate is found, create a new record for the rate
                    self.env['res.currency.rate'].create({
                        'currency_id': usd_currency.id,
                        'rate': rate,
                        'name': fields.Date.today(),
                        'company_id': company.id,
                    })

                # Log the success message indicating that the rates were updated
                _logger.info(f"Currency rates updated successfully for company {company.name}")

            except requests.RequestException as e:
                # Handle errors from the API request
                _logger.error(f"Failed to fetch currency rates for company {company.name}: {str(e)}")
            except Exception as e:
                # Handle other errors (e.g., parsing errors or database errors)
                _logger.error(f"An error occurred while updating currency rates for company {company.name}: {str(e)}")
