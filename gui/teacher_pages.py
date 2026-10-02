# gui/teacher_pages.py
import streamlit as st

def show_teacher_management_page(manager):
    """Renders all components for the teacher management page."""
    st.header("Teacher Management")

    # --- Search Section (remains the same) ---
    st.subheader("Find a Teacher by Name or Specialty")

    with st.form("find_teacher"):
        search_term = st.text_input("Enter teacher name")
        submitted = st.form_submit_button("Search for Teacher")

    if submitted:
        matches = manager.find_teachers(search_term)
        if matches and search_term:
            rows = []
            for t in matches:
                rows.append({
                    "ID": t.teacher_id,
                    "Name": t.name,
                    "Specialty": t.speciality
                })
    
            st.caption(f"{len(rows)} teachers")
            st.dataframe(rows, hide_index=True, width='stretch')
        else:
            st.info("No matches found")

    st.divider()
    

    # --- Registration Section ---
    st.subheader("Register New Teacher")
    with st.form("teacher_registration_form"):
        reg_name = st.text_input("New Teacher Name")
        reg_speciality = st.text_input("New Teacher speciality")
        submitted = st.form_submit_button("Register Teacher")

    if submitted:
    # This call now works because we implemented the method in PST3.
    # Add a check for blank name/instrument.
        if reg_name.strip() and reg_speciality.strip():
            manager.add_teacher(reg_name.strip(), reg_speciality)
            st.success(f"Successfully registered {reg_name}!")
            # You can use st.balloons() for extra flair.
        else:
            st.warning("Please enter a name and speciality.")

    st.divider()


    # --- Update Teacher Info ---
    st.subheader("Update Teacher Info")

    teacher_lookup = {t.teacher_id: t for t in manager.teachers}

    # Outside the form so the fields below refresh when the teacher changes
    selected_id = st.selectbox(
        "Select Teacher",
        options=list(teacher_lookup.keys()),
        format_func=lambda teacher_id: f"{teacher_id}: {teacher_lookup[teacher_id].name}",
        index=None, placeholder="Select a teacher"
    )

    if selected_id is None:
        st.info("Select a student to edit their details.")
    else:
        teacher = teacher_lookup[selected_id]

        with st.form("update_teacher_form"):
            new_name = st.text_input("Edit Name", value=teacher.name,
                                    key=f"upd_name_{selected_id}")
            new_speciality = st.text_input("Edit Speciality", value=teacher.speciality,
                                    key=f"upd_speciality_{selected_id}")
            
            submitted = st.form_submit_button("Save Changes")

        if submitted:
            if not new_name.strip() or not new_speciality.strip():
                st.warning("Name and speciality cannot be blank.")
            elif manager.update_teacher(selected_id, name=new_name.strip(), speciality=new_speciality.strip()):
                st.success(f"Updated {new_name.strip()}.")
            else:
                st.error("Could not update teacher.")

    st.divider()


    # --- Remove Teacher ---
    st.subheader("Remove Teacher")
    
    with st.form("remove_teacher_form"):
        teacher_options = {f"{c.teacher_id}: {c.name} ": c.teacher_id
                        for c in manager.teachers}
        del_label = st.selectbox("Teacher", list(teacher_options.keys()),
                                index=None, placeholder="Select a Teacher")
        submitted = st.form_submit_button("Delete Teacher")

    if submitted:
        del_id = teacher_options[del_label]
        del_teacher = manager.find_teacher_by_id(del_id)
        if manager.remove_teacher(teacher_options[del_label]):
            st.success(f"Deleted {del_teacher.name}.")
        else:
            st.error("Could not delete teacher.")

    st.divider()

    # --- List Teachers ---
    st.subheader("All Teachers")

    if manager.teachers:
        rows = []
        for t in manager.teachers:
            rows.append({
                "Teacher ID": t.teacher_id,
                "Name": t.name,
                "Speciality": t.speciality,
            })

        st.caption(f"{len(rows)} teachers")
        st.dataframe(rows, hide_index=True, width='stretch')
    else:
        st.info("No teachers in the system.")