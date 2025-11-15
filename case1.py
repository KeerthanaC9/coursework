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

def perform_fls_case1(age_val, headache_val, temp_val):
  
    patient_age_input = Input("Patient Age", Tuple(0,130))
    headache_severity_input = Input("Headache Severity", Tuple(0,10))
    patient_temperature_input = Input("Patient Temperature", Tuple(30,45))
    patient_urgency_output = Output("Patient Urgency", Tuple(0,100))



    temp_low    = T1MF_Trapezoidal("LowTemp", [30, 30, 35.5, 36.3])
    temp_normal = T1MF_Triangular("NormalTemp", 35.8, 37, 38.3)
    temp_high   = T1MF_Trapezoidal("HighTemp", [37.8, 39.5, 45, 45])

   
    headache_mild     = T1MF_Trapezoidal("MildHeadache", [0, 0, 1.5, 4.5])
    headache_moderate = T1MF_Triangular("ModerateHeadache", 3, 5, 7)
    headache_severe   = T1MF_Trapezoidal("SevereHeadache", [5.5, 8.5, 10, 10])


    age_young   = T1MF_Trapezoidal("Young", [0,0, 12, 25])
    age_adult   = T1MF_Triangular("Adult", 20, 40, 65)
    age_elderly = T1MF_Trapezoidal("Elderly", [55, 80, 130, 130])

  
    urgency_standard  = T1MF_Trapezoidal("Standard", [0, 0, 30, 50])
    urgency_urgent    = T1MF_Triangular("Urgent", 40, 55, 70)
    urgency_emergency = T1MF_Trapezoidal("Emergency", [60, 80, 100, 100])

    temp_low_a    = T1_Antecedent(temp_low,    patient_temperature_input, "TempLow")
    temp_normal_a = T1_Antecedent(temp_normal, patient_temperature_input, "TempNormal")
    temp_high_a   = T1_Antecedent(temp_high,   patient_temperature_input, "TempHigh")

    headache_mild_a     = T1_Antecedent(headache_mild,     headache_severity_input, "HeadacheMild")
    headache_moderate_a = T1_Antecedent(headache_moderate, headache_severity_input, "HeadacheModerate")
    headache_severe_a   = T1_Antecedent(headache_severe,   headache_severity_input, "HeadacheSevere")

    age_young_a   = T1_Antecedent(age_young,   patient_age_input, "AgeYoung")
    age_adult_a   = T1_Antecedent(age_adult,   patient_age_input, "AgeAdult")
    age_elderly_a = T1_Antecedent(age_elderly, patient_age_input, "AgeElderly")

    urgency_std_c = T1_Consequent(urgency_standard,  patient_urgency_output, "UrgencyStandard")
    urgency_urg_c = T1_Consequent(urgency_urgent,    patient_urgency_output, "UrgencyUrgent")
    urgency_emg_c = T1_Consequent(urgency_emergency, patient_urgency_output, "UrgencyEmergency")

   
    rulebase = T1_Rulebase()

    # ==============================================================================
    # 1. ABSOLUTE EMERGENCY OVERRIDES (TempLow and TempHigh)
    #    These rules cover critical physiological extremes (Hypothermia or High Fever/Hyperpyrexia)
    #    and result in Emergency (urgency_emg_c) regardless of minor symptom variations,
    #    as per the precautionary principle in triage. 
    # ==============================================================================

    # 1.1. IF Temp IS Low THEN Urgency IS Emergency (9 Rules)
    rulebase.addRule(T1_Rule([temp_low_a, headache_mild_a, age_young_a], urgency_emg_c))
    rulebase.addRule(T1_Rule([temp_low_a, headache_mild_a, age_adult_a], urgency_emg_c))
    rulebase.addRule(T1_Rule([temp_low_a, headache_mild_a, age_elderly_a], urgency_emg_c))
    rulebase.addRule(T1_Rule([temp_low_a, headache_moderate_a, age_young_a], urgency_emg_c))
    rulebase.addRule(T1_Rule([temp_low_a, headache_moderate_a, age_adult_a], urgency_emg_c))
    rulebase.addRule(T1_Rule([temp_low_a, headache_moderate_a, age_elderly_a], urgency_emg_c))
    rulebase.addRule(T1_Rule([temp_low_a, headache_severe_a, age_young_a], urgency_emg_c))
    rulebase.addRule(T1_Rule([temp_low_a, headache_severe_a, age_adult_a], urgency_emg_c))
    rulebase.addRule(T1_Rule([temp_low_a, headache_severe_a, age_elderly_a], urgency_emg_c))

    # 1.2. IF Temp IS High THEN Urgency IS Emergency (9 Rules)
    rulebase.addRule(T1_Rule([temp_high_a, headache_mild_a, age_young_a], urgency_emg_c))
    rulebase.addRule(T1_Rule([temp_high_a, headache_mild_a, age_adult_a], urgency_emg_c))
    rulebase.addRule(T1_Rule([temp_high_a, headache_mild_a, age_elderly_a], urgency_emg_c))
    rulebase.addRule(T1_Rule([temp_high_a, headache_moderate_a, age_young_a], urgency_emg_c))
    rulebase.addRule(T1_Rule([temp_high_a, headache_moderate_a, age_adult_a], urgency_emg_c))
    rulebase.addRule(T1_Rule([temp_high_a, headache_moderate_a, age_elderly_a], urgency_emg_c))
    rulebase.addRule(T1_Rule([temp_high_a, headache_severe_a, age_young_a], urgency_emg_c))
    rulebase.addRule(T1_Rule([temp_high_a, headache_severe_a, age_adult_a], urgency_emg_c))
    rulebase.addRule(T1_Rule([temp_high_a, headache_severe_a, age_elderly_a], urgency_emg_c))

    # ==============================================================================
    # 2. NORMAL TEMPERATURE RULES (TempNormal)
    # ==============================================================================

    # 2.1. IF Temp IS Normal AND Headache IS Mild
    rulebase.addRule(T1_Rule([temp_normal_a, headache_mild_a, age_young_a], urgency_std_c))
    rulebase.addRule(T1_Rule([temp_normal_a, headache_mild_a, age_adult_a], urgency_std_c))
    rulebase.addRule(T1_Rule([temp_normal_a, headache_mild_a, age_elderly_a], urgency_std_c))

    # 2.2. IF Temp IS Normal AND Headache IS Moderate
    rulebase.addRule(T1_Rule([temp_normal_a, headache_moderate_a, age_young_a], urgency_urg_c))
    rulebase.addRule(T1_Rule([temp_normal_a, headache_moderate_a, age_adult_a], urgency_std_c))
    rulebase.addRule(T1_Rule([temp_normal_a, headache_moderate_a, age_elderly_a], urgency_urg_c))

    # 2.3. IF Temp IS Normal AND Headache IS Severe
    rulebase.addRule(T1_Rule([temp_normal_a, headache_severe_a, age_young_a], urgency_urg_c))
    rulebase.addRule(T1_Rule([temp_normal_a, headache_severe_a, age_adult_a], urgency_urg_c))
    rulebase.addRule(T1_Rule([temp_normal_a, headache_severe_a, age_elderly_a], urgency_urg_c))


    patient_age_input.setInput(age_val)
    headache_severity_input.setInput(headache_val)
    patient_temperature_input.setInput(temp_val)
    patient_urgency_output.setDiscretisationLevel(100)

    output_dict = rulebase.evaluate(1)
    urgency_value = output_dict[patient_urgency_output]

    print(f"\nDefuzzified Patient Urgency: {urgency_value:.2f}")

    fig, axes = plt.subplots(3,1, figsize=(10,10))

    
    axes[0].set_title("Age Membership Degrees")
    x_vals = np.linspace(0,130,400)
    for mf in [age_young, age_adult, age_elderly]:
        axes[0].plot(x_vals, [mf.getFS(x) for x in x_vals], label=mf.getName())
    axes[0].axvline(age_val, color='red', linestyle='--')
    axes[0].legend()

    
    axes[1].set_title("Headache Severity Membership Degrees")
    x_vals = np.linspace(0,10,400)
    for mf in [headache_mild, headache_moderate, headache_severe]:
        axes[1].plot(x_vals, [mf.getFS(x) for x in x_vals], label=mf.getName())
    axes[1].axvline(headache_val, color='red', linestyle='--')
    axes[1].legend()

    
    axes[2].set_title("Temperature Membership Degrees")
    x_vals = np.linspace(30,45,400)
    for mf in [temp_low, temp_normal, temp_high]:
        axes[2].plot(x_vals, [mf.getFS(x) for x in x_vals], label=mf.getName())
    axes[2].axvline(temp_val, color='red', linestyle='--')
    axes[2].legend()

   
    fig2, ax = plt.subplots(figsize=(10,5))
    ax.set_title("Urgency Output MFs with Aggregated Fuzzy Set")

    x_vals = np.linspace(0,100,500)


    for mf in [urgency_standard, urgency_urgent, urgency_emergency]:
        ax.plot(x_vals, [mf.getFS(x) for x in x_vals], label=mf.getName(), linewidth=2)

   
    aggregated = np.zeros_like(x_vals)

    for rule in rulebase.getRules():
        for cons in rule.getConsequents():
            mf = cons.getMF()
            alpha = rule.getFStrength(1)

            clipped = np.array([min(mf.getFS(x), alpha) for x in x_vals])
            aggregated = np.maximum(aggregated, clipped)

    ax.fill_between(x_vals, 0, aggregated, color="blue", alpha=0.3, label="Aggregated Fuzzy Set", linewidth=2)
    ax.plot(x_vals, aggregated, color="red", linewidth=2.5, linestyle='--', label="Aggregated MF Boundary")

    ax.plot([urgency_value], [0], marker='o', markersize=10, color='purple',
            label=f"Defuzzified = {urgency_value:.2f}", zorder=5)
    
    ax.axvline(urgency_value, color='purple', linestyle='--', alpha=0.7)
    ax.axhline(0, color='black', linewidth=0.8)

    ax.set_xlabel("Urgency Score")
    ax.set_ylabel("Membership")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    return urgency_value


def main():
   
    try:
        age_val = float(input("Enter patient age (0–130): "))
        headache_val = float(input("Enter headache severity (0–10): "))
        temp_val = float(input("Enter temperature (30–45 °C): "))

        urgency_value = perform_fls_case1(age_val, headache_val, temp_val)
        print(f"\nFinal Defuzzified Urgency = {urgency_value:.2f}")

    except ValueError as e:
        print(f"Invalid input: {e}")


if __name__ == "__main__":
    main()

