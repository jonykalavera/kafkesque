MANDATORY_WEBHOOK_PARAMS = ['topic', 'webhook']
import validators

def validate_webhook_request(params):
    for p in MANDATORY_WEBHOOK_PARAMS:
        if p not in params:
            raise KeyError(f'"{p}" must be present in the webhook connector params')
    if not validators.url(params['webhook']):
        raise ValueError(f'Malformed webhook URL: {params["webhook"]}')
