import matplotlib.pyplot as plt


def CheckNoEmpty(df,name):
    if name in df:
        return 0
    else:
        print("no Data")
        return 1



def plot_quaternion(data,namefile) -> None :

    #check if empty
    boolcheck = CheckNoEmpty(data,"quatx")
    if boolcheck == 1:
        return None

    # Create a 2x2 subplot layout
    fig, axs = plt.subplots(4, 1, figsize=(10, 15))  # Adjust the values as needed for width and height of each subplot

    # Plot DataFrame 1 in the first subplot
    # axs[0].plot( data["quatx_imu"],label="imu",c = "blue")

    d = data["quatx"].values
    axs[0].plot( d,label="opti",c="red",linestyle=':')

    d = data["quatx_filter"].values
    axs[0].plot( d,label="opti_filter",c="orange",linestyle='--')

    axs[0].set_title('Quaternion x')

    # Plot DataFrame 2 in the first subplot
    # axs[1].plot( data["quay_imu"],label="imu",c = "blue")

    d = data["quaty"].values
    axs[1].plot( d,label="opti",c="red",linestyle=':')

    d = data["quaty_filter"].values
    axs[1].plot( d,label="opti_filter",c="orange",linestyle='--')

    axs[1].set_title('Quaternion y')

    # Plot DataFrame 3 in the first subplot
    # axs[2].plot( data["quatz_imu"],label="imu",c = "blue")

    d = data["quatz"].values
    axs[2].plot( d,label="opti",c="red",linestyle=':')

    d = data["quatz_filter"].values
    axs[2].plot( d,label="opti_filter",c="orange",linestyle='--')

    axs[2].set_title('Quaternion z')

    # Plot DataFrame 4 in the first subplot
    # axs[3].plot( data["quatw_imu"],label="imu",c = "blue")

    d = data["quatw"].values
    axs[3].plot( d,label="opti",c="red",linestyle=':')

    d = data["quatw_filter"].values
    axs[3].plot( d,label="opti_filter",c="orange",linestyle='--')

    axs[3].set_title('Quaternion w')

    plt.legend()

    # Adjust layout to prevent overlapping titles
    plt.tight_layout()

    # Display the plot
    plt.savefig("../data/plots/quaternion_" + namefile)


def plot_angularVelocity(data,namefile) -> None :

    #check if empty
    boolcheck = CheckNoEmpty(data,"wx")
    if boolcheck == 1:
        return None


    # Create a 2x2 subplot layout
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))  # Adjust the values as needed for width and height of each subplot

    # Plot DataFrame 1 in the first subplot
    # axs[0].plot( data["quatx_imu"],label="imu",c = "blue")

    d = data["wx"].values
    axs[0].plot( d,label="opti",c="red",linestyle=':')
    axs[0].plot( data["wx_filter"].values, label="opti_filter",c="blue")
    #axs[0].plot( data["wx_euler"].values, label="euler",c="orange",linestyle='--')

    axs[0].set_title('angular Velocity x')

    # Plot DataFrame 2 in the first subplot
    # axs[1].plot( data["quay_imu"],label="imu",c = "blue")

    d = data["wy"].values
    axs[1].plot( d,label="opti",c="red",linestyle=':')
    axs[1].plot( data["wy_filter"].values, label="opti_filter",c="blue")
    #axs[1].plot( data["wy_euler"].values, label="euler",c="orange",linestyle='--')



    axs[1].set_title('angular Velocity y')

    # Plot DataFrame 3 in the first subplot
    # axs[2].plot( data["quatz_imu"],label="imu",c = "blue")

    d = data["wz"].values
    axs[2].plot( d,label="opti",c="red",linestyle=':')
    axs[2].plot( data["wz_filter"].values, label="opti_filter",c="blue")
    #axs[2].plot( data["wz_euler"].values, label="euler",c="orange",linestyle='--')


    axs[2].set_title('angular Velocity z')



    plt.legend()

    # Adjust layout to prevent overlapping titles
    plt.tight_layout()

    # Display the plot
    plt.savefig("../data/plots/Angular_vel_" + namefile)

def plot_position(data,namefile) -> None :


    #check if empty
    boolcheck = CheckNoEmpty(data,"posx")
    if boolcheck == 1:
        return None
    
    # Create a 2x2 subplot layout
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))  # Adjust the values as needed for width and height of each subplot

    # Plot DataFrame 1 in the first subplot
    # axs[0].plot( data["quatx_imu"],label="imu",c = "blue")

    d = data["posx"].values
    axs[0].plot( d,label="opti",c="red",linestyle=':')

    axs[0].set_title('Position x')

    # Plot DataFrame 2 in the first subplot
    # axs[1].plot( data["quay_imu"],label="imu",c = "blue")

    d = data["posy"].values
    axs[1].plot( d,label="opti",c="red",linestyle=':')


    axs[1].set_title('Position y')

    # Plot DataFrame 3 in the first subplot
    # axs[2].plot( data["quatz_imu"],label="imu",c = "blue")

    d = data["posz"].values
    axs[2].plot( d,label="opti",c="red",linestyle=':')

    axs[2].set_title('Position z')



    plt.legend()

    # Adjust layout to prevent overlapping titles
    plt.tight_layout()

    # Display the plot
    plt.savefig("../data/plots/position_" + namefile)

