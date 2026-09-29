import json, os, datetime

# Paths
cvwe_path = '/root/cognitive_value_weighting_engine.py'
axioms_path = '/root/axioms.json'
aeo_queue = '/root/aeo_task_queue.json'

# Load CVWE (contains class definition)
exec(open(cvwe_path).read())

# Load existing axioms (or create placeholder)
if os.path.exists(axioms_path):
    with open(axioms_path) as f:
        axioms = json.load(f)
else:
    axioms = {}

# Determine highest ROI axiom (simple scan)
best_id = None
best_score = -1
cvwe = CognitiveValueWeightingEngine()
for aid, data in axioms.items():
    # assume data contains 'text' field
    txt = data.get('text','')
    score = cvwe.calculate_roi(txt, complexity_estimate=1.0)
    if score > best_score:
        best_score = score
        best_id = aid

if not best_id:
    print('No axioms found for ROI evaluation.')
    exit(0)

# Create a pilot task for AEO
task = {
    'id': f'pilot_{int(datetime.datetime.utcnow().timestamp())}',
    'title': f'Apply high-ROI axiom {best_id}',
    'timestamp': datetime.datetime.utcnow().isoformat(),
    'related_axiom': best_id,
    'metadata': {'roi_score': best_score}
}

# Load existing queue
if os.path.exists(aeo_queue):
    with open(aeo_queue) as f:
        queue = json.load(f)
else:
    queue = []

queue.append(task)
with open(aeo_queue, 'w') as f:
    json.dump(queue, f, indent=2)

print(f'Pilot task queued for axiom {best_id} with ROI {best_score:.2f}')
