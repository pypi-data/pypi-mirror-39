from __future__ import unicode_literals

from epsilon.util import (epsilon_authenticate,
                          epsilon_get_transaction_id,
                          epsilon_add_profile,
                          epsilon_add_promotion,
                          epsilon_add_survey,
                          epsilon_on,
                          epsilon_validate_data)


class Epsilon:
    @staticmethod
    def addProfile(profile, add_survey=False):
        epsilon_on()
        epsilon_validate_data(profile)

        auth_response = epsilon_authenticate()
        access_token = auth_response.get('access_token')

        transaction_id = epsilon_get_transaction_id()

        profile_id = epsilon_add_profile(access_token,
                                         transaction_id,
                                         profile)

        promotion_id = epsilon_add_promotion(access_token,
                                             transaction_id,
                                             profile_id,
                                             profile)
        if add_survey is True:
            epsilon_add_survey(access_token,
                               transaction_id,
                               profile_id)

        return promotion_id
