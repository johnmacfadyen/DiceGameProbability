# Dice Roll Probability Calculator

This Streamlit app calculates the probabilities of winning, partially winning, and losing a dice game based on the sum of dice rolls. It also visualizes the cumulative distribution function (CDF) for achieving at least a certain score within a specified number of rolls.

## Overview

The app allows users to select the number of sides on the dice, a target number, and the maximum number of rolls. It calculates the probability of:

- **Winning**: Achieving exactly the target sum with the dice rolls.
- **Partial Winning**: Achieving a sum one less or one more than the target.
- **Losing**: Not achieving the target or partial win conditions.

Additionally, the app provides a Plotly graph that shows the cumulative probability of achieving at least each possible score up to the selected target number.

## Features

- Interactive sliders and inputs for customizing game parameters.
- Calculation of win, partial win, and loss probabilities.
- Visualization of the cumulative distribution function (CDF) using Plotly for an interactive experience.
- Explanation of game rules for easy understanding by new users.

## How to Run

1. Ensure you have Python and pip installed on your system.
2. Clone this repository to your local machine.
3. Install the required dependencies:

    ```bash
    pip install streamlit plotly
    ```

4. Run the Streamlit app:

    ```bash
    streamlit run main.py
    ```

## Contributing

Contributions are welcome! If you have suggestions for improving the app, please open an issue or submit a pull request.

## License

[MIT License](LICENSE)

Feel free to use this project as you like. If you use it for educational purposes or build on it, I'd love to hear about your projects!

