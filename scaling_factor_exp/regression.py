import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import datetime
from scipy.optimize import curve_fit

def drawing_graph(x, y, name: str):
    x_np = np.array(x).reshape(-1, 1)
    y_np = np.array(y)
    
    reg = LinearRegression().fit(x_np[1:6], y_np[1:6])
    predicted_y = reg.predict(x_np)
    m, b = reg.coef_[0], reg.intercept_

    def combined_model(x, C, a, d):
        linear_part = m*x+b
        return C / (1 + np.exp(-a * (x - d)))
#         return linear_part + (C-linear_part) * (1-np.exp(-a*(x-d)))
    
    params, covariance = curve_fit(combined_model, x_np.flatten(), y_np, p0=[max(y_np), 1, np.mean(x_np)], maxfev=50000)

    # ploting!
    plt.figure(dpi=300)
    plt.axhline(params[0], color='gray', alpha=0.5, linestyle='--')
    plt.scatter(x_np, y_np, color='red', marker='x', label='Data points')
    plt.plot(x_np, predicted_y, color='blue', label='Linear regression')
    plt.plot(np.array([i for i in range(0,65)]), combined_model(np.array([i for i in range(0,65)]), *params), color='green', label='Fitted Model')
    plt.xlim(1,65)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.title(f'Regression {name}')

    # make images
    current_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    filename = f"{current_time}.png"
    plt.savefig(filename, format='png')
    # plt.show()

    m = reg.coef_[0]
    b = reg.intercept_ 

    print(f"Linear regression equation: Y = {m:.4f}X + {b:.4f}")
    print(f"Parameters: C={params[0]}, a={params[1]}, d={params[2]}")

    y_pred = combined_model(x_np.flatten(), *params)
    SS_res = np.sum((y_np - y_pred) ** 2)
    SS_tot = np.sum((y_np - np.mean(y_np)) ** 2)
    r_squared = 1 - (SS_res / SS_tot)
    mse = np.mean((y_np - y_pred) ** 2)

    print(f"R^2 for the combined model: {r_squared:.4f}")
    print(f"MSE for the combined model: {mse:.4f}")


x = [1,2,4,8,12,16,20,24,28,32]

y1 = [1,
1.543563477,
2.611500242,
4.44203444,
6.036262578,
7.838882621,
9.373377966,
10.62302447,
12.25985739,
13.14976249,
]

y2 = [1,
1.819143677,
3.008615153,
5.0179522,
6.731799077,
8.427746206,
10.05767383,
11.34228815,
13.40979828,
13.77542623,
]


y3 = [1,
1.743289057,
2.484011722,
3.759779167,
5.188109816,
6.459267881,
7.291238585,
8.954169511,
10.75390126,
10.79036229,
]
drawing_graph(x,y1,'(ResNet18)')
drawing_graph(x,y2,'(ResNet152)')
drawing_graph(x,y3,'(Efficient-V2L)')