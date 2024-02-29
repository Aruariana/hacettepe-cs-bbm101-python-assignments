import os

# Ömer Kayra Çetin
# b2210356060

# Environmental Variables
CURRENT_DIR_PATH = os.getcwd()
INPUT_FILE_NAME = "doctors_aid_inputs.txt"
INPUT_FILE_PATH = os.path.join(CURRENT_DIR_PATH, INPUT_FILE_NAME)
OUTPUT_FILE_NAME = "doctors_aid_outputs.txt"
OUTPUT_FILE_PATH = os.path.join(CURRENT_DIR_PATH, OUTPUT_FILE_NAME)
# Global Variables
patient_data = []  # This is the multidimensional built-in python list.


def read_input():
    with open(INPUT_FILE_PATH, "r", encoding="utf-8") as file:  # Used encoding utf-8 to represent turkish letters.
        data = file.readlines()
    for i in range(len(data)):
        data[i] = data[i].replace("\n", "")  # Got rid of new line characters in lines.
    return data


def write_output(output):
    with open(OUTPUT_FILE_PATH, "a") as file:
        file.write(output)


def create(line_of_input_data):
    global patient_data
    # Split the line into two parts, command and patient info.
    # Take the patient info and split it from commas to get the info one by one in a list.
    current_patient_info = line_of_input_data.split(" ", 1)[1].split(", ")
    patient_name = current_patient_info[0]
    for patient in patient_data:
        if patient[0] == patient_name:
            return "Patient {} cannot be recorded due to duplication.\n".format(patient_name)
    patient_data.append(current_patient_info)
    return "Patient {} is recorded.\n".format(patient_name)


def remove(name):
    for patient in patient_data:
        if patient[0] == name:
            patient_data.remove(patient)
            return "Patient {} is removed.\n".format(name)
    return "Patient {} cannot be removed due to absence.\n".format(name)


def list_patients():
    line1 = "Patient Diagnosis\tDisease\t\t\tDisease\t\tTreatment\t\tTreatment\n"
    line2 = "Name\tAccuracy\tName\t\t\tIncidence\tName\t\t\tRisk\n"
    line3 = "-------------------------------------------------------------------------\n"
    write_output(line1)
    write_output(line2)
    write_output(line3)

    # Defining a liner function to line the words to correct spots.
    # Adds tab to string until it reaches its designed character number.
    def liner(string, length):
        space_needed = length - len(string)
        while space_needed > 0:
            string += "\t"
            space_needed -= 4
        return string

    for patient in patient_data:
        patient_lines = ""
        patient_copy = patient.copy()  # Creating a copy in order not to mess with my actual data.
        # Get diagnosis accuracy to the wanted format.
        patient_copy[1] = format(float(patient[1])*100, ".2f")+"%"
        # Get treatment risk to the wanted format.
        patient_copy[5] = str(round(float(patient[5])*100))+"%"
        for i in range(len(patient)):
            # Check the index to correctly line the new line.
            if i == 0:
                patient_copy[0] = liner(patient_copy[0], 8)
            elif i == 1:
                patient_copy[1] = liner(patient_copy[1], 12)
            elif i == 2:
                patient_copy[2] = liner(patient_copy[2], 16)
            elif i == 3:
                patient_copy[3] = liner(patient_copy[3], 12)
            elif i == 4:
                patient_copy[4] = liner(patient_copy[4], 16)
            elif i == 5:
                patient_copy[5] = patient_copy[5] + "\n"
            # With every iteration add the newly created line to patient lines.
            patient_lines += patient_copy[i]
        write_output(patient_lines)


def probability(name):
    for patient in patient_data:
        if patient[0] == name:
            cancer_people = int(patient[3].split("/")[0])  # Get the numerator in disease incidence.
            whole_population = int(patient[3].split("/")[1])  # Get the denominator in disease incidence.
            misdiagnose_percentage = 100 - round(float(patient[1])*100, 2)  # Calculate wrong diagnose percentage.
            # Make the necessary calculations to find the disease probability percentage.
            probability_percentage = (cancer_people/((whole_population*misdiagnose_percentage)/100+cancer_people))*100
            probability_percentage = round(probability_percentage, 2)  # Round it to two decimal places
            if probability_percentage == int(probability_percentage):  # Drop the zeros in the decimal part
                probability_percentage = int(probability_percentage)
            # Make the return statement a list of two elements because recommendation function
            # Will need cancer probability percentage as a float, as in the second element.
            return ["Patient {} has a probability of {}% of having {}.\n".format(
                name, probability_percentage, patient[2].lower()), probability_percentage]
    return ["Probability for {} cannot be calculated due to absence.\n".format(name)]


def recommendation(name):
    for patient in patient_data:
        if patient[0] == name:
            treatment_risk = float(patient[5])*100  # Get treatment risk in a percentage form.
            cancer_percentage = probability(name)[1]  # Get percentage of cancer probability from probability function.
            if treatment_risk > cancer_percentage:
                return "System suggests {} NOT to have the treatment.\n".format(name)
            else:
                return "System suggests {} to have the treatment.\n".format(name)
    return "Recommendation for {} cannot be calculated due to absence.\n".format(name)


input_data = read_input()

for line in input_data:
    command = line.split(" ", 1)[0]  # Seperate commands as they are the first word a line has.
    # Check commands to use the right functions with their right inputs.
    if command == "create":
        write_output(create(line))
    elif command == "remove":
        write_output(remove(line.split()[1]))
    elif command == "probability":
        # Probability function returns lists as outputs due to its usage in recommendation function.
        # So we just need the zero index elements in both of its outputs.
        write_output(probability(line.split()[1])[0])
    elif command == "recommendation":
        write_output(recommendation(line.split()[1]))
    elif command == "list":
        list_patients()
