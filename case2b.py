import matplotlib.pyplot as plt
import numpy as np
from juzzyPython.generic.Tuple import Tuple
from juzzyPython.generic.Output import Output
from juzzyPython.generic.Input import Input
from juzzyPython.type1.sets.T1MF_Triangular import T1MF_Triangular
from juzzyPython.type1.sets.T1MF_Trapezoidal import T1MF_Trapezoidal
from juzzyPython.type1.system.T1_Rule import T1_Rule
from juzzyPython.type1.system.T1_Antecedent import T1_Antecedent
from juzzyPython.type1.system.T1_Consequent import T1_Consequent
from juzzyPython.type1.system.T1_Rulebase import T1_Rulebase

def perform_fls_case1(age_interval, headache_interval, temp_interval):
    age_low, age_high = age_interval
    headache_low, headache_high = headache_interval
    temp_low_val, temp_high_val = temp_interval

    # Inputs/Outputs
    patient_age_input = Input("Patient Age", Tuple(0, 130))
    headache_severity_input = Input("Headache Severity", Tuple(0, 10))
    patient_temperature_input = Input("Patient Temperature", Tuple(30, 45))
    patient_urgency_output = Output("Patient Urgency", Tuple(0, 100))

    # Membership functions --------------------------------
    temp_low = T1MF_Trapezoidal("LowTemp", [30, 30, 35.5, 36.3])
    temp_normal = T1MF_Triangular("NormalTemp", 35.8, 37, 38.3)
    temp_high = T1MF_Trapezoidal("HighTemp", [37.8, 39.5, 45, 45])

    headache_mild = T1MF_Trapezoidal("MildHeadache", [0, 0, 1.5, 4.5])
    headache_moderate = T1MF_Triangular("ModerateHeadache", 3, 5, 7)
    headache_severe = T1MF_Trapezoidal("SevereHeadache", [5.5, 8.5, 10, 10])

    age_young = T1MF_Trapezoidal("Young", [0, 0, 12, 25])
    age_adult = T1MF_Triangular("Adult", 20, 40, 65)
    age_elderly = T1MF_Trapezoidal("Elderly", [55, 80, 130, 130])

    urgency_standard = T1MF_Trapezoidal("Standard", [0, 0, 30, 50])
    urgency_urgent = T1MF_Triangular("Urgent", 40, 55, 70)
    urgency_emergency = T1MF_Trapezoidal("Emergency", [60, 80, 100, 100])

    # Antecedents -----------------------------------------
    temp_low_a = T1_Antecedent(temp_low, patient_temperature_input, "TempLow")
    temp_normal_a = T1_Antecedent(temp_normal, patient_temperature_input, "TempNormal")
    temp_high_a = T1_Antecedent(temp_high, patient_temperature_input, "TempHigh")

    headache_mild_a = T1_Antecedent(headache_mild, headache_severity_input, "HeadacheMild")
    headache_moderate_a = T1_Antecedent(headache_moderate, headache_severity_input, "HeadacheModerate")
    headache_severe_a = T1_Antecedent(headache_severe, headache_severity_input, "HeadacheSevere")

    age_young_a = T1_Antecedent(age_young, patient_age_input, "AgeYoung")
    age_adult_a = T1_Antecedent(age_adult, patient_age_input, "AgeAdult")
    age_elderly_a = T1_Antecedent(age_elderly, patient_age_input, "AgeElderly")

    urgency_std_c = T1_Consequent(urgency_standard, patient_urgency_output, "UrgencyStandard")
    urgency_urg_c = T1_Consequent(urgency_urgent, patient_urgency_output, "UrgencyUrgent")
    urgency_emg_c = T1_Consequent(urgency_emergency, patient_urgency_output, "UrgencyEmergency")

    rulebase = T1_Rulebase()

    # EMERGENCY OVERRIDES -------------------------------
    for h in [headache_mild_a, headache_moderate_a, headache_severe_a]:
        for a in [age_young_a, age_adult_a, age_elderly_a]:
            rulebase.addRule(T1_Rule([temp_low_a, h, a], urgency_emg_c))
            rulebase.addRule(T1_Rule([temp_high_a, h, a], urgency_emg_c))

    # Normal temperature rules
    rulebase.addRule(T1_Rule([temp_normal_a, headache_mild_a, age_young_a], urgency_std_c))
    rulebase.addRule(T1_Rule([temp_normal_a, headache_mild_a, age_adult_a], urgency_std_c))
    rulebase.addRule(T1_Rule([temp_normal_a, headache_mild_a, age_elderly_a], urgency_std_c))

    rulebase.addRule(T1_Rule([temp_normal_a, headache_moderate_a, age_young_a], urgency_urg_c))
    rulebase.addRule(T1_Rule([temp_normal_a, headache_moderate_a, age_adult_a], urgency_std_c))
    rulebase.addRule(T1_Rule([temp_normal_a, headache_moderate_a, age_elderly_a], urgency_urg_c))

    rulebase.addRule(T1_Rule([temp_normal_a, headache_severe_a, age_young_a], urgency_urg_c))
    rulebase.addRule(T1_Rule([temp_normal_a, headache_severe_a, age_adult_a], urgency_urg_c))
    rulebase.addRule(T1_Rule([temp_normal_a, headache_severe_a, age_elderly_a], urgency_urg_c))

    # Evaluate LOW inputs
    patient_urgency_output.setDiscretisationLevel(100)
    patient_age_input.setInput(age_low)
    headache_severity_input.setInput(headache_low)
    patient_temperature_input.setInput(temp_low_val)
    output_low = rulebase.evaluate(1)[patient_urgency_output]

    # Evaluate HIGH inputs
    patient_age_input.setInput(age_high)
    headache_severity_input.setInput(headache_high)
    patient_temperature_input.setInput(temp_high_val)
    output_high = rulebase.evaluate(1)[patient_urgency_output]

    urgency_mid = (output_low + output_high) / 2

    print(f"\nDefuzzified Urgency Interval: [{output_low:.2f}, {output_high:.2f}]")

   
    fig, axes = plt.subplots(3, 1, figsize=(10, 10))

    # ---------------- AGE ----------------
    x_age = np.linspace(0, 130, 400)
    labels = []
    for mf in [age_young, age_adult, age_elderly]:
        axes[0].plot(x_age, [mf.getFS(x) for x in x_age])
        mu_low = mf.getFS(age_low)
        mu_high = mf.getFS(age_high)
        labels.append(f"{mf.getName()} (μ ∈ [{mu_low:.2f}, {mu_high:.2f}])")

    axes[0].axvspan(age_low, age_high, color='red', alpha=0.2, label="Input Interval")
    axes[0].set_title("Age Membership Functions")
    axes[0].legend(labels + ["Input Interval"])

    # ---------------- HEADACHE ----------------
    x_head = np.linspace(0, 10, 400)
    labels = []
    for mf in [headache_mild, headache_moderate, headache_severe]:
        axes[1].plot(x_head, [mf.getFS(x) for x in x_head])
        mu_low = mf.getFS(headache_low)
        mu_high = mf.getFS(headache_high)
        labels.append(f"{mf.getName()} (μ ∈ [{mu_low:.2f}, {mu_high:.2f}])")

    axes[1].axvspan(headache_low, headache_high, color='red', alpha=0.2, label="Input Interval")
    axes[1].set_title("Headache Membership Functions")
    axes[1].legend(labels + ["Input Interval"])

    # ---------------- TEMPERATURE ----------------
    x_temp = np.linspace(30, 45, 400)
    labels = []
    for mf in [temp_low, temp_normal, temp_high]:
        axes[2].plot(x_temp, [mf.getFS(x) for x in x_temp])
        mu_low = mf.getFS(temp_low_val)
        mu_high = mf.getFS(temp_high_val)
        labels.append(f"{mf.getName()} (μ ∈ [{mu_low:.2f}, {mu_high:.2f}])")

    axes[2].axvspan(temp_low_val, temp_high_val, color='red', alpha=0.2, label="Input Interval")
    axes[2].set_title("Temperature Membership Functions")
    axes[2].legend(labels + ["Input Interval"])

    plt.tight_layout()
    plt.show()

   

    fig, ax = plt.subplots(figsize=(10, 5))
    x_urg = np.linspace(0, 100, 400)

    for mf in [urgency_standard, urgency_urgent, urgency_emergency]:
        ax.plot(x_urg, [mf.getFS(x) for x in x_urg], linewidth=2)

    ax.axvspan(output_low, output_high, color='red', alpha=0.25,
               label=f"Output Interval [{output_low:.2f}, {output_high:.2f}]")

    # Aggregated MF
    x_vals = np.linspace(0, 100, 500)
    aggregated = np.zeros_like(x_vals)
    for rule in rulebase.getRules():
        for cons in rule.getConsequents():
            mf = cons.getMF()
            alpha = rule.getFStrength(1)
            clipped = np.array([min(mf.getFS(x), alpha) for x in x_vals])
            aggregated = np.maximum(aggregated, clipped)

    ax.fill_between(x_vals, 0, aggregated, color="blue", alpha=0.3, label="Aggregated MF")

    ax.axvline(urgency_mid, color='purple', linestyle='--')
    ax.plot([urgency_mid], [0], 'o', color='purple',
            label=f"Midpoint = {urgency_mid:.2f}")

    ax.set_title("Output Urgency Membership Functions")
    ax.set_xlabel("Urgency Score")
    ax.set_ylabel("Membership Degree")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    return output_low, output_high


def main():
    try:
        age_min = float(input("Enter patient age minimum (0–130): "))
        age_max = float(input("Enter patient age maximum (0–130): "))
        headache_min = float(input("Enter headache severity minimum (0–10): "))
        headache_max = float(input("Enter headache severity maximum (0–10): "))
        temp_min = float(input("Enter temperature minimum (30–45 °C): "))
        temp_max = float(input("Enter temperature maximum (30–45 °C): "))

        urgency_interval = perform_fls_case1(
            (age_min, age_max),
            (headache_min, headache_max),
            (temp_min, temp_max)
        )
        print(f"\nFinal Defuzzified Urgency Interval = [{urgency_interval[0]:.2f}, {urgency_interval[1]:.2f}]")

    except ValueError as e:
        print(f"Invalid input: {e}")


if __name__ == "__main__":
    main()
