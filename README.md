CPU Integrity & Health MonitorA lightweight, Python-based stress testing tool designed to verify CPU stability, thermal performance, and computational accuracy.Unlike simple "burn" tests that just generate heat, this tool verifies the integrity of your CPU's floating-point unit (FPU) by comparing calculation results against known constants.🚀 FeaturesMulti-Core Stress Testing: Automatically detects and saturates all available logical cores using Python's multiprocessing.Logic Integrity Verification: Performs millions of heavy trigonometric calculations (sin, cos, sqrt) and validates the final result to detect:Calculation errors (Bit flips)Logic failures (NaN / Infinity)Transistor degradation under loadReal-Time Monitoring: Displays live test duration, active thread count, and CPU temperature (Linux only).Cross-Platform Logic: Math stress tests work on Windows, macOS, and Linux (Temperature sensors are Linux-specific).📋 PrerequisitesPython 3.6+No external dependencies required (uses standard libraries only).🛠️ Installation & UsageClone the repository:git clone [https://github.com/yourusername/cpu-integrity-monitor.git](https://github.com/yourusername/cpu-integrity-monitor.git)
cd cpu-integrity-monitor
Run the script:python3 cpu_health_tester.py
(Note: If your file is named Test.py, run python3 Test.py instead)Stop the test:The test runs for a fixed number of iterations. To stop it early, press CTRL+C.🔍 How It WorksWorkload Generation: The script spawns a separate process for each CPU core.Math Stress: Each core enters a loop performing 30 million iterations of complex floating-point math:x = math.sin(i) * math.cos(i)
y = math.sqrt(abs(x) + 1.0)
Verification: - Most stress tests simply discard the result.This tool sums the results and compares the final value against a pre-calculated known good hash.If the result differs even slightly (beyond standard floating-point tolerance), it reports an Integrity Error.🖥️ Example Output--- Linux CPU Integrity & Health Monitor ---
Detected 16 logical cores.
OS: Linux 5.15.0-generic
Starting functional stress test (30,000,000 iterations per core)...
This will take a moment. Press CTRL+C to stop early.
------------------------------------------------------------
Testing in progress... Time: 14.2s | CPU Temp: 72.0°C | Active Threads: 16

------------------------------------------------------------
Test Complete. Analyzing Integrity...
[CORE 0] HEALTHY: Calculation verified in 14.52s
[CORE 1] HEALTHY: Calculation verified in 14.55s
...
[CORE 15] HEALTHY: Calculation verified in 14.60s
------------------------------------------------------------
SUCCESS: All cores passed functional integrity check.
Your CPU logic gates are functioning correctly under load.
⚠️ DisclaimerUse at your own risk. This software places a heavy load on your CPU, which will generate significant heat. Ensure your cooling system is functioning correctly before running this test for extended periods. The authors are not responsible for hardware damage resulting from overheating or existing hardware faults.📄 LicenseThis project is licensed under the MIT License - see the LICENSE file for details.
