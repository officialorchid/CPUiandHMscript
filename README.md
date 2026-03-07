# 🔥 CPU Integrity & Health Monitor

[![Python](https://img.shields.io/badge/Python-3.6+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-4CAF50)](https://github.com/yourusername/cpu-integrity-monitor)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **A precision stress testing tool that verifies CPU stability through mathematical integrity checks.**

Unlike conventional "burn-in" tests that merely generate heat, this tool performs rigorous floating-point calculations and validates results against known constants to detect hardware defects, bit-flips, and transistor degradation.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🧮 **Mathematical Integrity** | Validates FPU calculations against pre-computed constants |
| 🌡️ **Thermal Monitoring** | Real-time CPU temperature tracking (Linux) |
| ⚡ **Full Core Saturation** | Automatically utilizes all logical cores |
| 🔍 **Error Detection** | Identifies logic failures, NaN/Inf results, and precision errors |
| 🖥️ **Cross-Platform** | Works on Linux, macOS, and Windows |

---

## 📦 Installation

### Requirements
- Python 3.6 or higher
- No external dependencies (uses standard library only)

### Quick Start
```bash
# Clone the repository
git clone https://github.com/officialorchid/CPUiandHMscript.git
cd CPUiandHMscript
uv venv
source .venv/bin/activate



# Run the test
#python3 Test.py
```

---

## 🚀 Usage

### Basic Usage
```bash
uv run Test.py
#python3 Test.py
```

The test will automatically:
1. Detect all available CPU cores
2. Spawn parallel stress processes
3. Monitor temperature and progress in real-time
4. Validate calculation integrity
5. Report detailed results per core

### Expected Output
```
--- Linux CPU Integrity & Health Monitor ---
Detected 16 logical cores.
OS: Linux 5.15.0-generic
Starting functional stress test (30,000,000 iterations per core)...
------------------------------------------------------------
Testing in progress... Time: 14.2s | CPU Temp: 72.0°C | Active Threads: 16
------------------------------------------------------------
Test Complete. Analyzing Integrity...
[CORE 0]  HEALTHY: Calculation verified in 14.52s
[CORE 1]  HEALTHY: Calculation verified in 14.55s
...
[CORE 15] HEALTHY: Calculation verified in 14.60s
------------------------------------------------------------
SUCCESS: All cores passed functional integrity check.
```

### Stopping the Test
Press `CTRL+C` at any time to interrupt testing and gracefully terminate all processes.

---

## 🔬 How It Works

### The Science Behind the Test

1. **Workload Generation**
   - Spawns isolated processes for each logical core
   - Achieves true parallelism via Python's `multiprocessing`

2. **Mathematical Stress**
   - Executes 30 million iterations of complex floating-point operations:
   ```python
   x = math.sin(i) * math.cos(i)
   y = math.sqrt(abs(x) + 1.0)
   result += y
   ```

3. **Integrity Verification**
   - Compares final result against pre-calibrated constant: `24901844.241512414`
   - Uses `math.isclose()` with 1e-9 relative tolerance
   - Detects bit-flips, rounding errors, and FPU defects

4. **Error Classification**
   - **Logic Errors**: NaN or Infinity results
   - **Integrity Errors**: Result deviation beyond tolerance
   - **Process Failures**: Unexpected termination or crashes

---

## ⚙️ Configuration

### Adjusting Workload Intensity
Modify the iteration count in `Test.py`:
```python
# Default: 30 million iterations
self.target_iterations = 30_000_000  # ~15-30 seconds per core
```

### Temperature Sensors (Linux)
The tool automatically checks these paths:
- `/sys/class/thermal/thermal_zone0/temp`
- `/sys/class/hwmon/hwmon0/temp1_input`
- `/sys/class/hwmon/hwmon1/temp1_input`

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Ensure Python 3.6+ is installed: `python3 --version` |
| Temperature shows "N/A" | Normal on Windows/macOS. Install `lm-sensors` on Linux for additional support |
| High CPU temperatures | Ensure adequate cooling. Stop with `CTRL+C` if thermal throttling occurs |
| Slow performance | Expected on older CPUs or systems with fewer cores |

---

## ⚠️ Safety Notice

**Use at your own risk.** This software places sustained 100% load on all CPU cores, generating significant heat. 

**Before running:**
- ✅ Verify cooling system functionality
- ✅ Monitor temperatures during first run
- ✅ Avoid running on laptops with blocked vents
- ✅ Stop immediately if thermal throttling occurs

The authors assume no liability for hardware damage resulting from overheating or pre-existing hardware faults.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Inspired by classic FPU stress tests like Prime95 and SuperPI
- Built with Python's robust `multiprocessing` and `math` libraries

---

<div align="center">

**[⬆ Back to Top](#-cpu-integrity--health-monitor)**

Made with ❤️ and 🔥 by [officialorchid](https://github.com/officialorchid)

</div>
