import streamlit as st
import plotly.graph_objects as go


# Function to calculate the cumulative probabilities
def cumulative_probabilities(dice_sides, target_number, max_rolls=10, cache={}):
    # Check if the probability is already in the cache
    if (max_rolls, target_number) in cache:
        return cache[(max_rolls, target_number)]

    # Initialize the probability array
    probabilities = [[0] * (target_number + 1) for _ in range(max_rolls + 1)]

    # Base case: after 1 roll
    for i in range(1, dice_sides + 1):
        if i <= target_number:
            probabilities[1][i] = 1 / dice_sides

    # Dynamic programming: compute probabilities for 2 to max_rolls rolls
    for roll in range(2, max_rolls + 1):
        for total in range(1, target_number + 1):
            for face in range(1, dice_sides + 1):
                if total - face > 0:
                    probabilities[roll][total] += probabilities[roll - 1][total - face] / dice_sides

    # Sum the probabilities for achieving the target in up to max_rolls
    win_probability = sum(probabilities[roll][target_number] for roll in range(1, max_rolls + 1))
    partial_win_probability = 0
    for roll in range(1, max_rolls + 1):
        if 0 < target_number - 1 < len(probabilities[roll]):
            partial_win_probability += probabilities[roll][target_number - 1]
        if 0 < target_number + 1 <= dice_sides and target_number + 1 < len(probabilities[roll]): 
            partial_win_probability += probabilities[roll][target_number + 1]

    # Store the probability in the cache
    cache[(max_rolls, target_number)] = (win_probability, partial_win_probability)

    return win_probability, partial_win_probability

def cumulative_probabilities_cdf(dice_sides, target_number, max_rolls=10):
    probabilities = [[0] * (target_number + 1) for _ in range(max_rolls + 1)]
    for i in range(1, min(dice_sides, target_number) + 1):
        probabilities[1][i] = 1 / dice_sides

    for roll in range(2, max_rolls + 1):
        for total in range(1, target_number + 1):
            for face in range(1, min(dice_sides, total) + 1):
                probabilities[roll][total] += probabilities[roll - 1][total - face] / dice_sides

    cdf = [sum(probabilities[roll][i] for roll in range(1, max_rolls + 1)) for i in range(target_number + 1)]
    return cdf

def plot_cdf_with_plotly(dice_sides, max_target, max_rolls):
    cdf_values = [cumulative_probabilities_cdf(dice_sides, target, max_rolls)[-1] for target in range(1, max_target + 1)]
    fig = go.Figure(data=go.Scatter(x=list(range(1, max_target + 1)), y=cdf_values, mode='lines+markers'))
    fig.update_layout(
        title=f'Cumulative Distribution Function up to Target {max_target}',
        xaxis_title='Target Score',
        yaxis_title='Cumulative Probability',
        margin=dict(l=40, r=40, t=40, b=30)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    
# Initialize session state for previous probabilities if not already done
if 'prev_win_probability' not in st.session_state:
    st.session_state['prev_win_probability'] = 0
if 'prev_partial_win_probability' not in st.session_state:
    st.session_state['prev_partial_win_probability'] = 0
if 'prev_loss_probability' not in st.session_state:
    st.session_state['prev_loss_probability'] = 1  # Initially, loss is certain without any roll


##################################################################################################################
# Site Layout
##################################################################################################################

st.sidebar.title("Dice Probability Calculator")

# Create an input for the target number
st.sidebar.number_input("Target number", min_value=1, key="target_number", value=25)

# Create a select slider for the number of sides on the dice
st.sidebar.select_slider("Number of sides on the dice", options=[4, 6, 8, 10, 12, 20], value=6, key="dice_sides")

# Create an input for the maximum number of rolls
st.sidebar.slider("Maximum number of rolls", min_value=1, max_value=100, key="max_rolls", value=10)


# Get the values from the sidebar
dice_sides = st.session_state.dice_sides
target_number = st.session_state.target_number
max_rolls = st.session_state.max_rolls

st.sidebar.caption(f"Maximum possible target number is {dice_sides * max_rolls}")

st.sidebar.write("""
### Game Rules

The game is played by rolling a dice with a certain number of sides. The objective is as follows:

- **Win**: The sum of the dice rolls is **equal** to the target number.
- **Partial Win**: The sum of the dice rolls is **one less or one more** than the target number.
- **Lose**: In all other cases, where the sum is not equal to, one less, or one more than the target number.
""")

# Input Validation
if target_number > dice_sides * max_rolls or target_number < dice_sides:
    st.error(f"The target number should be more than the dice size and not exceed the possible bounds for a {dice_sides}-sided dice with a maximum of {max_rolls} rolls.")
    st.stop()


# Calculate the probabilities
win_probability, partial_win_probability = cumulative_probabilities(dice_sides, target_number, max_rolls)

# Calculate loss probability
loss_probability = 1 - win_probability - partial_win_probability

# Calculate deltas
delta_win = win_probability - st.session_state['prev_win_probability']
delta_partial_win = partial_win_probability - st.session_state['prev_partial_win_probability']
delta_loss = loss_probability - st.session_state['prev_loss_probability']

# Update session state with current probabilities for next iteration
st.session_state['prev_win_probability'] = win_probability
st.session_state['prev_partial_win_probability'] = partial_win_probability
st.session_state['prev_loss_probability'] = loss_probability

# Display cumulative distribution function of the probabilities
st.header("Chances of Hitting Target Scores with Rolls")

plot_cdf_with_plotly(dice_sides, target_number, max_rolls)

# Divider
st.write("---")

# Display probabilities in columns as a metric with delta

col1, col2, col3 = st.columns(3)
col1Container = col1.container(border=True)
col2Container = col2.container(border=True)
col3Container = col3.container(border=True)

col1Container.metric("Win Probability", f"{win_probability:.6f}", delta=f"{delta_win:.6f}")
col2Container.metric("Partial Win Probability", f"{partial_win_probability:.6f}", delta=f"{delta_partial_win:.6f}")
col3Container.metric("Loss Probability", f"{loss_probability:.6f}", delta=f"{delta_loss:.6f}")
    

    
    
    
    
    
    