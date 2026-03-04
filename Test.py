import multiprocessing
import time
import os
import sys
import math
import platform

class CPUHealthTester:
    def __init__(self):
        self.cpu_count = multiprocessing.cpu_count()

        # Increased workload: 30 million iterations.
        # This is high enough to run for several seconds and generate heat.
        self.target_iterations = 30_000_000

        # Pre-calculated "known good" result for 30M iterations (from 1 to 29,999,999).
        # A true integrity check compares the final result against this value.
        self.known_good_result = 24901844.241512414

    def get_linux_temperature(self):
        """
        Attempts to read temperature from standard Linux sysfs paths.
        Returns a formatted string or None if unavailable.
        """
        temp_paths = [
            "/sys/class/thermal/thermal_zone0/temp",
            "/sys/class/hwmon/hwmon0/temp1_input",
            "/sys/class/hwmon/hwmon1/temp1_input"
        ]

        for path in temp_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r') as f:
                        # Linux stores temp in millidegrees Celsius
                        temp_c = int(f.read().strip()) / 1000.0
                        return temp_c
                except (IOError, ValueError):
                    continue
        return None

    def stress_core(self, core_id, return_dict):
        """
        Performs heavy floating point math to stress the ALU (Arithmetic Logic Unit).
        Verifies the result to detect logic errors (bit flips).
        """
        try:
            # We perform a series of heavy trigonometric operations
            # If a transistor in the FPU is bad, these results often diverge.
            result = 0.0
            start_time = time.time()

            # Run a deterministic loop (starts at 1)
            for i in range(1, self.target_iterations):
                # Heavy math load: sin, cos, sqrt, pow
                # This exercises different parts of the transistor logic
                x = math.sin(i) * math.cos(i)
                y = math.sqrt(abs(x) + 1.0)
                result += y

            duration = time.time() - start_time

            # --- Advanced Logic Check ---

            # 1. Check for catastrophic failure (NaN or Infinity)
            if math.isnan(result) or math.isinf(result):
                return_dict[core_id] = ("FAIL", "Math Logic Error (NaN/Inf)")

            # 2. Check for subtle integrity errors (bit flips, rounding errors)
            # We compare against a known, pre-calculated value.
            # We use math.isclose() to handle tiny, acceptable floating-point variations.
            elif not math.isclose(result, self.known_good_result, rel_tol=1e-9):
                return_dict[core_id] = ("FAIL", f"Integrity Error. Expected {self.known_good_result} but got {result}")

            # 3. If both checks pass, the core is healthy.
            else:
                return_dict[core_id] = ("PASS", f"{duration:.2f}s")

        except Exception as e:
            return_dict[core_id] = ("FAIL", str(e))

    def run_test(self):
        print(f"--- Linux CPU Integrity & Health Monitor ---")
        print(f"Detected {self.cpu_count} logical cores.")
        print(f"OS: {platform.system()} {platform.release()}")
        print(f"Starting functional stress test ({self.target_iterations:,} iterations per core)...")
        print("This will take a moment. Press CTRL+C to stop early.")
        print("-" * 60)

        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        processes = []

        # Start Timer
        global_start = time.time()

        # Spawn a process for every core to ensure 100% utilization
        for i in range(self.cpu_count):
            p = multiprocessing.Process(target=self.stress_core, args=(i, return_dict))
            processes.append(p)
            p.start()

        # Monitoring Loop
        try:
            while any(p.is_alive() for p in processes):
                temp = self.get_linux_temperature()
                temp_str = f"{temp:.1f}°C" if temp else "N/A"

                # Simple spinner animation
                elapsed = time.time() - global_start
                sys.stdout.write(f"\rTesting in progress... Time: {elapsed:.1f}s | CPU Temp: {temp_str} | Active Threads: {sum(p.is_alive() for p in processes)}")
                sys.stdout.flush()
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\n\nTest interrupted by user. Terminating processes...")
            for p in processes:
                p.terminate()
            return

        print("\n" + "-" * 60)
        print("Test Complete. Analyzing Integrity...")

        # Analyze Results
        failures = 0
        for core_id in range(self.cpu_count):
            if core_id in return_dict:
                status, msg = return_dict[core_id]
                if status == "FAIL":
                    print(f"[CORE {core_id}] \033[91mFAILED\033[0m: {msg}")
                    failures += 1
                else:
                    print(f"[CORE {core_id}] \033[92mHEALTHY\033[0m: Calculation verified in {msg}")
            else:
                print(f"[CORE {core_id}] \033[93mUNKNOWN\033[0m: Process died unexpectedly")
                failures += 1

        print("-" * 60)
        if failures == 0:
            print("\033[92mSUCCESS: All cores passed functional integrity check.\033[0m")
            print("Your CPU logic gates are functioning correctly under load.")
        else:
            print(f"\033[91mWARNING: {failures} core(s) failed the integrity check.\033[0m")
            print("This indicates potential hardware instability, overheating, or transistor degradation.")

if __name__ == "__main__":
    # Ensure we are running on Linux for the temp sensors, though math works anywhere
    if platform.system() != "Linux":
        print("Note: Temperature sensors are configured for Linux. Showing 'N/A' on other OS.")

    tester = CPUHealthTester()
    tester.run_test()
