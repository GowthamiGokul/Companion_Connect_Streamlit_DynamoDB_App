import pandas as pd
import streamlit as st
import boto3
import re
from decimal import Decimal  # DynamoDB requires Decimal for numbers
import time
from botocore.exceptions import ClientError  # Import ClientError for handling DynamoDB exceptions
import datetime

# Function to add background
def add_bg_from_url():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://www.boneappetitkitchen.com/cdn/shop/products/IMG_0431_685x.jpg?v=1635127289");
            background-size: cover;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_url()

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('animals')

# Fetch data from DynamoDB
def get_data_from_dynamodb():
    items = []
    response = table.scan()
    items.extend(response['Items'])
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response['Items'])
    return items

def create_item_in_dynamodb(item_data):
    try:
        item_data['animalage'] = Decimal(str(item_data['animalage']))  # Convert float to Decimal for DynamoDB
        
        # Ensure other fields are appropriately typed as needed
        response = table.put_item(Item=item_data)
        return True
    except Exception as e:
        st.error(f"Failed to create new entry: {str(e)}")
        return False

def fetch_item_by_id(item_id):
    try:
        # Convert the item_id to an integer since the DynamoDB 'id' is a Number
        item_id = int(item_id)
        print(f"Attempting to fetch item with ID: {item_id} (Type: {type(item_id)})")
        response = table.get_item(Key={'id': item_id})
        print("DynamoDB response:", response)
        if 'Item' in response:
            return response['Item']
        else:
            st.warning("Item not found with ID: " + str(item_id))
            return None
    except ValueError:
        st.error("Item ID must be an integer.")
        return None
    except ClientError as e:
        st.error(f"Failed to fetch item: {e.response['Error']['Message']}")
        print(f"ClientError: {e.response}")  # Log full error response
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        print(f"Exception: {e}")  # Log unexpected exceptions
        return None



