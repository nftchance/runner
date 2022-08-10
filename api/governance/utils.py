PROPOSAL_SUBMISSION_BALANCE_MINIMUM = 100000
PROPOSAL_DURATION_DAYS = 30

class Vote:
    FOR = 'for'
    AGAINST = 'against'
    ABSTAIN = 'abstain'

    VOTES = (
        (FOR, 'For'),
        (AGAINST, 'Against'),
        (ABSTAIN, 'Abstain'),
    )

class Tag:
    DASHBOARD = "dashboard"
    FEES = "fees"
    FINANCIALS = "financials"
    GOVERNANCE = "governance"
    INTEGRATIONS = "integrations"
    PAYMENTS = "payments"
    REVIEWS = "reviews"
    TAXES = "taxes"
    UX = "ux"

    TAGS = (
        (DASHBOARD, "Dashboard"),
        (FEES, "Fees"),
        (FINANCIALS, "Financials"),
        (GOVERNANCE, "Governance"),
        (INTEGRATIONS, "Integrations"),
        (PAYMENTS, "Payments"),
        (REVIEWS, "Reviews"),
        (TAXES, "Taxes"),
        (UX, "UX"),
    )