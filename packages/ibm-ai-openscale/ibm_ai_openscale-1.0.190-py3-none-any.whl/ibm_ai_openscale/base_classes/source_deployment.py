class SourceDeployment:
    def __init__(self, guid, url, name, deployment_type, created, scoring_endpoint=None, rn=None):
        self.guid = guid
        self.url = url
        self.name = name
        self.deployment_type = deployment_type
        self.created = created
        self.scoring_endpoint = scoring_endpoint
        self.rn = rn

    def _to_json(self):
        return {
            "deployment_id": self.guid,
            "url": self.url,
            "name": self.name,
            "deployment_type": self.deployment_type,
            "created_at": self.created,
            'scoring_endpoint': self.scoring_endpoint if self.scoring_endpoint is not None else {},
            "deployment_rn": self.rn if self.rn is not None else ''
        }
