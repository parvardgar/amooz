export default function Hero() {
  return (
    <section className="bg-gradient-to-r from-blue-500 to-blue-700 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <div className="text-center">
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6 leading-tight">
            For every student,
            <br />
            every classroom.
            <br />
            <span className="text-yellow-300">Real results.</span>
          </h1>
          <p className="text-xl md:text-2xl mb-10 max-w-3xl mx-auto leading-relaxed">
            We&apos;re a nonprofit with the mission to provide a free, world-class education for anyone, anywhere.
          </p>
          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <button className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-blue-50 transition-colors shadow-lg">
              Start learning now
            </button>
            <button className="bg-transparent border-2 border-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-white/10 transition-colors">
              Learn more
            </button>
          </div>
        </div>
      </div>
    </section>
  )
}