import streamlit as st
from snowflake.snowpark.functions import col
import requests


# Title and Description
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

# Input for name
name_on_order = st.text_input("Name on smoothie:")
st.write("The Name on your Smoothie will be:", name_on_order)

# Snowflake Session and Data Retrieval
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Extract fruit names into a list
fruit_list = my_dataframe.to_pandas()['FRUIT_NAME'].tolist()

# Multiselect for ingredients
ingredients_list = st.multiselect('Choose up to 5 ingredients:', fruit_list, max_selections=5)

# Define `time_to_insert` with a default value to avoid NameError
time_to_insert = False

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + 'Nutrition Information')
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    st.write("Selected Ingredients:", ingredients_list)

    # SQL Insert with parameterized query
    stmt = """
    INSERT INTO smoothies.public.orders(ingredients, name_on_order)
    VALUES (?, ?)
    """

    time_to_insert = st.button('Submit Order')

# Execute the SQL query safely with parameterized query
if time_to_insert:
    session.sql(stmt, [ingredients_string.strip(), name_on_order]).collect()
    st.success(f'✅ Your Smoothie is ordered, {name_on_order}!')