def update_item_in_dynamodb(item_data):
    try:
        key = {'id': int(item_data['id'])}  # Ensuring the key is an integer if your DynamoDB setup expects it.

        # Building the update expression dynamically
        update_expression = "SET "
        expression_attribute_values = {}
        for key, value in item_data.items():
            if key != 'id':  # Skipping the ID field for updates
                update_expression += f"{key} = :{key}, "
                if isinstance(value, float):
                    expression_attribute_values[f":{key}"] = Decimal(str(value))
                else:
                    expression_attribute_values[f":{key}"] = value
        update_expression = update_expression.rstrip(", ")  # Remove the trailing comma

        # Performing the update
        response = table.update_item(
            Key={'id': item_data['id']},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        logging.info(f"Update successful: {response}")
        return True
    except ClientError as e:
        logging.error(f"Failed to update item: {e.response['Error']['Message']}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return False




def delete_item_from_dynamodb(item_id):
    try:
        # Assuming 'id' is the primary key and it's a string. Adjust if your key is different or composite.
        # Example for a simple key:
        response = table.delete_item(Key={'id': str(item_id)})

        # Example for a composite key:
        # response = table.delete_item(Key={'partitionKeyName': 'value1', 'sortKeyName': 'value2'})
        
        return response
    except ClientError as e:
        if e.response['Error']['Code'] == "ValidationException":
            print("Validation exception:", e.response['Error']['Message'])
        else:
            raise e
    except Exception as e:
        print("Failed to delete item:", e)
        raise e


data = get_data_from_dynamodb()
df = pd.DataFrame(data)
column_order = ['id', 'animalname', 'speciesname', 'breedname', 'sexname', 'animalage',
                'basecolour', 'location', 'sheltercode', 'identichipnumber', 'intakereason',
                'intakedate', 'movementtype', 'movementdate', 'returnedreason',
                'deceasedreason', 'diedoffshelter', 'istransfer', 'istrial', 'puttosleep', 'isdoa']
df = df[column_order]
df.index = df.index + 1
df.columns = ['ID', 'Name', 'Species', 'Breed', 'Sex', 'Age', 'Color', 'Location', 'Shelter Code', 'Chip Number', 'Intake Reason', 'Intake Date', 'Movement Type', 'Movement Date', 'Return Reason', 'Deceased Reason', 'Off Shelter Death', 'Transfer', 'Trial', 'Euthanasia', 'DOA']

# Streamlit UI Layout
st.title('Companion Connect')
st.header("A Data-Driven Platform for Animal Shelter Management and Adoption")

cols = st.columns([5, 1])
with cols[1]:
    action = st.selectbox("Actions:", ["Create", "Read", "Update", "Delete"], key='action_select')

if action == 'Create':
    with st.form("New Animal Form", clear_on_submit=True):
        # Define the specific fields to include in the form
        fields_to_include = ['id', 'animalname', 'speciesname', 'breedname', 'sexname', 'animalage',
                             'basecolour', 'intakereason', 'intakedate']
        # Create a list of columns with 4 columns per row
        form_columns = st.columns(4)
        new_animal_data = {}
        index = 0  # Index to manage which column to place the input field
        for column in fields_to_include:
            current_col = form_columns[index % 4]  # Cycle through columns
            if column == 'animalage':  # Handle numeric input specifically
                new_animal_data[column] = current_col.number_input("Age", key=column, min_value=0.0, step=0.1, format="%.1f")
            elif column == 'intakedate':  # Handle date input
                new_animal_data[column] = current_col.date_input("Intake Date", key=column)
            else:
                new_animal_data[column] = current_col.text_input(column.capitalize(), key=column)
            index += 1  # Increment to place the next field in the next column

        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            try:
                # Ensure ID is an integer and unique
                new_animal_data['id'] = int(new_animal_data['id'])
                existing_ids = {int(item['id']) for item in data}  # Ensure ID uniqueness
                if new_animal_data['id'] in existing_ids:
                    st.error("An entry with this ID already exists. Please use a unique ID.")
                    st.stop()

                if create_item_in_dynamodb(new_animal_data):
                    st.success("New animal entry created successfully!")
                    data = get_data_from_dynamodb()  # Refresh data
                else:
                    st.error("Failed to create new animal entry.")
            except ValueError:
                st.error("Animal ID must be a number.")
                st.stop()


elif action == 'Update':
    st.subheader("Update an Existing Record")
    update_id = st.text_input("Enter the ID of the animal to update:", key="update_id")
    load_button = st.button('Load Animal Details')

    if load_button and update_id:
        item_to_update = fetch_item_by_id(update_id)
        if item_to_update:
            # Create a form populated with the item's existing data
            with st.form("Update Animal Form", clear_on_submit=False):
                update_data = {}
                for key in item_to_update:
                    if key in ['id']:  # Skip non-editable fields like 'id'
                        st.write(f"ID: {item_to_update[key]}")  # Display the ID but do not make it editable
                        update_data[key] = item_to_update[key]
                    elif key == 'animalage':  # Handle numeric inputs
                        update_data[key] = st.number_input("Age", value=float(item_to_update[key]), key=key, min_value=0.0, step=0.1, format="%.1f")
                    elif key == 'intakedate':  # Handle date inputs
                        update_data[key] = st.date_input("Intake Date", value=datetime.datetime.strptime(item_to_update[key], '%Y-%m-%d').date(), key=key)
                    else:
                        update_data[key] = st.text_input(key.capitalize(), value=item_to_update[key], key=key)
                
                update_button = st.form_submit_button("Submit Update")

                if update_button:
                    # Update the record in DynamoDB
                    if update_item_in_dynamodb(update_data):
                        st.success("Animal record updated successfully!")
                    else:
                        st.error("Failed to update the animal record.")
        else:
            st.warning("No record found with that ID.")




elif action == 'Delete':
    delete_id = st.text_input("Enter the ID of the item to delete:", key="delete_id")
    if st.button('Confirm Delete'):
        if delete_id:
            delete_response = delete_item_from_dynamodb(delete_id)
            st.success(f"Item with ID {delete_id} has been deleted.")
        else:
            st.error("Please enter a valid ID.")
            
elif action == 'Read':
    st.header("Find Your Companion")
    search_fields = ['Species', 'Breed', 'Color', 'Age', 'Sex', 'Intake Reason']
    search_cols_layout = st.columns(6)

    # Buttons for searching and refreshing
    button_cols = st.columns([1, 1, 4])
    search_clicked = button_cols[0].button('Search')
    refresh_clicked = button_cols[1].button('Refresh')

    # If the "Refresh" button is clicked, clear the fields and rerun
    if refresh_clicked:
        # Set all search fields in session_state to empty strings before any input widgets are created
        for field in search_fields:
            st.session_state[field] = ""
        # Trigger a rerun of the app to reflect the updated state
        st.experimental_rerun()

    # Create the input fields after checking for refresh
    search_values = {}
    for idx, field in enumerate(search_fields):
        search_values[field] = search_cols_layout[idx].text_input(field, value=st.session_state.get(field, ""), key=field)

    # If the "Search" button is clicked, filter the dataframe
    if search_clicked:
        query_df = df.copy()
        for field in search_fields:
            if search_values[field]:
                # Use a raw string to handle regex special characters correctly
                regex_pattern = fr'\b{re.escape(search_values[field])}\b'
                query_df = query_df[query_df[field].str.contains(regex_pattern, case=False, na=False, regex=True)]
        if query_df.empty:
            st.write("No Matches Found")
        else:
            st.dataframe(query_df)
    elif not search_clicked:
        st.dataframe(df)


