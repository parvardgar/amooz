export type FormField = {
  label: string;
  name: string;
  type?: "text" | "number" | "select";
  placeholder?: string;
  options?: { label: string; value: string | number }[];
};

export const profileFormConfig: Record<string, FormField[]> = {
  student: [
    { label: "NationCode", name: "nation_code" },
    { label: "Gender", name: "gender", type: "select",
       options: [{label: "Female", value: "0"}, {label: "Male", value: "1"}] },
    {
      label: "Grade",
      name: "grade",
      type: "select",
      options: [
        { label: "Grade 1", value: "1" },
        { label: "Grade 2", value: "2" },
        { label: "Grade 3", value: "3" },
        { label: "Grade 4", value: "4" },
        { label: "Grade 5", value: "5" },
        { label: "Grade 6", value: "6" },
        { label: "Grade 7", value: "7" },
        { label: "Grade 8", value: "8" },
        { label: "Grade 9", value: "9" },
        { label: "Grade 10", value: "10" },
        { label: "Grade 11", value: "11" },
        { label: "Grade 12", value: "12" },
      ],
    },
    { label: "Last Year Avg", name: "last_year_avg" },
  ],
  teacher: [
    { label: "Nation Code", name: "nation_code" },
    { label: "Gender", name: "gender" },

    { label: "Specialization", name: "specialization" },
    { label: "Experience (years)", name: "experience_years", type: "number" },
    { label: "License Number", name: "license_number" },
    { label: "Consultation Fee", name: "consultation_fee", type: "number" },
  ],
  parent: [
    
    { label: "Occupation", name: "occupation" },
    { label: "Number of Children", name: "children_count", type: "number" },
  ],
};