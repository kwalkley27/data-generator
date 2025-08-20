# Copyright 2025 Kyle Walkley
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
import utils

import inference.generator as ig

st.set_page_config(
    page_title="Data Generator",
    layout="wide"
)

def render_header():
    st.title("Data Generator")
    st.markdown("An app that allows users to generate sample data by defining fields with natural language.")

def render_num_record_input() -> int:
    with st.container():
        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            num_records = st.number_input("Enter number of records to generate:", min_value=1, max_value=100, step=1)

    return num_records

def render_clear_data_button():
    # Clear all data button
    if st.button("Clear All Data", type="secondary"):
        st.session_state.table_data = [{'col1': '', 'col2': ''}]
        st.rerun()

def render_action_buttons() -> tuple[bool, bool]:
    with st.container():

        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            submit = st.button("Submit", type="secondary")

        with col2:
            download = st.button("Download", type="secondary")

    return submit, download

def get_formatted_schema():
    try:
        return ig.format_user_input(st.session_state.table_data)
    except ValueError as e:
        st.error(e)

def render_data_box(submit:bool, num_records:int):
    with st.container():
        if submit:
            try:
                formatted_schema = get_formatted_schema()
            except ValueError as e:
                st.error(e)

            st.code(ig.generate_data_sample(num_records, formatted_schema))

def render_field_list():

    # Initialize session state for table data
    if 'table_data' not in st.session_state:
        st.session_state.table_data = [{'col1': '', 'col2': ''}]
    
    # Create containers for the table
    
    with st.container():
        # Create column headers
        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            st.write("**Field Name**")
        with col2:
            st.write("**Value Description**")
        with col3:
            st.write("**Actions**")
        
        # Display each row
        for i, row in enumerate(st.session_state.table_data):
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                # Input for column 1
                st.session_state.table_data[i]['col1'] = st.text_input(
                    f"Row {i+1} Col 1", 
                    value=row['col1'], 
                    key=f"col1_{i}",
                    label_visibility="collapsed"
                )
            
            with col2:
                # Input for column 2
                st.session_state.table_data[i]['col2'] = st.text_input(
                    f"Row {i+1} Col 2", 
                    value=row['col2'], 
                    key=f"col2_{i}",
                    label_visibility="collapsed"
                )
            
            with col3:
                # Action buttons container
                button_col1, button_col2 = st.columns(2)
                
                with button_col1:
                    # Add button (using + symbol)
                    if st.button("➕", key=f"add_{i}", help="Add new row"):
                        st.session_state.table_data.insert(i + 1, {'col1': '', 'col2': ''})
                        st.rerun()
                
                with button_col2:
                    # Delete button (using - symbol) - only show if more than 1 row
                    if len(st.session_state.table_data) > 1:
                        if st.button("🗑️", key=f"delete_{i}", help="Delete this row"):
                            st.session_state.table_data.pop(i)
                            st.rerun()

def on_download(download:bool, num_records:int, formatted_schema:str):
    if download:
        utils.write_string_to_downloads(ig.generate_data_sample(num_records, formatted_schema))

def main():
    render_header()

    render_field_list()

    render_clear_data_button()

    num_records = render_num_record_input()

    submit, download = render_action_buttons()

    render_data_box(submit, num_records)

    on_download(download, num_records, get_formatted_schema())


if __name__ == "__main__":
    main()