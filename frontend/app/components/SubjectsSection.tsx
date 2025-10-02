interface Subject {
  name: string
  description: string
  color: string
}

export default function SubjectsSection() {
  const subjects: Subject[] = [
    {
      name: 'Math: Pre-K - 8th grade',
      description: 'Build foundational math skills with interactive exercises and videos.',
      color: 'bg-green-500',
    },
    {
      name: 'Computing',
      description: 'Learn programming, computer science, and digital skills for the modern world.',
      color: 'bg-purple-500',
    },
    {
      name: 'Science',
      description: 'Explore biology, chemistry, physics, and more with hands-on learning.',
      color: 'bg-blue-500',
    },
    {
      name: 'Arts & Humanities',
      description: 'Discover history, art, music, and literature from around the world.',
      color: 'bg-yellow-500',
    },
  ]

  return (
    <section className="py-16 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Explore our subjects
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Choose from a wide range of subjects and start learning today.
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {subjects.map((subject, index) => (
            <div
              key={index}
              className="border border-gray-200 rounded-lg overflow-hidden hover:shadow-lg transition-shadow"
            >
              <div className={`h-2 ${subject.color}`}></div>
              <div className="p-6">
                <h3 className="text-lg font-bold text-gray-900 mb-3">{subject.name}</h3>
                <p className="text-gray-600 text-sm">{subject.description}</p>
                <button className="mt-4 text-blue-600 hover:text-blue-800 font-medium text-sm">
                  Start learning →
                </button>
              </div>
            </div>
          ))}
        </div>
        
        {/* Windows Activation Notice (like in your screenshot) */}
        <div className="mt-16 text-center">
          <div className="bg-gray-100 border border-gray-300 rounded-lg p-4 inline-block">
            <p className="text-gray-600 text-sm">
              Activate Windows
              <span className="mx-2">•</span>
              <button className="text-blue-600 hover:text-blue-800 underline">
                Go to Settings to activate Windows
              </button>
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}