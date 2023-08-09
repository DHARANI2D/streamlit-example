import streamlit as st

grade_points = {
    "O": 10.0,
    "A+": 9.0,
    "A": 8.0,
    "B+": 7.0,
    "B": 6.0,
    "C": 5.0,
}

def calculate_adjusted_grade(difficulty, target_cgpa):
    if difficulty == "Difficult":
        return grade_points["C"]
    elif difficulty == "Moderate" and target_cgpa is not None:
        return target_cgpa * 0.75
    else:
        return grade_points["A"]

def main():
    st.title("CGPA Calculator")

    current_cgpa = st.number_input("Current CGPA:", min_value=0.0, max_value=9.9, step=0.1)
    target_cgpa = st.number_input("Target CGPA:", min_value=8.0, max_value=9.9, step=0.1)

    num_subjects = st.number_input("Number of Subjects:", min_value=1, value=1, step=1)

    subject_data = []
    for i in range(num_subjects):
        st.markdown(f"Subject {i + 1}")
        subject_name = st.text_input(f"Subject {i + 1} Name:")
        credits = st.number_input(f"Credits for {subject_name}:", key=f"credits_{i}", min_value=1.0, step=0.5)
        difficulty = st.selectbox(
            f"Difficulty Level for {subject_name}:",
            ["Easy", "Moderate", "Difficult"],
            key=f"difficulty_{i}"
        )

        adjusted_grade = calculate_adjusted_grade(difficulty, target_cgpa)
        rounded_grade_key = max(grade_points, key=lambda key: grade_points[key] <= adjusted_grade)
        subject_data.append((subject_name, credits, rounded_grade_key))


    if st.button("Calculate"):
        st.write("Estimated Grades for Each Subject:")
        for subject_name, credits, grade_key in subject_data:
            st.write(f"{subject_name}: {grade_key} (Credits: {credits})")

        total_credits = sum(credits for _, credits, _ in subject_data)
        weighted_sum = sum(credits * grade_points[grade_key] for _, credits, grade_key in subject_data)
        new_cgpa = (weighted_sum + (current_cgpa * total_credits)) / (total_credits + credits)

        if new_cgpa > target_cgpa:
            cgpa_decrease = new_cgpa - target_cgpa
            st.warning(f"Estimated CGPA exceeds Target CGPA by {cgpa_decrease:.2f}. Adjusting grades...")

            st.write("Adjusted Grades:")
            for i in range(num_subjects):
                subject_data[i] = (subject_data[i][0], subject_data[i][1], "C")

            for subject_name, credits, grade_key in subject_data:
                st.write(f"{subject_name}: {grade_key} (Credits: {credits})")

            new_cgpa = target_cgpa

        if new_cgpa < 5.0:
            st.warning("Estimated CGPA went below 5.0. Adjusting grades and target CGPA...")
            reduction_factor = (5.0 - current_cgpa * total_credits) / credits
            for i in range(num_subjects):
                subject_data[i] = (subject_data[i][0], subject_data[i][1], calculate_adjusted_grade(subject_data[i][2], target_cgpa))
            target_cgpa = 5.0
            new_cgpa = 5.0

        st.success(f"Estimated CGPA: {new_cgpa:.2f}")

        if new_cgpa < target_cgpa:
            st.info("Your capabilities are low estimated,So your Modified Target CGPA: {target_cgpa:.2f}")
    
    st.write("<p style='text-align: center;'>Crafted with fervor by 2D🤓</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
