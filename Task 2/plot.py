import matplotlib.pyplot as plt


def graph_simulation(sheep_list, wolf):
    plt.figure(figsize=(12, 8))
    x_sheep, y_sheep = [], []
    for sheep in sheep_list:
        if sheep.is_alive:
            x_sheep.append(sheep.x_pos)
            y_sheep.append(sheep.y_pos)
    plt.scatter(x_sheep, y_sheep, marker='o', color='red', label='Sheep',s=50)
    plt.scatter(wolf.x_pos, wolf.y_pos, marker='x', color='blue', label='Wolf',s=100)
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.tight_layout()
    plt.show()