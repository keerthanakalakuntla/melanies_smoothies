import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Title and Description
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

# Input for name
name_on_order = st.text_input("Name on smoothie:")
st.write("The Name on your Smoothie will be:", name_on_order)

# Snowflake Session and Data Retrieval
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Extract fruit names into a list
fruit_list = my_dataframe.to_pandas()['FRUIT_NAME'].tolist()

# Multiselect for ingredients
ingredients_list = st.multiselect('Choose up to 5 ingredients:', fruit_list , max_selections=6)

if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)
    st.write("Selected Ingredients:", ingredients_list)

    # SQL Insert Statement
    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders(ingredients, name_on_order)
    VALUES ('{ingredients_string}', '{name_on_order}')
    """

    st.write("SQL Query:", my_insert_stmt)

    # Order submission
    time_to_insert = st.button('Submit Order')

if time_to_insert:
    # Use parameterized query to safely insert data
    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders(ingredients, name_on_order)
    VALUES ('{ingredients_string}', '{name_on_order}')
    """
    
    # Execute the insert statement
    session.sql(my_insert_stmt).collect()

    # Display confirmation message
    st.success(f'✅ Your Smoothie is ordered, {name_on_order}!')
