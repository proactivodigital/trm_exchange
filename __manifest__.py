{
    "name": "Automatic Currency Rate",  # Name of the module
    "version": "1.0",  # Version of the module
    'summary': 'Automatic currency rate updates from Custom Exchange Rates API',  # Brief description of the module
    'description': 'Fetch and update currency rates from Custom Exchange Rates API.',  # Detailed description
    "author": "Proactivo Digital",  # Author of the module
    "support": "cristian.berrio@proactivo.digital",  # Support contact email
    "license": "LGPL-3",  # License under which the module is released
    "category": "Accounting",  # Category of the module (Accounting related)
    "depends": ['base', 'account'],  # Dependencies required for the module to function properly
    "data": [
        'data/ir_cron_data.xml',  # Data file containing cron job configurations for fetching currency rates
    ],
    "auto_install": False,  # Whether the module should be automatically installed with its dependencies (False means no)
    "application": False,  # Indicates whether the module is an application (False means it is an extension)
}
