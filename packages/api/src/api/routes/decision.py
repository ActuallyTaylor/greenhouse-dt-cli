from apiflask import APIBlueprint, HTTPTokenAuth

decision_bp = APIBlueprint('decision_api', __name__)
auth = HTTPTokenAuth('Bearer')

# TODO: Implement all endpoints from DecisionController.kt
# GET /api/decision/strategies
# GET /api/decision/plant-strategies
# POST /api/decision/reload
