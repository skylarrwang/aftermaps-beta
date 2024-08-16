"""
blockage_credibility.py

This is a class that defines a procedure for calculating the probability that a road is blocked.
It synthesizes individual user report credibilities and reported severity ratings into an overall
assessment of road blockage probability.
"""
import numpy as np
from sklearn.mixture import GaussianMixture  # Non-Bayesian Gaussian mixture model


class BlockageCredibility:
    """
    A class to define a procedure for calculating the
      probability that a road is blocked. It takes the
    weighted average of user report credibilities and
      reported severity ratings to synthesize an overall
    assessment of road blockage probability.

    Attributes
    ----------
    report_credibilities (ndarray): Array of credibility values for user reports.
    severity_ratings (ndarray): Array of severity ratings for the blockages.

    Methods
    ----------
    calculate_blockage_probability(): Calculate the probability
    that a road is blocked based on user report
    credibilities and reported severity ratings.
    """
    def __init__(self, report_credibilities, severity_ratings, n_clusters=2):
        """
        Initialize the model with the accuracy of reports and the severity ratings.

        Parameters
        ----------
        report_credibilities (ndarray): Array of credibility values for user reports.
        severity_ratings (ndarray): Array of severity ratings for the blockages.

        Returns
        ----------
        None.
        """
        self.report_credibilities = report_credibilities
        self.severity_ratings = severity_ratings
        self.n_clusters = n_clusters

    def calculate_blockage_probability(self, n_clusters=2):
        """
        Calculate the probability that a road is 
        blocked based on user report credibilities and
        reported severity ratings.

        Parameters
        ----------
        None.

        Returns
        ----------
        blockage_probability (float): The probability that a road is blocked.
        """
        # Step 1: Weigh the severity ratings by the credibility of the reports
        weighted_severities = self.report_credibilities * self.severity_ratings
        gmm = GaussianMixture(n_components=n_clusters, random_state=42)
        gmm.fit(weighted_severities.reshape(-1, 1))

        # Step 4: Derive blockage probability for this road
        higher_severity_component = np.argmax(gmm.means_)
        blockage_probability = gmm.weights_[higher_severity_component]

        return blockage_probability
if __name__ == "__main__":
    raise Exception("Please import this file as a module instead of running it directly.")
