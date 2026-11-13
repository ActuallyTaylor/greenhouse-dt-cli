from apiflask import APIBlueprint
from flask import jsonify, request

decision_bp = APIBlueprint('decision_api', __name__)

@decision_bp.post('/api/decision/strategy/', methods=['POST'])
@decision_bp.input()
def set_watering_strategy(strategyName: str):
    return jsonify([]),

