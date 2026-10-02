# gui/student_pages.py
import streamlit as st

def show_student_management_page(manager):
    """Renders all components for the student management page."""
    st.header("Student Management")

    # --- Search Section (remains the same) ---
    st.subheader("Find a Student by Name")

    with st.form("find_student"):
        search_name = st.text_input("Enter student name")
        submitted = st.form_submit_button("Search for Student")

    if submitted:
        matches = manager.find_students(search_name)
        if matches and search_name:
            rows = []
            for s in matches:
                course_labels = []
                for course_id in s.enrolled_in:
                    course = manager.find_course_by_id(course_id)
                    course_labels.append(f"{course_id}: {course.name} ({course.instrument})")
                rows.append({
                    "ID": s.student_id,
                    "Name": s.name,
                    "Courses": course_labels or "None",
                })
    
            st.caption(f"{len(rows)} students")
            st.dataframe(rows, hide_index=True, width='stretch')
        else:
            st.info("No matches found")

    st.divider()
    

    # --- Registration Section (now works correctly) ---
    st.subheader("Register New Student")
    with st.form("student_registration_form"):
        reg_name = st.text_input("New Student Name")
        course_options = {f"{c.course_id}: {c.name} ({c.instrument})": c.course_id
                        for c in manager.courses}
        reg_course_label = st.selectbox("Course", list(course_options.keys()), 
                    index=None, placeholder="Select a Course")
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
        index=None,
        placeholder="Select a student"
    )

    if selected_id is None:
        st.info("Select a student to edit their details.")
    else:
        student = student_lookup[selected_id]

        with st.form("update_student_form"):
            new_name = st.text_input("Edit Name", value=student.name,
                                    key=f"upd_name_{selected_id}")
            new_courses = st.multiselect(
                "Edit Courses",
                options=list(course_lookup.keys()),
                default=[course_id for course_id in student.enrolled_in if course_id in course_lookup],
                format_func=lambda course_id: (f"{course_id}: {course_lookup[course_id].name} "
                                        f"({course_lookup[course_id].instrument})"),
                key=f"upd_courses_{selected_id}"
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
        del_label = st.selectbox("Student", list(student_options.keys()), index=None,
                                 placeholder="Select a Student")
        submitted = st.form_submit_button("Delete Student")

    if submitted:
        del_id = student_options[del_label]
        del_student = manager.find_student_by_id(del_id)
        if manager.remove_student(student_options[del_label]):
            st.success(f"Deleted {del_student.name}.")
        else:
            st.error("Could not delete student.")

    st.divider()

    # --- Print Student Card ---
    st.subheader("Print Student Card")

    with st.form("print_student_card"):
        student_options = {f"{c.student_id}: {c.name} ": c.student_id
                        for c in manager.students}
        del_label = st.selectbox("Student", list(student_options.keys()), index=None,
                                    placeholder="Select a Student")
        submitted = st.form_submit_button("Prepare Student Card")
    if submitted:
        try:
            filename, data = manager.print_student_card(student_options[del_label]) 
        except :
            return
        st.download_button(
            label=f"Download Student {student_options[del_label]}'s File",
            data=data,
            file_name=filename,
            mime="text/plain"
            )


    
    
    st.divider()


    # --- List Students ---
    st.subheader("All Students")

    if manager.students:
        rows = []
        for s in manager.students:
            course_labels = []
            for course_id in s.enrolled_in:
                course = manager.find_course_by_id(course_id)
                course_labels.append(f"{course_id}: {course.name} ({course.instrument})")
            rows.append({
                "Student ID": s.student_id,
                "Name": s.name,
                "Courses": course_labels or "None",
            })

        st.caption(f"{len(rows)} students")
        st.dataframe(rows, hide_index=True, width='stretch')
    else:
        st.info("No students in the system.")
        