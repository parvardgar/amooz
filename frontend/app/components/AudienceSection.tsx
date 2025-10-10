interface AudienceItem {
  title: string
  description: string
  icon: string
}

export default function AudienceSection() {
  const audienceItems: AudienceItem[] = [
    {
      title: 'Students',
      description: 'Students of all ages can build and deepen their skills with our engaging content.',
      icon: '🎓',
    },
    {
      title: 'Teachers',
      description: 'Empower your teaching with tools and resources to support student learning.',
      icon: '👩‍🏫',
    },
    {
      title: 'Parents',
      description: 'Support your child\'s learning journey with insights and progress tracking.',
      icon: '👨‍👩‍👧‍👦',
    },
  ]

  return (
    <section className="py-16 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Who can benefit from LearnHub?
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Our platform is designed to support students, educators, and families in their educational journey.
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {audienceItems.map((item, index) => (
            <div
              key={index}
              className="bg-white p-8 rounded-lg shadow-md hover:shadow-lg transition-shadow text-center"
            >
              <div className="text-4xl mb-4">{item.icon}</div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">{item.title}</h3>
              <p className="text-gray-600">{item.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}