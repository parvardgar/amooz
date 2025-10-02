import Header from './components/Header'
import Hero from './components/Hero'
import AudienceSection from './components/AudienceSection'
import SubjectsSection from './components/SubjectsSection'

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      <Header />
      <Hero />
      <AudienceSection />
      <SubjectsSection />
    </div>
  )
}