"""helpers with blockage reports"""
import models.blockage_credibility as bc
import numpy as np

def blockage_nplist(rows):
    '''Converts SQL rows into np.array readable form'''
    credibilities = []
    severities = []
    for row in rows:
        credibilities.append(row[0])
        severities.append(row[1])
    return credibilities, severities

def run_bm(cred_list, sev_list):
    """Generate some example data for one road"""
    report_credibilities = np.array(cred_list)  # Credibility values for user reports
    severity_ratings = np.array(sev_list)  # Severity ratings for the blockages

    # Instantiate the model for one road
    model = bc.BlockageCredibility(report_credibilities=report_credibilities,
                                severity_ratings=severity_ratings)

    # Calculate the blockage probability
    blockage_probability = model.calculate_blockage_probability()
    return round(blockage_probability, 2)
