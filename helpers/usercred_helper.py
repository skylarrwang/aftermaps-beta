"""helper for user credability"""
import models.user_credibility as uc
import numpy as np

def convert_nplist(rows):
    '''Converts SQL rows into np.array readable form'''
    distance = []
    ground_truths = []
    for row in rows:
        distance.append(row[0])
        ground_truths.append(row[1])
    return distance, ground_truths


def init_uc(uf_distance, uf_ground_truths):
    """helps with report"""
    # Generate some example data for one user (five reports)
    reports_accuracy = np.array(uf_ground_truths)  # 1 for True, 0 for False
    distances = np.array(uf_distance)  # Distance in km
    distances = (distances - np.mean(distances)) / np.std(distances)

    # Instantiate the model for one user
    model = uc.UserCredibility(reports_accuracy=reports_accuracy,
                            distances=distances)

    # Run the model and get the trace
    trace = model.build_model(num_samples=1000, prior_credibility=0.5)

    # Posterior analysis to get user credibility
    credibility_samples = trace['credibility']
    # Take samples from the posterior

    # Return the mean of the samples as the estimated credibility
    return round(np.mean(credibility_samples), 2)

def update_uc(uf_distance, uf_ground_truths, old_cred):
    """updates credability"""
    # Update the prior with five more reports
    reports_accuracy = np.array(uf_ground_truths)
    distances = np.array(uf_distance)
    model = uc.UserCredibility(reports_accuracy=reports_accuracy,
                            distances=distances)
    trace = model.build_model(num_samples=1000,
                            prior_credibility=old_cred)  # Use the old posterior as the new prior
    credibility_samples = trace['credibility']
    estimated_credibility = np.mean(credibility_samples)
    return round(estimated_credibility, 2)
