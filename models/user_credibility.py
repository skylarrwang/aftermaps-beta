"""
user_credibility.py

This is a class that defines a Bayesian model for estimating the credibility of reports
of blockages in a city after a disaster. The model takes into account the accuracy of
the reports, the distance from the user to the blockage, and other features such as
the location, type, and degree of the blockage.

Warning: Please use the version in the Jupyter Notebook credibility_model_testing.ipynb
until the code is fully tested and validated.
"""
import pymc as pm  # Bayesian modeling library


class UserCredibility:
    """
    A class to define a Bayesian model for estimating the credibility of reports of blockages
    in a city after a disaster. The model takes into account the accuracy of the reports, the
    distance from the user to the blockage, and other features such as the location, type, and
    degree of the blockage.

    Attributes
    ----------
    reports_accuracy (ndarray): Array of 0s and 1s indicating the accuracy of the reports.
    distance (ndarray): Array of distances from the user to the blockage.
    location_data (ndarray): Array of location data for the blockages.
    type_data (ndarray): Array of blockage type data.
    degree_data (ndarray): Array of blockage degree data.

    Methods
    ----------
    build_model(): Builds the Bayesian model and returns the trace of the model.
    """
    def __init__(self, reports_accuracy, distances):
        """
        Initialize the UserCredibility model with the accuracy of reports and the distance
        from the user to the blockage.

        Parameters
        ----------
        reports_accuracy (ndarray): Array of 0s and 1s indicating the accuracy of the reports.
        distance (ndarray): Array of distances from the user to the blockage.

        Returns
        ----------
        None.
        """
        self.reports_accuracy = reports_accuracy
        self.distances = distances

    def build_model(self, num_samples=1000, prior_credibility=0.5):
        """
        Constructs the Bayesian model for estimating the credibility of reports of blockages
        in a city after a disaster. The model takes into account the accuracy of the reports,
        the distance from the user to the blockage, and other features such as the location,
        type, and degree of the blockage.

        Parameters
        ----------
        num_samples (int): Number of samples to draw from the model.
        prior_credibility (float): Initial credibility of the reports.

        Returns
        ----------
        trace (ndarray): Array of samples from the model.
        """
        with pm.Model() as model:
            # Prior for user credibility
            credibility = pm.Beta('credibility', alpha=2 * prior_credibility,
                                  beta=(1 - prior_credibility) * 2)

            # Modeling the impact of distance
            distance_effect = pm.Normal('distance_effect', mu=0, sigma=1)
            adjusted_credibility = pm.Deterministic('adjusted_credibility',
                                                    pm.math.sigmoid(credibility - distance_effect * self.distances))

            # Likelihood of observed data
            likelihood = pm.Bernoulli('likelihood', p=adjusted_credibility, observed=self.reports_accuracy)

            # Sampling from the model
            trace = pm.sample(num_samples, return_inferencedata=False)

        return trace
if __name__ == "__main__":
    raise Exception("Please import this file as a module instead of running it directly.")
