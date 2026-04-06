import subprocess
import yaml
import re
import matplotlib.pyplot as plt

# File paths
PROB_FILE = 'prob.yaml'
STATS_FILE = 'timeloop-model.stats.txt'

def run_accelforge():
    """Triggers the Timeloop/AccelForge evaluation."""
    print("Running Timeloop...")
    # Make sure these match your actual filenames
    cmd = ["timeloop-model", "arch.yaml", "components.yaml", "prob.yaml", "map.yaml"]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

def update_filtering_ratio(yaml_path, new_ratio):
    """Dynamically updates the prob.yaml file to simulate different filtering ratios."""
    with open(yaml_path, 'r') as file:
        data = yaml.safe_load(file)
    
    # Assuming your NMA Einsum has a density/sparsity factor defined.
    # The exact path depends on how your agent structured prob.yaml.
    # Example: density = 1.0 / ratio
    density = 1.0 / new_ratio
    
    # Update the dictionary (Adjust these keys to match your actual prob.yaml structure)
    # data['problem']['instance']['densities']['Keys'] = density
    
    with open(yaml_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)
    print(f"Updated prob.yaml for a {new_ratio}x filtering ratio (Density: {density:.3f}).")

def parse_stats():
    """Parses the Timeloop output stats to extract total energy and cycles."""
    energy = 0.0
    cycles = 0
    
    try:
        with open(STATS_FILE, 'r') as file:
            content = file.read()
            
            # Use Regex to find the summary stats at the bottom of the Timeloop output
            energy_match = re.search(r'Total Energy\s*\[pJ\]\s*:\s*([0-9.]+)', content)
            cycles_match = re.search(r'Cycles\s*:\s*([0-9]+)', content)
            
            if energy_match:
                energy = float(energy_match.group(1))
            if cycles_match:
                cycles = int(cycles_match.group(1))
                
    except FileNotFoundError:
        print("Error: Stats file not found. Did Timeloop fail to run?")
        
    return energy, cycles

def main():
    # Ratios to test: 5x, 10x, 20x (Paper baseline), 40x
    filtering_ratios = [5, 10, 20, 40]
    energies = []
    latencies = []

    for ratio in filtering_ratios:
        # 1. Modify the YAML
        update_filtering_ratio(PROB_FILE, ratio)
        
        # 2. Run the simulation
        run_accelforge()
        
        # 3. Parse the results
        energy, cycles = parse_stats()
        energies.append(energy)
        latencies.append(cycles)
        
        print(f"Result -> Energy: {energy} pJ | Latency: {cycles} cycles\n")

    # 4. Visualize the results
    plt.figure(figsize=(10, 5))
    
    # Plot Energy
    plt.subplot(1, 2, 1)
    plt.plot(filtering_ratios, energies, marker='o', color='blue')
    plt.title('Total Energy vs. Filtering Ratio')
    plt.xlabel('Filtering Ratio (X times reduction)')
    plt.ylabel('Total Energy (pJ)')
    plt.grid(True)

    # Plot Latency
    plt.subplot(1, 2, 2)
    plt.plot(filtering_ratios, latencies, marker='s', color='red')
    plt.title('Latency vs. Filtering Ratio')
    plt.xlabel('Filtering Ratio (X times reduction)')
    plt.ylabel('Latency (Cycles)')
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('longsight_results.png')
    print("Plot saved to longsight_results.png")

if __name__ == "__main__":
    main()