import streamlit as st
import pandas as pd

# Initialize session state for budgets and expenses
if 'budgets' not in st.session_state:
    st.session_state.budgets = pd.DataFrame(columns=['Category', 'Budget'])
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=['Date', 'Category', 'Description', 'Amount'])

st.title('Expense Budget Planner')

# Add Budget Form
st.subheader('Set Budget Goals')
with st.form(key='budget_form'):
    category = st.text_input('Category')
    budget_amount = st.number_input('Budget Amount', min_value=0.01, format='%.2f')

    submit_budget = st.form_submit_button('Add Budget')
    if submit_budget:
        new_budget = pd.DataFrame([[category, budget_amount]], columns=['Category', 'Budget'])
        st.session_state.budgets = pd.concat([st.session_state.budgets, new_budget], ignore_index=True)
        st.success('Budget added successfully!')

# Add Expense Form
st.subheader('Log Expenses')
with st.form(key='expense_form'):
    date = st.date_input('Date')
    expense_category = st.selectbox('Category', st.session_state.budgets['Category'].tolist())
    description = st.text_input('Description')
    amount = st.number_input('Amount', min_value=0.01, format='%.2f')

    submit_expense = st.form_submit_button('Add Expense')
    if submit_expense:
        new_expense = pd.DataFrame([[date, expense_category, description, amount]], columns=['Date', 'Category', 'Description', 'Amount'])
        st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)
        st.success('Expense added successfully!')

# Display Budgets and Expenses
st.subheader('Budgets')
st.dataframe(st.session_state.budgets)

st.subheader('Expenses')
st.dataframe(st.session_state.expenses)

# Calculate and Display Budget vs Spending
st.subheader('Budget Summary')
if not st.session_state.budgets.empty and not st.session_state.expenses.empty:
    summary = st.session_state.budgets.copy()
    summary['Spent'] = summary['Category'].apply(lambda x: st.session_state.expenses[st.session_state.expenses['Category'] == x]['Amount'].sum())
    summary['Remaining'] = summary['Budget'] - summary['Spent']
    summary['Spent'] = summary['Spent'].fillna(0)  # Fill NaN values with 0

    st.dataframe(summary)
else:
    st.write('Please add some budgets and expenses to see the summary.')




