"use client";

import { useParams } from "next/navigation";
import { useState } from "react";
import { profileFormConfig, FormField } from "../../../../config/profileFormConfig";
import api from "../../../../lib/api";

export default function CreateProfilePage() {
  const { role } = useParams() as { role: "student" | "teacher" | "parent" };
  const [formData, setFormData] = useState<Record<string, any>>({});
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const fields: FormField[] = profileFormConfig[role];

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setMessage("");
    setLoading(true);

    try {
      const res = await api.post(`/profile/create/${role}`, formData);
      if (res.status === 201) setMessage("Profile created successfully!");
      else setMessage("Profile creation failed.");
    } catch (err) {
      console.error(err);
      setMessage("Failed to create profile");
    } finally {
      setLoading(false);
    }
  }

  function handleChange(name: string, value: any) {
    setFormData((prev) => ({ ...prev, [name]: value }));
  }

  return (
    <div className="max-w-lg mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4 capitalize">
        Create {role} Profile
      </h1>

      {!fields ? (
        <p className="text-red-600">Invalid role: {role}</p>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          {fields.map((field) => (
            <div key={field.name}>
              <label className="block mb-1 font-medium">{field.label}</label>

              {field.type === "select" ? (
                <select
                  value={formData[field.name] || ""}
                  onChange={(e) => handleChange(field.name, e.target.value)}
                  className="w-full p-2 border rounded-md"
                  required
                >
                  <option value="">Select {field.label}</option>
                  {field.options?.map((opt) => (
                    <option key={opt.value} value={opt.value}>
                      {opt.label}
                    </option>
                  ))}
                </select>
              ) : (
                <input
                  type={field.type || "text"}
                  placeholder={field.placeholder || field.label}
                  value={formData[field.name] || ""}
                  onChange={(e) => handleChange(field.name, e.target.value)}
                  className="w-full p-2 border rounded-md"
                  required
                />
              )}
            </div>
          ))}

          <button
            type="submit"
            disabled={loading}
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400"
          >
            {loading ? "Saving..." : "Save Profile"}
          </button>
        </form>
      )}

      {message && (
        <p className="mt-4 text-center text-green-600 font-medium">
          {message}
        </p>
      )}
    </div>
  );
}