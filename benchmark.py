#!/usr/bin/env python3
"""
Script de Benchmark et Profilage des Ressources Docker
Mesure la latence, le débit (RPS) et la consommation CPU/RAM de l'architecture.
"""

import time
import urllib.request
import concurrent.futures
import subprocess
import json

TARGET_URL = "http://localhost:8080/api"
CONCURRENCY = 10
TOTAL_REQUESTS = 300

def get_docker_stats():
    """Récupère les métriques en temps réel des conteneurs via docker stats."""
    try:
        cmd = [
            "docker", "stats", "--no-stream",
            "--format", "{{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.PIDs}}"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        stats = []
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) >= 5:
                stats.append({
                    "name": parts[0],
                    "cpu": parts[1],
                    "mem": parts[2],
                    "mem_perc": parts[3],
                    "pids": parts[4]
                })
        return stats
    except Exception as e:
        return [{"error": str(e)}]

def send_request(idx):
    """Envoie une requête HTTP et mesure la latence en millisecondes."""
    start = time.perf_counter()
    try:
        req = urllib.request.Request(
            TARGET_URL,
            headers={"User-Agent": "DockerBenchmark/1.0"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            code = response.getcode()
            elapsed_ms = (time.perf_counter() - start) * 1000.0
            return (code == 200, elapsed_ms)
    except Exception:
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        return (False, elapsed_ms)

def run_benchmark():
    print("=" * 70)
    print("   BENCHMARK ARCHITECTURE DOCKER - LABYRINTHE WARHAMMER")
    print("=" * 70)
    print(f"Cible : {TARGET_URL}")
    print(f"Nombre total de requêtes : {TOTAL_REQUESTS}")
    print(f"Concurrence : {CONCURRENCY} threads\n")

    print("[1/3] Mesure de la consommation à vide (Idle) :")
    idle_stats = get_docker_stats()
    for s in idle_stats:
        if "error" not in s:
            print(f"  - {s['name']:<20} CPU: {s['cpu']:<8} RAM: {s['mem']:<20} ({s['mem_perc']}) PIDs: {s['pids']}")

    print("\n[2/3] Exécution du test de charge en cours...")
    latencies = []
    successes = 0

    bench_start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
        futures = [executor.submit(send_request, i) for i in range(TOTAL_REQUESTS)]
        for fut in concurrent.futures.as_completed(futures):
            ok, lat = fut.result()
            latencies.append(lat)
            if ok:
                successes += 1
    bench_duration = time.perf_counter() - bench_start

    print("[3/3] Mesure de la consommation sous charge :")
    load_stats = get_docker_stats()
    for s in load_stats:
        if "error" not in s:
            print(f"  - {s['name']:<20} CPU: {s['cpu']:<8} RAM: {s['mem']:<20} ({s['mem_perc']}) PIDs: {s['pids']}")

    # Analyse statistique
    rps = TOTAL_REQUESTS / bench_duration if bench_duration > 0 else 0
    avg_lat = sum(latencies) / len(latencies) if latencies else 0
    latencies.sort()
    min_lat = latencies[0] if latencies else 0
    max_lat = latencies[-1] if latencies else 0
    p95_lat = latencies[int(len(latencies) * 0.95)] if latencies else 0

    print("\n" + "=" * 70)
    print("   RÉSULTATS DE LA MESURE DE PERFORMANCE")
    print("=" * 70)
    print(f"Durée du test           : {bench_duration:.2f} s")
    print(f"Requêtes réussies       : {successes}/{TOTAL_REQUESTS} ({successes/TOTAL_REQUESTS*100:.1f}%)")
    print(f"Débit moyen (RPS)       : {rps:.2f} requêtes/sec")
    print(f"Latence moyenne         : {avg_lat:.2f} ms")
    print(f"Latence minimale        : {min_lat:.2f} ms")
    print(f"Latence p95             : {p95_lat:.2f} ms")
    print(f"Latence maximale        : {max_lat:.2f} ms")
    print("=" * 70)

if __name__ == "__main__":
    run_benchmark()

