import matplotlib.pyplot as plt


class StatisticalAnalysis:

    def __init__(self, df_cleaned):
        self.df_cleaned = df_cleaned

    # functions for statistical analysis

    def plot_resistance_in_grid(self, df_cleaned):
        plt.figure()
        power = df_cleaned['Total Power']  # summed up Power1, Power2, and Power3 for each row
        current = df_cleaned['Total Current']  # summed Current1, Current2, and Current3

        # Scatter Plot
        plt.figure(figsize=(10, 6))
        plt.scatter(current, power, color='blue', alpha=0.5)
        plt.title('Power vs Current for August')
        plt.xlabel('Current (Amps)')
        plt.ylabel('Power (Watts)')
        plt.grid(True)
        plt.show()

    def plot_grid_consumption_rate(self, df_cleaned):
        plt.figure()
        # convert energy to kWHr by dividing summed up Power1, Power2, and Power3 for each row by 1000
        power = df_cleaned['Total Power']/1000
        energy = df_cleaned['Total Energy']  # summed instant Energy, instant Energy, and instant Energy

        # Scatter Plot
        plt.figure(figsize=(10, 6))
        plt.scatter(power, energy,  color='blue', alpha=0.5)
        plt.title('Power vs Energy for August')
        plt.xlabel('Energy (kWHr)')
        plt.ylabel('Power (Watts)')
        plt.grid(True)
        plt.show()

    def plot_acummulated_consumption_rate(self, df_cleaned):
        plt.figure()
        # convert energy to kWHr by dividing summed up Power1, Power2, and Power3 for each row by 1000
        power = df_cleaned['Total Power']/1000
        energy = df_cleaned['Accumulated Energy']  # summed instant Energy, instant Energy, and instant Energy

        # Scatter Plot
        plt.figure(figsize=(10, 6))
        plt.plot(energy, power,  color='black', alpha=0.5)
        plt.title('Power vs Accumulated Energy for August')
        plt.xlabel('Energy (kWHr)')
        plt.ylabel('Power (Watts)')
        plt.grid(True)
        plt.show()

    def plot_consumption(self, df_cleaned):
        plt.figure()
        # convert energy to kWHr by dividing summed up Power1, Power2, and Power3 for each row by 1000
        energy = df_cleaned['Total Energy']
        time = df_cleaned['Time']  # summed instant Energy, instant Energy, and instant Energy
        # Scatter Plot
        plt.figure(figsize=(10, 6))
        plt.plot(time, energy,  color='red', alpha=0.5)
        plt.title('Energy vs Time for August')


        plt.xticks(rotation=45)
        plt.xlabel('DateTime')
        plt.ylabel('Energy (kWHr)')
        plt.grid(True)
        plt.show()

    def plot_accumulated_consumption(self, df_cleaned):
        plt.figure()
        # convert energy to kWHr by dividing summed up Power1, Power2, and Power3 for each row by 1000
        energy = df_cleaned['Accumulated Energy']
        time = df_cleaned['Time']  # summed instant Energy, instant Energy, and instant Energy
        # Scatter Plot
        plt.figure(figsize=(10, 6))
        plt.plot(energy, time,  color='violet', alpha=0.5)
        plt.title('Accumulated Energy vs Time for August')
        plt.xlabel('Energy (kWHr)')
        plt.ylabel('DateTime')
        plt.grid(True)
        plt.show()
