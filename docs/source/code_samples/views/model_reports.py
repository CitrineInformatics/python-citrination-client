from citrination_client.views.client import DataViewsClient
from os import environ

# Note: for the purposes of this example, environ["CITRINATION_SITE"] is
#       https://citrination.com
client = DataViewsClient(environ["CITRINATION_API_KEY"], environ["CITRINATION_SITE"])
reports = client.get_model_reports(524)

print([str(report) for report in reports])
# ["<ModelReport model_name='Crystallinity'>",
#  "<ModelReport model_name='Color'>",
#  "<ModelReport model_name='Band gap'>"]

# Crystallinity is a Categorical output
print(reports[0].performance)
# {'ndme_f1': 0.7513840971831497}

print(reports[0].model_settings)
# {'Algorithm': 'Ensemble of non-linear estimators',
#  'Maximum tree depth': 30,
#  'Minimum samples per leaf': 1,
#  'Number of cross-validation folds': 3,
#  'Number of estimators': 194}

print(reports[0].feature_importances)
# [{'name': 'mean of Non-dimensional work function for Chemical formula',
#   'value': 0.016694057309452427},
#  {'name': 'mean of DFT volume ratio for Chemical formula',
#   'value': 0.02425121569638139},
#  {'name': 'mean of Non-dimensional liquid range for Chemical formula',
#   'value': 0.024088896494558795},
#  {'name': 'mean of Radius of d orbitals for Chemical formula',
#   'value': 0.018493567944483043},
#  ...
# ]

# Band Gap is a Real output, hence why it may have different keys
print(reports[2].performance)
# {'ndme': 0.35374524040321054,
#  'ndme_stderr': 0.008224021869691423,
#  'rmse': 0.8023624551013153,
#  'rmse_stderr': 0.018653668302790923,
#  'uc_fraction': 0.5793304221251819,
#  'uc_rmsse': 1.9191506842755264}

print(reports[2].model_settings)
# {'Algorithm': 'Ensemble of non-linear estimators',
#  'Leaf model': 'Mean',
#  'Maximum tree depth': 30,
#  'Minimum samples per leaf': 1,
#  'Number of cross-validation folds': 3,
#  'Number of estimators': 148,
#  'Uses jackknife method of uncertainty estimation': True}

print(reports[2].feature_importances)
# [{'name': 'mean of Non-dimensional work function for Chemical formula',
#   'value': 0.04867717383587202},
#  {'name': 'mean of DFT volume ratio for Chemical formula',
#   'value': 0.008961689534579438},
#  {'name': 'mean of Non-dimensional liquid range for Chemical formula',
#   'value': 0.006946688158984557},
#  ...
# ]
