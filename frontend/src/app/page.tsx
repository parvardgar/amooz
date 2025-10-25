import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Link from "next/link";

export default function HomePage() {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />

      <main className="flex flex-col flex-1 items-center justify-center text-center px-6 py-20 bg-gradient-to-b from-blue-50 to-white">
        <h1 className="text-5xl md:text-6xl font-extrabold text-gray-800 mb-6">
          Learn Smarter, Not Harder
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mb-8">
          Connect instantly with trusted teachers and improve your learning experience through personalized guidance.
        </p>

        <div className="flex gap-4">
          <Link
            href="/signup"
            className="px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition"
          >
            Get Started
          </Link>
          <Link
            href="/about"
            className="px-6 py-3 border border-blue-600 text-blue-600 rounded-md hover:bg-blue-50 transition"
          >
            Learn More
          </Link>
        </div>
      </main>

      <Footer />
    </div>
  );
}
