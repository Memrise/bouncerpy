import requests


class Experiment(object):
    def __init__(self, name, alternatives):
        self.alternatives = alternatives
        self.name = name


class Feature(object):
    def __init__(self, name, enabled):
        self.name = name
        self.enabled = float(enabled)


class Group(object):
    def __init__(self, name, members):
        self.name = name
        self.members = members


class Bouncer(object):
    def __init__(self, service_url='http://localhost:5000'):
        self.service_url = service_url

    def configured_experiments(self):
        """
        Retrieve configured experiments
        :return: List of Experiment objects
        """
        resp = requests.get(self.service_url + '/experiments/')
        return [Experiment(exp['name'], exp['alternatives']) for exp in resp.json()]

    def configured_features(self):
        """
        Retrieve configured features
        :return: List of Feature objects
        """
        resp = requests.get(self.service_url + '/features/')
        return [Feature(f['name'], f['enabled']) for f in resp.json()]

    def configured_groups(self):
        """
        Retrieve configured groups
        :return: List of Group objects
        """
        resp = requests.get(self.service_url + '/groups/')
        return [Group(g['name'], g['uids']) for g in resp.json()]

    def stats(self):
        """
        Get stats from the AB test service
        :return: dictionary of stats
        """
        return requests.get(self.service_url + '/stats/').json()

    def participate(self, uid, features=None, experiments=None):
        """
        Participate in an experiment.
        :param features: dict of feature_name: status
        :param experiments: dict of experiment_name: [list, of, alts]
        :return:
        """
        if not uid:
            raise ValueError("Missing parameter uid")

        resp = requests.post(self.service_url + '/participate/', json={
            'uid': uid,
            'features': features or {},
            'experiments': experiments or {}
        })
        if resp.status_code != 200:
            raise ValueError(u"Bad request: " + resp.content)

        data = resp.json()
        return data['features'], data['experiments']
