from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
from .agent import LiveSoftware, config

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/request', methods=['POST'])
def handle_request():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Invalid request, 'message' key is required"}), 400
    
    user_message = data['message']
    try:
        response = live_software.request(user_message)
        return jsonify(response)
    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/api/structure', methods=['GET'])
def get_structure():
    graph_type = request.args.get('type', 'node')
    node_id = request.args.get('node_id')
    
    structure_dict = live_software.get_structure()
    if not isinstance(structure_dict, dict) or not structure_dict:
        return jsonify({"elements": {"nodes": [{"data": {"id": "Meta", "label": "Meta"}}], "edges": []}})
    nodes = []
    edges = []
    nodes.append({"data": {"id": "Meta", "label": "Meta"}})

    if graph_type == 'class' and node_id and node_id in structure_dict:
        nodes.append({"data": {"id": str(node_id), "label": str(node_id)}})
        edges.append({"data": {"source": "Meta", "target": str(node_id)}})
        methods = structure_dict.get(node_id, [])
        filtered_methods = []
        main_method_exists = False
        for method_str in methods:
            if "__main__" in method_str:
                if not main_method_exists:
                    filtered_methods.append("main()")
                    main_method_exists = True
            elif method_str not in filtered_methods:
                 filtered_methods.append(method_str)
        for method_str in filtered_methods:
            method_name = method_str.split('(')[0].strip()
            if not method_name:
                continue            
            method_node_id = f"{method_name}"
            nodes.append({"data": {"id": method_node_id, "label": method_name}})
            edges.append({"data": {"source": str(node_id), "target": method_node_id}})
    else:
        # Node Graph View (default): Meta -> file
        for file_name in structure_dict.keys():
            if file_name.startswith('__'):
                continue
            nodes.append({"data": {"id": str(file_name), "label": str(file_name)}})
            edges.append({"data": {"source": "Meta", "target": str(file_name)}})

    elements = {"nodes": nodes, "edges": edges}
    return jsonify({"elements": elements})

@app.route('/api/code_get', methods=['POST'])
def get_code():
    data = request.get_json()
    node_id = data.get('node_id')
    if not node_id:
        return jsonify({"error": "node_id is required"}), 400
    try:
        all_codes = live_software.state_manager.load_code()
        node_code = all_codes.get(node_id, f"# Code for '{node_id}' not found.")
        return jsonify({"code": node_code})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    live_software = LiveSoftware(config)
    app.run(host='0.0.0.0', port=5001, debug=True)