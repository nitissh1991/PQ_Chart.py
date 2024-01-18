import matplotlib.pyplot as plt

data = {
    "0.95": {"P": [], "Q": []},
    "1": {"P": [], "Q": []},
    "1.05": {"P": [], "Q": []}
}

with open("4.PQ_Output.txt", "r") as file:
    for line in file:
        parts = line.strip().split(",")
        power_factor = parts[2]
        p_value = float(parts[6].split()[-1])
        q_value = float(parts[8].split()[-1])
        data[power_factor]["P"].append(p_value)
        data[power_factor]["Q"].append(q_value)

    # Read data from the second file and update the 'data' dictionary
    with open("Reg.txt", "r") as file:
        for line in file:
            parts = line.strip().split(",")
            if parts[0] == 'Reg':
                p_value = float(parts[2])
                q_value = float(parts[4])
                power_factor = "Regulation"
                if power_factor not in data:
                    data[power_factor] = {"P": [], "Q": []}
                data[power_factor]["P"].append(p_value)
                data[power_factor]["Q"].append(q_value)

    for power_factor, values in data.items():
        P = values["P"]
        Q = values["Q"]

        # Sorting P values in ascending order from 0 to (P/2-1)
        ascending_data = sorted(zip(P[:len(P) // 2], Q[:len(Q) // 2]), key=lambda p: p[0])

        # Sorting P values in descending order from (P/2) to the end
        descending_data = sorted(zip(P[len(P) // 2:], Q[len(Q) // 2:]), key=lambda p: p[0], reverse=True)

        # Combining the sorted data
        sorted_data = ascending_data + descending_data

        P, Q = zip(*sorted_data)
        values["P"] = P
        values["Q"] = Q

    for power_factor, values in data.items():
        P = values["P"]
        Q = values["Q"]
        plt.plot(Q, P, label=f"PCC Voltage {power_factor}")

    plt.xlabel('Q (MVAR)')
    plt.ylabel('P (MW)')
    plt.title('PQ-Chart')
    plt.legend()
    plt.grid(True)
    plt.show()
