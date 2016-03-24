import logging

import requests


logger = logging.getLogger(__name__)


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

    def participate(self, context, features=None, experiments=None, timeout=3, fallback=True):
        """
        Participate in an experiment.
        :param context: dict including uid and additional context
        :param features: dict of feature_name: status
        :param experiments: dict of experiment_name: [list, of, alts]
        :param timeout: timeout in seconds
        :param fallback: pick locally if service unavailable
        :return:
        """
        if 'uid' not in context:
            raise ValueError("Missing parameter uid in context")

        try:
            resp = requests.post(self.service_url + '/participate/', json={
                'context': context,
                'features': features or {},
                'experiments': experiments or {}
            }, timeout=timeout)

        except requests.Timeout as e:
            if fallback:
                logger.error('Timed out after {} seconds attempting to reach: {}'.format(
                    timeout, self.service_url), exc_info=True)
                return self._offline_response(features, experiments)
            else:
                raise e

        except requests.ConnectionError:
            if fallback:
                logger.error('Connection error attempting to reach: {}'.format(
                    self.service_url), exc_info=True)
                return self._offline_response(features, experiments)
            else:
                raise e

        if resp.status_code != 200:
            raise ValueError(u"Bad request: " + resp.content)

        data = resp.json()
        return data['features'], data['experiments']

    def _offline_response(self, requested_features, requested_experiments):
        """
        Called when the bouncer service can't be reached picks default values
            from args if available.
        :param requested_features:
        :param requested_experiments:
        :return: features, experiments
        """
        features, experiments = {}, {}

        if requested_features:
            for feature, status in requested_features.iteritems():
                features[feature] = status == 1

        if requested_experiments:
            for experiment, alternatives in requested_experiments.iteritems():
                experiments[experiment] = alternatives[0]

        return features, experiments
