import matplotlib.pyplot as plt

def plot_simulation(times, glucose, insulin, insulin_action):
    plt.figure(figsize=(12,6))

    plt.subplot(3,1,1)
    plt.plot(times, glucose)
    plt.ylabel('Glucose (mg/dL)')
    plt.title('Glucose over Time')

    plt.subplot(3,1,2)
    plt.plot(times, insulin)
    plt.ylabel('Insulin (uU/mL)')
    plt.title('Insulin over Time')

    plt.subplot(3,1,3)
    plt.plot(times, insulin_action)
    plt.ylabel('Insulin Action (X)')
    plt.xlabel('Time (minutes)')
    plt.title('Insulin Action over Time')

    plt.tight_layout()
    plt.show()
