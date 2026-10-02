# gui/course_pages.py
import streamlit as st
import datetime


def show_course_management_page(manager):
    """Renders all components for the course management page."""
    st.header("Course Management")

    # --- Add a new Course ---
    st.subheader("Add a new Course")

    with st.form("add_course_form"):
        reg_course_ID = st.text_input("New Course ID")
        reg_name = st.text_input("New Course Name")
        reg_instrument = st.text_input("New Course Instrument")
        teacher_options = {f"{c.teacher_id}: {c.name} ": c.teacher_id
                        for c in manager.teachers}
        del_label = st.selectbox("Teacher", list(teacher_options.keys()),
                                index=None, placeholder="Select a Teacher")
        submitted = st.form_submit_button("Add Course")



    if submitted:
        if not (reg_course_ID.strip() and reg_name.strip()
                and reg_instrument.strip() and teacher_options[del_label]):
            st.warning("Please enter a course ID, course name, instrument, and teacher ID.")
        else:
            try:
                clean_course_ID = int(reg_course_ID.strip())
            except ValueError:
                st.warning("Course ID and Teacher ID must be whole numbers.")
            else:
                course = manager.add_course(clean_course_ID, reg_name.strip(),
                                            reg_instrument.strip(), teacher_options[del_label])
                if course == 101:
                    st.warning(f"Course ID {clean_course_ID} already exists.")
                elif course == 102:
                    st.warning(f"Teacher with ID {teacher_options[del_label]} not found.")
                else:
                    st.success(f"Added {reg_name}.")

    st.divider()

    # --- Add Lesson to Course ---
    st.subheader("Add a Lesson to a Course")
    
    with st.form("add_lesson_to_course_form"):
        course_options = {f"{c.course_id}: {c.name} ({c.instrument})": c.course_id
                                for c in manager.courses}
        reg_course_label = st.selectbox("Course", list(course_options.keys()), 
                index=None, placeholder="Select a Course")
        reg_day = st.selectbox("Day",options=("Monday", "Tuesday", 
                                        "Wednesday", "Thursday", "Friday", 
                                        "Saturday", "Sunday"), index=None, placeholder="Choose a Day")
        reg_start_time = st.time_input("Start Time", value=None)
        reg_room = st.text_input("Room")
        submitted = st.form_submit_button("Add Course")
        

    if submitted:
        course_id = course_options[reg_course_label]
        if not (course_id and reg_day and reg_start_time and reg_room):
            st.warning("Please enter a course ID, Day, Time, and Room.")
        else:
            lesson_id = manager.add_lesson_to_course(course_id, reg_day, 
                            reg_start_time.strftime("%H:%M"), reg_room)
            if lesson_id:
                course = manager.find_course_by_id(course_id)
                st.success(f"Added Lesson with Lesson ID: {lesson_id} to {course_id}: {course.name}")

    st.divider()

    # --- List Courses ---
    st.subheader("All Courses")

    if manager.courses:
        rows = []
        for c in manager.courses:
            rows.append({
                "Course ID": c.course_id,
                "Name": c.name,
                "Instrument": c.instrument,
                "Teacher": manager.find_teacher_by_id(c.teacher_id).name
            })

        st.caption(f"{len(rows)} courses")
        st.dataframe(rows, hide_index=True, width='stretch')
    else:
        st.info("No courses in the system.")