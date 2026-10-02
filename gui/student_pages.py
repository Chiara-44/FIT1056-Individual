# gui/student_pages.py
import streamlit as st

def show_student_management_page(manager):
    """Renders all components for the student management page."""
    st.header("Student Management")

    # --- Search Section (remains the same) ---
    st.subheader("Find a Student")

    st.divider()
    

    # --- Registration Section (now works correctly) ---
    st.subheader("Register New Student")
    with st.form("registration_form"):
        reg_name = st.text_input("New Student Name")
        course_options = {f"{c.course_id}: {c.name} ({c.instrument})": c.course_id
                        for c in manager.courses}
        reg_course_label = st.selectbox("Course", list(course_options.keys()))
        submitted = st.form_submit_button("Register Student")

    if submitted:
    # This call now works because we implemented the method in PST3.
    # Add a check for blank name/instrument.
        if reg_name.strip():
            course_id = course_options[reg_course_label]
            manager.add_student(reg_name.strip(), [course_id])
            st.success(f"Successfully registered {reg_name}!")
            # You can use st.balloons() for extra flair.
        else:
            st.warning("Please enter a name.")

    st.divider()


    # --- Update Student Info ---
    st.subheader("Update Student Info")

    student_lookup = {s.student_id: s for s in manager.students}
    course_lookup = {c.course_id: c for c in manager.courses}

    # Outside the form so the fields below refresh when the student changes
    selected_id = st.selectbox(
        "Select Student",
        options=list(student_lookup.keys()),
        format_func=lambda student_id: f"{student_id}: {student_lookup[student_id].name}",
    )
    student = student_lookup[selected_id]

    with st.form("update_student_form"):
        new_name = st.text_input("Name", value=student.name,
                                key=f"upd_name_{selected_id}")
        new_courses = st.multiselect(
            "Courses",
            options=list(course_lookup.keys()),
            default=[course_id for course_id in student.enrolled_in if course_id in course_lookup],
            format_func=lambda course_id: (f"{course_id}: {course_lookup[course_id].name} "
                                    f"({course_lookup[course_id].instrument})"),
            key=f"upd_courses_{selected_id}",
        )
        submitted = st.form_submit_button("Save Changes")

    if submitted:
        if not new_name.strip():
            st.warning("Name cannot be blank.")
        elif manager.update_student(selected_id,
                                    name=new_name.strip(),
                                    enrolled_in=new_courses):
            st.success(f"Updated {new_name.strip()}.")
        else:
            st.error("Could not update student.")

    st.divider()



    # --- Remove Student ---
    st.subheader("Remove Student")
    
    with st.form("remove_student_form"):
        student_options = {f"{c.student_id}: {c.name} ": c.student_id
                        for c in manager.students}
        del_label = st.selectbox("Student", list(student_options.keys()))
        submitted = st.form_submit_button("Delete Student")

    del_id = student_options[del_label]
    del_student = manager.find_student_by_id(del_id)
    if submitted:
        if manager.remove_student(student_options[del_label]):
            st.success(f"Deleted {del_student.name}.")
        else:
            st.error("Could not delete student.")

    st.divider()
        