def plot_euler(data,namefile) -> None :

    #check if empty
    boolcheck = CheckNoEmpty(data,"eulerx")
    if boolcheck == 1:
        return None
    
    # Create a 2x2 subplot layout
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))  # Adjust the values as needed for width and height of each subplot

    # Plot DataFrame 1 in the first subplot
    # axs[0].plot( data["quatx_imu"],label="imu",c = "blue")

    d = data["eulerx"].values
    axs[0].plot( d,label="opti",c="red",linestyle=':')
    axs[0].plot( data["eulerx_filter"].values, label="euler_filter",c="orange",linestyle='--')


    axs[0].set_title('euler x')

    # Plot DataFrame 2 in the first subplot
    # axs[1].plot( data["quay_imu"],label="imu",c = "blue")

    d = data["eulery"].values
    axs[1].plot( d,label="opti",c="red",linestyle=':')
    axs[1].plot( data["eulery_filter"].values, label="euler_filter",c="orange",linestyle='--')


    axs[1].set_title('euler y')

    # Plot DataFrame 3 in the first subplot
    # axs[2].plot( data["quatz_imu"],label="imu",c = "blue")

    d = data["eulerz"].values
    axs[2].plot( d,label="opti",c="red",linestyle=':')
    axs[2].plot( data["eulerz_filter"].values, label="euler_filter",c="orange",linestyle='--')

    axs[2].set_title('euler z')



    plt.legend()

    # Adjust layout to prevent overlapping titles
    plt.tight_layout()

    # Display the plot
    plt.savefig("../data/plots/euler_" + namefile)


def plot_force(data,namefile) -> None :

    #check if empty
    boolcheck = CheckNoEmpty(data,"forcex")
    if boolcheck == 1:
        return None
    
    # Create a 2x2 subplot layout
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))  # Adjust the values as needed for width and height of each subplot

    # Plot DataFrame 1 in the first subplot
    # axs[0].plot( data["quatx_imu"],label="imu",c = "blue")

    d = data["forcex"].values
    axs[0].plot( d,label="Force",c="red",linestyle=':')
    axs[0].plot( data["forcex_filter"].values, label="force_filter",c="orange",linestyle='--')


    axs[0].set_title('Force x')

    # Plot DataFrame 2 in the first subplot
    # axs[1].plot( data["quay_imu"],label="imu",c = "blue")

    d = data["forcey"].values
    axs[1].plot( d,label="Force",c="red",linestyle=':')
    axs[1].plot( data["forcey_filter"].values, label="force_filter",c="orange",linestyle='--')


    axs[1].set_title('Force y')

    # Plot DataFrame 3 in the first subplot
    # axs[2].plot( data["quatz_imu"],label="imu",c = "blue")

    d = data["forcez"].values
    axs[2].plot( d,label="Force",c="red",linestyle=':')
    axs[2].plot( data["forcez_filter"].values, label="force_filter",c="orange",linestyle='--')

    axs[2].set_title('Force z')



    plt.legend()

    # Adjust layout to prevent overlapping titles
    plt.tight_layout()

    # Display the plot
    plt.savefig("../data/plots/force_" + namefile)


def plot_torque(data,namefile) -> None :

    #check if empty
    boolcheck = CheckNoEmpty(data,"torquex")
    if boolcheck == 1:
        return None
    
    # Create a 2x2 subplot layout
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))  # Adjust the values as needed for width and height of each subplot

    # Plot DataFrame 1 in the first subplot
    # axs[0].plot( data["quatx_imu"],label="imu",c = "blue")

    d = data["torquex"].values
    axs[0].plot( d,label="Torque",c="red",linestyle=':')
    axs[0].plot( data["torquex_filter"].values, label="torquex_filter",c="orange",linestyle='--')


    axs[0].set_title('Torque x')

    # Plot DataFrame 2 in the first subplot
    # axs[1].plot( data["quay_imu"],label="imu",c = "blue")

    d = data["torquey"].values
    axs[1].plot( d,label="Torque",c="red",linestyle=':')
    axs[1].plot( data["torquey_filter"].values, label="torque_filter",c="orange",linestyle='--')


    axs[1].set_title('Torque y')

    # Plot DataFrame 3 in the first subplot
    # axs[2].plot( data["quatz_imu"],label="imu",c = "blue")

    d = data["torquez"].values
    axs[2].plot( d,label="Torque",c="red",linestyle=':')
    axs[2].plot( data["torquez_filter"].values, label="torque_filter",c="orange",linestyle='--')

    axs[2].set_title('Torque z')



    plt.legend()

    # Adjust layout to prevent overlapping titles
    plt.tight_layout()

    # Display the plot
    plt.savefig("../data/plots/torque_" + namefile)

def plot_path(data,namefile) -> None :

# Sample data
    z = data["posz"].values

    y = data["posy"].values

    # Create a color gradient from red to blue
    colors = np.linspace(0, 1, len(z))
    cmap = plt.get_cmap('coolwarm')

    # Plot the scatter plot with changing colors
    for i in range(len(x)):
        plt.scatter(z[i], y[i], c=cmap(colors[i]), label=f'Data Point {i+1}')

    # Add labels and a legend
    plt.xlabel('z-axis')
    plt.ylabel('Y-axis')
    plt.legend()
    # Adjust layout to prevent overlapping titles
    plt.tight_layout()

    # Display the plot
    plt.savefig("../data/plots/path_" + namefile)
    # Show the plot
"""def plot_all(data):
    plot_angularVelocity(data)
    plot_quaternion(data)

if __name__ == "__main__":
    plot_all(data)"""
