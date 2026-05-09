"""
Flask REST API Application with Prometheus Metrics
Main entry point for the REST API server with monitoring capabilities
"""

from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics
import psutil
import time
import threading

app = Flask(__name__)

from prometheus_flask_exporter import PrometheusMetrics

# Initialize Prometheus metrics
metrics = PrometheusMetrics(app)

# Explicitly add metrics endpoint
@app.route('/metrics')
def metrics_endpoint():
    from prometheus_client import generate_latest
    return generate_latest(), 200, {'Content-Type': 'text/plain; charset=utf-8'}


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Server is running'}), 200


@app.route('/api/hello', methods=['GET'])
def hello():
    """Simple hello endpoint"""
    name = request.args.get('name', 'World')
    return jsonify({'message': f'Hello, {name}!'}), 200


@app.route('/api/items', methods=['GET'])
def get_items():
    """Get all items"""
    items = [
        {'id': 1, 'name': 'Item 1', 'description': 'First item'},
        {'id': 2, 'name': 'Item 2', 'description': 'Second item'},
        {'id': 3, 'name': 'Item 3', 'description': 'Third item'},
    ]
    return jsonify({'items': items}), 200


@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Get a specific item by ID"""
    items = {
        1: {'id': 1, 'name': 'Item 1', 'description': 'First item'},
        2: {'id': 2, 'name': 'Item 2', 'description': 'Second item'},
        3: {'id': 3, 'name': 'Item 3', 'description': 'Third item'},
    }
    
    if item_id not in items:
        return jsonify({'error': 'Item not found'}), 404
    
    return jsonify(items[item_id]), 200


@app.route('/api/items', methods=['POST'])
def create_item():
    """Create a new item"""
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Invalid request. "name" is required'}), 400
    
    new_item = {
        'id': 4,
        'name': data.get('name'),
        'description': data.get('description', '')
    }
    
    return jsonify(new_item), 201


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
