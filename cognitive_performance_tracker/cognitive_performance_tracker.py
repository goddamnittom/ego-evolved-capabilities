import json
import time
from datetime import datetime
import os

METRICS_FILE = '/root/performance_metrics.json'

def log_task(task_id, category, duration, success, errors=0, user_correction=False, notes=""):
    """Logs the metrics for a completed cognitive task."""
    metrics = {}
    if os.path.exists(METRICS_FILE):
        with open(METRICS_FILE, 'r') as f:
            try:
                metrics = json.load(f)
            except json.JSONDecodeError:
                metrics = {}

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "category": category,
        "duration": duration,
        "success": success,
        "errors": errors,
        "user_correction": user_correction,
        "notes": notes
    }
    
    if task_id not in metrics:
        metrics[task_id] = []
    
    metrics[task_id].append(entry)
    
    with open(METRICS_FILE, 'w') as f:
        json.dump(metrics, f, indent=2)

def generate_report():
    """Generates a high-level summary of performance across categories."""
    if not os.path.exists(METRICS_FILE):
        return "No metrics recorded yet."
    
    with open(METRICS_FILE, 'r') as f:
        metrics = json.load(f)
    
    report = {}
    for task_id, entries in metrics.items():
        for e in entries:
            cat = e['category']
            if cat not in report:
                report[cat] = {"count": 0, "success_rate": 0, "avg_duration": 0, "corrections": 0}
            
            report[cat]["count"] += 1
            if e['success']:
                report[cat]["success_rate"] += 1
            if e['user_correction']:
                report[cat]["corrections"] += 1
            report[cat]["avg_duration"] += e['duration']
            
    final_stats = {}
    for cat, stats in report.items():
        final_stats[cat] = {
            "total_tasks": stats["count"],
            "success_rate": f"{(stats['success_rate']/stats['count'])*100:.1f}%",
            "avg_duration_sec": f"{stats['avg_duration']/stats['count']:.2f}",
            "correction_rate": f"{(stats['corrections']/stats['count'])*100:.1f}%"
        }
        
    return json.dumps(final_stats, indent=2)

if __name__ == "__main__":
    log_task("hb_test", "evolution", 0.1, True)
    print(generate_report())
